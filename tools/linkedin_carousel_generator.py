#!/usr/bin/env python3
"""
Generates a LinkedIn carousel PDF from carousel content JSON.
Reads:  .tmp/linkedin_carousel_content.json
Saves:  .tmp/linkedin_carousel.pdf
Usage:  python tools/linkedin_carousel_generator.py

Style: Matt Gray minimalist — dark cover, light slides, clean typography.
PDF dimensions: 210mm x 263mm (~4:5 ratio, optimal for LinkedIn carousel).
"""

import json
from pathlib import Path

from fpdf import FPDF

CAROUSEL_INPUT  = Path(".tmp/linkedin_carousel_content.json")
CAROUSEL_OUTPUT = Path(".tmp/linkedin_carousel.pdf")

# Dimensions (mm)
W = 210
H = 263

# Colour palette
DARK_BG    = (15, 15, 20)       # Near-black cover/last slide
LIGHT_BG   = (250, 249, 247)    # Off-white content slides
ACCENT     = (99, 102, 241)     # Indigo — subtle brand colour
WHITE      = (255, 255, 255)
DARK_TEXT  = (20, 20, 28)
MUTED_TEXT = (110, 110, 120)
ACCENT_BAR = (99, 102, 241)

# Typography (pt)
COVER_TITLE_SIZE    = 32
COVER_SUBTITLE_SIZE = 14
SLIDE_TITLE_SIZE    = 22
SLIDE_BODY_SIZE     = 13
SLIDE_NUMBER_SIZE   = 9
LAST_CTA_SIZE       = 18
FOOTER_SIZE         = 8


def load_carousel(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Carousel content not found: {path}")
    with open(path) as f:
        return json.load(f)


class CarouselPDF(FPDF):
    def set_bg(self, r: int, g: int, b: int):
        self.set_fill_color(r, g, b)
        self.rect(0, 0, W, H, "F")

    def accent_bar(self, y: float, width: float = 12, height: float = 3):
        self.set_fill_color(*ACCENT_BAR)
        self.rect(16, y, width, height, "F")

    def draw_cover(self, title: str, subtitle: str, week: int):
        self.add_page()
        self.set_bg(*DARK_BG)

        # Top corner label
        self.set_font("Helvetica", "", FOOTER_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(16, 16)
        self.cell(0, 6, f"WEEK {week}", ln=True)

        # Accent bar
        self.accent_bar(38)

        # Title
        self.set_font("Helvetica", "B", COVER_TITLE_SIZE)
        self.set_text_color(*WHITE)
        self.set_xy(16, 48)
        self.multi_cell(W - 32, 12, title, align="L")

        # Subtitle
        y_after_title = self.get_y() + 10
        self.set_font("Helvetica", "", COVER_SUBTITLE_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(16, y_after_title)
        self.multi_cell(W - 32, 7, subtitle, align="L")

        # Bottom branding
        self.set_font("Helvetica", "", FOOTER_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(16, H - 20)
        self.cell(0, 6, "The Bell by Nabilah", align="L")

        # Swipe prompt
        self.set_xy(0, H - 20)
        self.cell(W - 16, 6, "swipe →", align="R")

    def draw_slide(self, slide_num: int, total_slides: int, title: str, body: str, week: int):
        self.add_page()
        self.set_bg(*LIGHT_BG)

        # Slide number top-right
        self.set_font("Helvetica", "", SLIDE_NUMBER_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(0, 16)
        self.cell(W - 16, 6, f"{slide_num}/{total_slides}", align="R")

        # Accent bar
        self.accent_bar(38)

        # Title
        self.set_font("Helvetica", "B", SLIDE_TITLE_SIZE)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(16, 48)
        self.multi_cell(W - 32, 9, title, align="L")

        # Divider line
        y_divider = self.get_y() + 6
        self.set_draw_color(*MUTED_TEXT)
        self.set_line_width(0.3)
        self.line(16, y_divider, W - 16, y_divider)

        # Body
        self.set_font("Helvetica", "", SLIDE_BODY_SIZE)
        self.set_text_color(*DARK_TEXT)
        self.set_xy(16, y_divider + 10)
        self.multi_cell(W - 32, 7, body, align="L")

        # Bottom nav
        self.set_font("Helvetica", "", FOOTER_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(16, H - 20)
        self.cell(0, 6, "The Bell by Nabilah", align="L")
        self.set_xy(0, H - 20)
        self.cell(W - 16, 6, "swipe →", align="R")

    def draw_last_slide(self, cta: str):
        self.add_page()
        self.set_bg(*DARK_BG)

        # Accent bar centred vertically above CTA
        self.accent_bar(H / 2 - 40)

        # CTA text
        self.set_font("Helvetica", "B", LAST_CTA_SIZE)
        self.set_text_color(*WHITE)
        self.set_xy(16, H / 2 - 28)
        self.multi_cell(W - 32, 9, cta, align="L")

        # Branding
        self.set_font("Helvetica", "", FOOTER_SIZE)
        self.set_text_color(*MUTED_TEXT)
        self.set_xy(16, H - 20)
        self.cell(0, 6, "The Bell by Nabilah · nabilahazman249@gmail.com", align="L")


def main():
    data = load_carousel(CAROUSEL_INPUT)

    week           = data.get("week", 1)
    cover_title    = data.get("cover_title", "This Week's Build")
    cover_subtitle = data.get("cover_subtitle", "What actually happened")
    slides         = data.get("slides", [])
    last_slide     = data.get("last_slide", "Follow for weekly posts on building with AI from scratch.")

    if not slides:
        print("WARNING: No slides found in carousel content. PDF will only have cover and last slide.")

    pdf = CarouselPDF(orientation="P", unit="mm", format=(W, H))
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(0, 0, 0)

    # Cover
    pdf.draw_cover(cover_title, cover_subtitle, week)

    # Content slides
    total = len(slides)
    for i, slide in enumerate(slides, start=1):
        title = slide.get("title", "")
        body  = slide.get("body", "")
        pdf.draw_slide(i, total, title, body, week)

    # Last slide (CTA)
    pdf.draw_last_slide(last_slide)

    CAROUSEL_OUTPUT.parent.mkdir(exist_ok=True)
    pdf.output(str(CAROUSEL_OUTPUT))

    pages = 1 + total + 1
    size_kb = round(CAROUSEL_OUTPUT.stat().st_size / 1024, 1)
    print(f"  ✓ Carousel PDF → {CAROUSEL_OUTPUT} ({pages} pages, {size_kb} KB)")


if __name__ == "__main__":
    main()
