#!/usr/bin/env python3
"""
Parse linkedin_52_slides.md → generate 52 carousel PDFs.
Outputs: .tmp/carousel_pdfs/carousel_NN_slug.pdf
JSON inputs cached at: .tmp/carousel_inputs/carousel_NN.json
"""

import json, re, sys, time
from pathlib import Path

SLIDES_MD    = Path(".tmp/linkedin_52_slides.md")
INPUT_DIR    = Path(".tmp/carousel_inputs")
OUTPUT_DIR   = Path(".tmp/carousel_pdfs")
SLIDES_DIR   = Path(".tmp/carousel_slides")

LAST_SLIDE_CTA = "Follow for weekly posts on building with AI."

# Week offset: set to 0 if carousel #1 = week 1, or 1 if carousel #1 = week 2, etc.
WEEK_OFFSET = 1


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:40]


def parse_slides_md(path: Path) -> list[dict]:
    """Return list of {num, title, slides: [str×5]} for all 52 carousels."""
    text = path.read_text()
    carousels = []
    blocks = re.split(r"### (\d+)\. (.+)", text)
    # blocks[0] = preamble, then triplets: [num, title, content]
    i = 1
    while i + 2 < len(blocks):
        num   = int(blocks[i].strip())
        title = blocks[i + 1].strip()
        body  = blocks[i + 2]
        slides = re.findall(r"S\d+:\s*(.+)", body)
        if len(slides) == 5:
            carousels.append({"num": num, "title": title, "slides": slides})
        i += 3
    return carousels


def make_cover_title(title: str) -> str:
    """Shorten title for the big 104px cover headline if needed."""
    return title


def make_cover_subtitle(title: str) -> str:
    return ""


def build_json(carousel: dict) -> dict:
    week = carousel["num"] + WEEK_OFFSET
    return {
        "week": week,
        "post_type": "carousel",
        "cover_title": make_cover_title(carousel["title"]),
        "cover_subtitle": make_cover_subtitle(carousel["title"]),
        "slides": [{"text": s} for s in carousel["slides"]],
        "last_slide": LAST_SLIDE_CTA,
    }


def generate_pdf(data: dict, output_path: Path):
    """Call carousel generator internals directly."""
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Import selector + generator
    from tools.diagram_selector import assign_diagrams
    from tools.linkedin_carousel_generator import (
        cover_html, slide_html, last_html, render_slides, combine_to_pdf
    )

    slides   = data["slides"]
    week     = data["week"]
    svgs     = assign_diagrams(slides)

    all_slides = [(cover_html(data["cover_title"], data["cover_subtitle"], week), "cover")]
    for i, (s, svg) in enumerate(zip(slides, svgs), 1):
        text = s.get("text") or s.get("title", "")
        all_slides.append((slide_html(i, len(slides), text, svg), f"slide{i}"))
    all_slides.append((last_html(data["last_slide"]), "last"))

    png_paths = render_slides(all_slides)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combine_to_pdf(png_paths, output_path)


def main():
    start_carousel = 1
    end_carousel   = 52

    if len(sys.argv) >= 2:
        start_carousel = int(sys.argv[1])
    if len(sys.argv) >= 3:
        end_carousel = int(sys.argv[2])

    print(f"Parsing {SLIDES_MD.name}...")
    carousels = parse_slides_md(SLIDES_MD)
    print(f"  Found {len(carousels)} carousels\n")

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    batch = [c for c in carousels if start_carousel <= c["num"] <= end_carousel]
    print(f"Generating carousels {start_carousel}–{end_carousel} ({len(batch)} total)\n")

    failed = []
    for i, carousel in enumerate(batch, 1):
        num   = carousel["num"]
        slug  = slugify(carousel["title"])
        label = f"{num:02d}_{slug}"

        json_path = INPUT_DIR / f"carousel_{num:02d}.json"
        pdf_path  = OUTPUT_DIR / f"carousel_{label}.pdf"

        data = build_json(carousel)
        json_path.write_text(json.dumps(data, indent=2))

        print(f"[{i}/{len(batch)}] Carousel {num}: {carousel['title'][:55]}")
        t0 = time.time()
        try:
            generate_pdf(data, pdf_path)
            kb = round(pdf_path.stat().st_size / 1024, 1)
            print(f"        → {pdf_path.name} ({kb} KB, {time.time()-t0:.1f}s)")
        except Exception as e:
            print(f"        ✗ FAILED: {e}")
            failed.append(num)
        print()

    print("=" * 60)
    print(f"Done. {len(batch) - len(failed)}/{len(batch)} PDFs generated.")
    if failed:
        print(f"Failed carousels: {failed}")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
