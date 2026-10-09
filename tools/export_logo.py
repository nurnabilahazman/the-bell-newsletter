#!/usr/bin/env python3
"""Export The Bell logo in multiple formats for Canva Brand Kit upload."""

from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(".tmp/logo_exports")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Full logo — navy bell + gold crown/clapper + BELL wordmark (for light backgrounds)
LOGO_LIGHT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 280" width="240" height="280">
  <path d="M108 60 L108 32 Q108 16 120 16 Q132 16 132 32 L132 60 Z" fill="#C9A84C"/>
  <path d="M108 60 C72 70 38 108 34 152 C32 174 38 196 54 200
           L186 200 C202 196 208 174 206 152 C202 108 168 70 132 60 Z"
        fill="#1A1A2E"/>
  <circle cx="120" cy="213" r="13" fill="#C9A84C"/>
  <text x="120" y="265" font-family="Georgia,serif" font-size="36" font-weight="700"
        fill="#1A1A2E" text-anchor="middle" letter-spacing="10">BELL</text>
</svg>"""

# 2. Icon only — no wordmark (for small contexts like profile, favicon)
LOGO_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <path d="M88 50 L88 28 Q88 14 100 14 Q112 14 112 28 L112 50 Z" fill="#C9A84C"/>
  <path d="M88 50 C55 58 26 92 22 132 C20 150 26 168 40 172
           L160 172 C174 168 180 150 178 132 C174 92 145 58 112 50 Z"
        fill="#1A1A2E"/>
  <circle cx="100" cy="183" r="10" fill="#C9A84C"/>
</svg>"""

# 3. Reversed — white bell + gold crown/clapper (for dark backgrounds)
LOGO_DARK_BG_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 280" width="240" height="280">
  <path d="M108 60 L108 32 Q108 16 120 16 Q132 16 132 32 L132 60 Z" fill="#C9A84C"/>
  <path d="M108 60 C72 70 38 108 34 152 C32 174 38 196 54 200
           L186 200 C202 196 208 174 206 152 C202 108 168 70 132 60 Z"
        fill="rgba(255,255,255,0.9)"/>
  <circle cx="120" cy="213" r="13" fill="#C9A84C"/>
  <text x="120" y="265" font-family="Georgia,serif" font-size="36" font-weight="700"
        fill="rgba(255,255,255,0.9)" text-anchor="middle" letter-spacing="10">BELL</text>
</svg>"""

logos = [
    ("the_bell_logo_light.svg",   LOGO_LIGHT_SVG,   "white",   800, 930),
    ("the_bell_logo_icon.svg",    LOGO_ICON_SVG,    "white",   600, 600),
    ("the_bell_logo_dark_bg.svg", LOGO_DARK_BG_SVG, "#1A1A2E", 800, 930),
]

# Save raw SVGs
for fname, svg, *_ in logos:
    (OUT_DIR / fname).write_text(svg)
    print(f"  SVG saved: {fname}")

# Export PNGs via Playwright
print("\nExporting PNGs...")
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox"])
    for fname, svg, bg, w, h in logos:
        html = f"""<!DOCTYPE html><html><head><style>
          * {{margin:0;padding:0;}} body {{background:{bg};display:flex;
          align-items:center;justify-content:center;width:{w}px;height:{h}px;}}
        </style></head><body>{svg}</body></html>"""
        page = browser.new_page(viewport={"width": w, "height": h})
        page.set_content(html, wait_until="load")
        png_name = fname.replace(".svg", ".png")
        page.screenshot(path=str(OUT_DIR / png_name), full_page=False)
        page.close()
        print(f"  PNG saved: {png_name}")
    browser.close()

print(f"\nAll logo files saved to: {OUT_DIR.resolve()}")
print("\nUpload to Canva Brand Kit:")
print("  Light backgrounds → the_bell_logo_light.png")
print("  Icon only         → the_bell_logo_icon.png")
print("  Dark backgrounds  → the_bell_logo_dark_bg.png")
