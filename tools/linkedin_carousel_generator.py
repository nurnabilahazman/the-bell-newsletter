#!/usr/bin/env python3
"""
LinkedIn carousel — reference design: cream bg, big centered statement,
one [[highlighted]] phrase per slide, minimal branding.
"""

import json, re
from pathlib import Path

CAROUSEL_INPUT  = Path(".tmp/linkedin_carousel_content.json")
CAROUSEL_OUTPUT = Path(".tmp/linkedin_carousel.pdf")
SLIDES_DIR      = Path(".tmp/carousel_slides")
LOGO_PATH       = Path("brand_assets/logo.svg")

W, H = 1080, 1350

CREAM  = "#f5f0e8"
DARK   = "#111111"
ACCENT = "#C9A84C"
MUTED  = "#777777"
WHITE  = "#ffffff"

# Highlight: warm amber box, text stays black — readable, no purple clash
HL_BG  = "#fde68a"
HL_COL = "#111111"


# Bell logo — original brand colours: navy body, gold crown + clapper
# Used as the main visual on content slides (140px tall)
BELL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"
     width="130" height="130" style="display:block;">
  <!-- crown / handle -->
  <path d="M88 50 L88 28 Q88 14 100 14 Q112 14 112 28 L112 50 Z" fill="#C9A84C"/>
  <!-- bell body -->
  <path d="M88 50 C55 58 26 92 22 132 C20 150 26 168 40 172
           L160 172 C174 168 180 150 178 132 C174 92 145 58 112 50 Z"
        fill="#1A1A2E"/>
  <!-- clapper -->
  <circle cx="100" cy="183" r="10" fill="#C9A84C"/>
</svg>"""

# Cover logo — navy bell + gold crown + "BELL" wordmark only (no NEWSLETTER)
BELL_SVG_LG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240"
     width="150" height="180" style="display:block;">
  <path d="M88 50 L88 28 Q88 14 100 14 Q112 14 112 28 L112 50 Z" fill="#C9A84C"/>
  <path d="M88 50 C55 58 26 92 22 132 C20 150 26 168 40 172
           L160 172 C174 168 180 150 178 132 C174 92 145 58 112 50 Z"
        fill="#1A1A2E"/>
  <circle cx="100" cy="183" r="10" fill="#C9A84C"/>
  <text x="100" y="225" font-family="Georgia,serif" font-size="34" font-weight="700"
        fill="#1A1A2E" text-anchor="middle" letter-spacing="10">BELL</text>
</svg>"""


# SVG diagram definitions — minimal style: thin lines, gold squares, white space
# Canvas inner width: 1080 - 2*88px = 904px usable. SVG set to 820px, centered.

def _diagram_1() -> str:
    """52 gold squares — one per newsletter edition per year."""
    cols, rows, sq, gap = 13, 4, 48, 8
    total_w = cols * sq + (cols - 1) * gap   # 720
    ox = (820 - total_w) // 2                # 50
    oy = 90
    rects = []
    for r in range(rows):
        for c in range(cols):
            x = ox + c * (sq + gap)
            y = oy + r * (sq + gap)
            rects.append(f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" rx="5" fill="#C9A84C"/>')
    grid = "\n  ".join(rects)
    return f"""<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <text x="410" y="46" font-size="20" fill="#666" text-anchor="middle" font-style="italic">One square = one newsletter</text>
  {grid}
  <line x1="50" y1="350" x2="770" y2="350" stroke="#ddd8cf" stroke-width="1"/>
  <text x="50" y="402" font-size="26" fill="#1A1A2E" font-weight="700">52 newsletters / year</text>
  <text x="770" y="402" font-size="26" fill="#C9A84C" font-weight="900" text-anchor="end">0 hrs effort</text>
</svg>"""

DIAGRAM_1 = _diagram_1()

DIAGRAM_2 = """<svg width="820" height="520" viewBox="0 0 820 520" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Clock face -->
  <circle cx="410" cy="230" r="180" fill="#f0ece3" stroke="#1A1A2E" stroke-width="2"/>
  <!-- Hour tick marks -->
  <line x1="410" y1="58"  x2="410" y2="78"  stroke="#1A1A2E" stroke-width="3"/>
  <line x1="497" y1="83"  x2="489" y2="97"  stroke="#1A1A2E" stroke-width="2"/>
  <line x1="561" y1="143" x2="550" y2="152" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="582" y1="230" x2="562" y2="230" stroke="#1A1A2E" stroke-width="3"/>
  <line x1="561" y1="317" x2="550" y2="308" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="497" y1="377" x2="489" y2="363" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="410" y1="402" x2="410" y2="382" stroke="#1A1A2E" stroke-width="3"/>
  <line x1="323" y1="377" x2="331" y2="363" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="259" y1="317" x2="270" y2="308" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="238" y1="230" x2="258" y2="230" stroke="#1A1A2E" stroke-width="3"/>
  <line x1="259" y1="143" x2="270" y2="152" stroke="#1A1A2E" stroke-width="2"/>
  <line x1="323" y1="83"  x2="331" y2="97"  stroke="#1A1A2E" stroke-width="2"/>
  <!-- Minute hand: 12 oclock -->
  <line x1="410" y1="230" x2="410" y2="90" stroke="#1A1A2E" stroke-width="4" stroke-linecap="round"/>
  <!-- Hour hand: 1am — GOLD, my personal choice -->
  <line x1="410" y1="230" x2="465" y2="135" stroke="#C9A84C" stroke-width="7" stroke-linecap="round"/>
  <!-- Center hub -->
  <circle cx="410" cy="230" r="9" fill="#1A1A2E"/>
  <circle cx="410" cy="230" r="4" fill="#C9A84C"/>
  <!-- Label -->
  <text x="410" y="455" font-size="32" fill="#1A1A2E" text-anchor="middle" font-weight="700">I chose 1am.</text>
  <text x="410" y="497" font-size="20" fill="#666" text-anchor="middle">Set yours to any time.</text>
</svg>"""

DIAGRAM_3 = """<svg width="820" height="500" viewBox="0 0 820 500" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Left: input effort — small, gray, fading -->
  <text x="190" y="180" font-size="110" fill="#e8e4db" font-weight="900" text-anchor="middle">1</text>
  <text x="190" y="270" font-size="30" fill="#666" text-anchor="middle" font-weight="600">weekend</text>
  <text x="190" y="310" font-size="22" fill="#777" text-anchor="middle">to build it</text>
  <!-- Center divider -->
  <line x1="410" y1="60" x2="410" y2="440" stroke="#e0ddd7" stroke-width="1.5"/>
  <!-- Arrow pointing right -->
  <text x="410" y="200" font-size="36" fill="#aaa" text-anchor="middle">→</text>
  <!-- Right: return — large, gold, FOCAL POINT -->
  <text x="630" y="210" font-size="160" fill="#C9A84C" font-weight="900" text-anchor="middle">52</text>
  <text x="630" y="295" font-size="30" fill="#1A1A2E" text-anchor="middle" font-weight="700">weeks it runs</text>
  <text x="630" y="334" font-size="22" fill="#666" text-anchor="middle">on its own</text>
  <!-- Bottom label -->
  <text x="410" y="460" font-size="20" fill="#666" text-anchor="middle">Build once. Runs forever.</text>
</svg>"""

DIAGRAM_4 = """<svg width="820" height="500" viewBox="0 0 820 500" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Source: GitHub Actions (small, at top) -->
  <rect x="260" y="10" width="300" height="62" rx="9" fill="#1A1A2E"/>
  <text x="410" y="48" font-size="24" fill="#fff" text-anchor="middle" font-weight="700">GitHub Actions</text>
  <!-- Stem from source to branch point -->
  <line x1="410" y1="72" x2="410" y2="160" stroke="#ddd8cf" stroke-width="1.5"/>
  <circle cx="410" cy="163" r="5" fill="#C9A84C"/>
  <!-- Three branches fanning out -->
  <line x1="410" y1="163" x2="130" y2="280" stroke="#ddd8cf" stroke-width="1.5"/>
  <line x1="410" y1="163" x2="410" y2="280" stroke="#ddd8cf" stroke-width="1.5"/>
  <line x1="410" y1="163" x2="690" y2="280" stroke="#ddd8cf" stroke-width="1.5"/>
  <!-- Output 1: Email Newsletter — FOCAL POINT left -->
  <rect x="20" y="280" width="220" height="80" rx="9" fill="none" stroke="#1A1A2E" stroke-width="1.5"/>
  <text x="130" y="314" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">Email</text>
  <text x="130" y="340" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">Newsletter</text>
  <!-- Output 2: LinkedIn Post — FOCAL POINT center -->
  <rect x="300" y="280" width="220" height="80" rx="9" fill="none" stroke="#1A1A2E" stroke-width="1.5"/>
  <text x="410" y="314" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">LinkedIn</text>
  <text x="410" y="340" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">Post</text>
  <!-- Output 3: Carousel PDF — FOCAL POINT right -->
  <rect x="580" y="280" width="220" height="80" rx="9" fill="none" stroke="#1A1A2E" stroke-width="1.5"/>
  <text x="690" y="314" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">Carousel</text>
  <text x="690" y="340" font-size="21" fill="#1A1A2E" text-anchor="middle" font-weight="700">PDF</text>
  <!-- Caption -->
  <text x="410" y="440" font-size="22" fill="#666" text-anchor="middle">3 outputs. 0 manual work. Every Monday.</text>
</svg>"""

DIAGRAM_5 = """<svg width="820" height="340" viewBox="0 0 820 340" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Week labels above squares -->
  <text x="170" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">WK 1</text>
  <text x="290" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">WK 2</text>
  <text x="410" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">WK 3</text>
  <text x="530" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">WK 4</text>
  <text x="650" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">WK 5</text>
  <!-- 5 failed squares — dark with white X -->
  <rect x="120" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>
  <line x1="132" y1="68" x2="208" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="208" y1="68" x2="132" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="240" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>
  <line x1="252" y1="68" x2="328" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="328" y1="68" x2="252" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="360" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>
  <line x1="372" y1="68" x2="448" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="448" y1="68" x2="372" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="480" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>
  <line x1="492" y1="68" x2="568" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="568" y1="68" x2="492" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <rect x="600" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>
  <line x1="612" y1="68" x2="688" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="688" y1="68" x2="612" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Caption -->
  <text x="410" y="226" font-size="28" fill="#1A1A2E" font-weight="700" text-anchor="middle">Sent. Delivered. Broken.</text>
  <text x="410" y="278" font-size="22" fill="#666" text-anchor="middle">No alert. No error. Five weeks of silence.</text>
</svg>"""

_DIAGRAM_SVGS: list = []  # populated at runtime by assign_diagrams()


def clean_html(text: str) -> str:
    return (text
        .replace("--", " ")
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace("\u201c", '"').replace("\u201d", '"')
        .replace("\u2018", "'").replace("\u2019", "'")
        .replace("**", "").replace("*", ""))


def render_statement(text: str) -> str:
    parts = re.split(r'\[\[(.+?)\]\]', text)
    out = ""
    for i, part in enumerate(parts):
        p = clean_html(part.strip())
        if not p:
            continue
        if i % 2 == 1:
            out += f'<span class="hl">{p}</span>'
        else:
            out += f'<span>{p}</span>'
    return out.strip()


FONTS = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');"
BASE  = f"""
{FONTS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; font-family:'Inter',system-ui,sans-serif; overflow:hidden; }}
.hl {{
  background:{HL_BG}; color:{HL_COL};
  font-weight:900;
  padding:2px 10px 4px; border-radius:6px;
  display:inline;
  white-space:nowrap;
  -webkit-box-decoration-break:clone;
  box-decoration-break:clone;
}}
"""


CREATOR_HTML = f'<span style="font-weight:700;color:{DARK};">Nabilah Azman</span><span style="color:{MUTED};font-weight:400;"> &nbsp;&middot;&nbsp; </span><span style="color:{ACCENT};font-weight:600;">The Bell</span>'
CREATOR_LAST = f'<span style="font-weight:700;color:rgba(255,255,255,0.8);">Nabilah Azman</span><span style="color:rgba(255,255,255,0.45);font-weight:400;"> &nbsp;&middot;&nbsp; </span><span style="color:rgba(255,255,255,0.7);font-weight:600;">The Bell</span>'


def cover_html(title: str, subtitle: str, week: int) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
body {{ background:{CREAM}; }}
.wrap {{
  width:{W}px; height:{H}px;
  padding:80px 88px;
  display:flex; flex-direction:column;
}}
.top {{
  display:flex; justify-content:space-between; align-items:center;
}}
.creator {{ font-size:26px; }}
.tag {{ font-size:26px; font-weight:700; color:{ACCENT}; }}
.center {{
  flex:1; display:flex; flex-direction:column; justify-content:center;
}}
.logo-row {{
  display:flex; align-items:flex-end; gap:32px;
  margin-bottom:52px;
}}
.week-badge {{
  font-size:18px; font-weight:700; color:{ACCENT};
  letter-spacing:3px; text-transform:uppercase;
  padding-bottom:6px;
}}
.title {{
  font-size:104px; font-weight:900; color:{DARK};
  line-height:0.98; margin-bottom:40px;
  word-break:break-word;
}}
.subtitle {{
  font-size:30px; font-weight:400; color:{MUTED}; line-height:1.6;
}}
.bottom {{
  display:flex; justify-content:space-between; align-items:center;
}}
.site {{ font-size:22px; font-style:italic; color:{MUTED}; }}
.dot {{ width:18px; height:18px; background:{ACCENT}; border-radius:50%; }}
</style></head><body>
<div class="wrap">
  <div class="top">
    <span class="creator">{CREATOR_HTML}</span>
    <span class="tag">#WEEK{week}</span>
  </div>
  <div class="center">
    <div class="logo-row">
      {BELL_SVG_LG}
      <span class="week-badge">Week {week}</span>
    </div>
    <div class="title">{render_statement(title)}</div>
    <div class="subtitle">{clean_html(subtitle)}</div>
  </div>
  <div class="bottom">
    <span class="site">thebell.newsletter</span>
    <span class="dot"></span>
  </div>
</div>
</body></html>"""


def _font_size(text: str) -> int:
    n = len(text)
    if n < 55:   return 80
    if n < 80:   return 70
    if n < 105:  return 60
    if n < 135:  return 52
    return 44


def slide_html(num: int, total: int, text: str, diagram_svg: str = "") -> str:
    fs = _font_size(text)
    diagram_def = diagram_svg
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
{BASE}
body {{ background:{CREAM}; }}
.wrap {{
  width:{W}px; height:{H}px;
  padding:72px 88px 64px;
  display:flex; flex-direction:column;
}}
.top {{
  display:flex; justify-content:space-between; align-items:center;
  flex-shrink:0;
}}
.creator {{ font-size:26px; }}
.counter {{ font-size:26px; font-weight:700; color:{ACCENT}; }}
.text-area {{ flex:0 0 auto; padding-top:36px; }}
.statement {{
  font-size:{fs}px; font-weight:900; color:{DARK};
  line-height:1.08; word-break:break-word;
}}
.diagram-area {{
  flex:1; display:flex; align-items:flex-start; justify-content:center;
  padding-top:28px;
  min-height:0;
  width:100%;
}}
.bottom {{
  display:flex; justify-content:space-between; align-items:center;
  flex-shrink:0;
}}
.site {{ font-size:22px; font-style:italic; color:{MUTED}; }}
.dot {{ width:18px; height:18px; background:{ACCENT}; border-radius:50%; }}
</style></head><body>
<div class="wrap">
  <div class="top">
    <span class="creator">{CREATOR_HTML}</span>
    <span class="counter">#{num:02d}</span>
  </div>
  <div class="text-area">
    <div class="statement">{render_statement(text)}</div>
  </div>
  <div class="diagram-area">
    {diagram_def}
  </div>
  <div class="bottom">
    <span class="site">thebell.newsletter</span>
    <span class="dot"></span>
  </div>
</div>
</body></html>"""


def last_html(cta: str) -> str:
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
{BASE}
body {{ background:#1A1A2E; }}
.wrap {{
  width:{W}px; height:{H}px;
  padding:80px 88px;
  display:flex; flex-direction:column;
}}
.top {{
  display:flex; justify-content:space-between; align-items:center;
}}
.creator {{ font-size:26px; }}
.tag {{ font-size:26px; font-weight:700; color:{WHITE}; }}
.center {{
  flex:1; display:flex; flex-direction:column; justify-content:center;
}}
.cta {{
  font-size:88px; font-weight:900; color:{WHITE};
  line-height:1.06; word-break:break-word;
}}
.sub {{
  margin-top:40px;
  font-size:28px; font-weight:400; color:rgba(255,255,255,0.6);
  line-height:1.6;
}}
.bottom {{
  display:flex; justify-content:space-between; align-items:center;
}}
.site {{ font-size:22px; font-style:italic; color:rgba(255,255,255,0.45); }}
.dot {{ width:18px; height:18px; background:rgba(255,255,255,0.35); border-radius:50%; }}
</style></head><body>
<div class="wrap">
  <div class="top">
    <span class="creator">{CREATOR_LAST}</span>
    <span class="tag">Follow</span>
  </div>
  <div class="center">
    <div class="cta">{clean_html(cta)}</div>
    <div class="sub">Real posts on building with AI.<br>New every Monday.</div>
  </div>
  <div class="bottom">
    <span class="site">nabilahazman249@gmail.com</span>
    <span class="dot"></span>
  </div>
</div>
</body></html>"""


def render_slides(slides_html):
    from playwright.sync_api import sync_playwright
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        for i, (html, name) in enumerate(slides_html):
            page = browser.new_page(viewport={"width": W, "height": H})
            page.set_content(html, wait_until="load")
            out = SLIDES_DIR / f"{i:02d}_{name}.png"
            page.screenshot(path=str(out))
            paths.append(out)
            page.close()
            print(f"    {i+1}/{len(slides_html)} rendered")
        browser.close()
    return paths


def combine_to_pdf(png_paths, output):
    from PIL import Image
    imgs = [Image.open(p).convert("RGB") for p in png_paths]
    imgs[0].save(str(output), save_all=True, append_images=imgs[1:], resolution=150)


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tools.diagram_selector import assign_diagrams

    data        = json.loads(CAROUSEL_INPUT.read_text())
    week        = data.get("week", 1)
    cover_title = data.get("cover_title", "Week 1")
    cover_sub   = data.get("cover_subtitle", "")
    slides      = data.get("slides", [])
    last_cta    = data.get("last_slide", "Follow for weekly posts on building with AI.")

    diagram_svgs = assign_diagrams(slides)

    all_slides = [(cover_html(cover_title, cover_sub, week), "cover")]
    total = len(slides)
    for i, s in enumerate(slides, 1):
        text = s.get("text") or s.get("title", "")
        all_slides.append((slide_html(i, total, text, diagram_svgs[i - 1]), f"slide{i}"))
    all_slides.append((last_html(last_cta), "last"))

    print(f"  Rendering {len(all_slides)} slides...")
    paths = render_slides(all_slides)
    CAROUSEL_OUTPUT.parent.mkdir(exist_ok=True)
    combine_to_pdf(paths, CAROUSEL_OUTPUT)
    size_kb = round(CAROUSEL_OUTPUT.stat().st_size / 1024, 1)
    print(f"  > {CAROUSEL_OUTPUT} ({len(all_slides)} pages, {size_kb} KB)")


if __name__ == "__main__":
    main()
