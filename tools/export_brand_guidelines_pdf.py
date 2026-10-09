#!/usr/bin/env python3
"""Convert the_bell_brand_guidelines.md to a styled PDF using Playwright."""

import re
from pathlib import Path

MD_PATH  = Path(".tmp/the_bell_brand_guidelines.md")
PDF_PATH = Path(".tmp/the_bell_brand_guidelines.pdf")

CREAM  = "#F5F0E8"
NAVY   = "#1A1A2E"
GOLD   = "#C9A84C"
MUTED  = "#777777"


def md_to_html(md: str) -> str:
    """Minimal markdown → HTML converter for this specific document."""
    lines = md.split("\n")
    html_lines = []
    in_table = False
    in_code = False
    in_list = False

    for line in lines:
        # Code block
        if line.strip().startswith("```"):
            if not in_code:
                html_lines.append('<pre><code>')
                in_code = True
            else:
                html_lines.append('</code></pre>')
                in_code = False
            continue
        if in_code:
            html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Table
        if line.startswith("|"):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            if re.match(r'\|[-| ]+\|', line):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            is_header = not any(html_lines[-1:]) or html_lines and '<table>' in html_lines[-1]
            tag = "th" if html_lines and html_lines[-1] == "<table>" else "td"
            row = "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False

        # Headings
        if line.startswith("# "):
            html_lines.append(f'<h1>{inline(line[2:])}</h1>')
        elif line.startswith("## "):
            html_lines.append(f'<h2>{inline(line[3:])}</h2>')
        elif line.startswith("### "):
            html_lines.append(f'<h3>{inline(line[4:])}</h3>')
        # HR
        elif line.startswith("---"):
            html_lines.append("<hr/>")
        # List item
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline(line[2:])}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if line.strip() == "":
                html_lines.append("<br/>")
            else:
                html_lines.append(f"<p>{inline(line)}</p>")

    if in_table:
        html_lines.append("</table>")
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def inline(text: str) -> str:
    """Handle bold, italic, inline code, backtick hex codes."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    return text


def build_full_html(body: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: {CREAM};
    color: {NAVY};
    padding: 64px 80px;
    font-size: 15px;
    line-height: 1.7;
    max-width: 860px;
    margin: 0 auto;
  }}
  h1 {{
    font-size: 36px;
    font-weight: 900;
    color: {NAVY};
    margin-bottom: 6px;
    margin-top: 48px;
    border-bottom: 4px solid {GOLD};
    padding-bottom: 10px;
  }}
  h1:first-of-type {{ margin-top: 0; }}
  h2 {{
    font-size: 22px;
    font-weight: 700;
    color: {NAVY};
    margin-top: 40px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-left: 4px solid {GOLD};
    padding-left: 14px;
  }}
  h3 {{
    font-size: 17px;
    font-weight: 700;
    color: {NAVY};
    margin-top: 24px;
    margin-bottom: 8px;
  }}
  p {{
    margin-bottom: 10px;
    color: {NAVY};
  }}
  strong {{ font-weight: 700; }}
  em {{ font-style: italic; color: {MUTED}; }}
  code {{
    background: {NAVY};
    color: {GOLD};
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 13px;
    font-family: 'Courier New', monospace;
  }}
  pre {{
    background: {NAVY};
    color: #f0ece3;
    padding: 24px 28px;
    border-radius: 10px;
    margin: 20px 0;
    font-size: 13px;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  pre code {{
    background: none;
    color: #f0ece3;
    padding: 0;
    border-radius: 0;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 24px;
    font-size: 14px;
  }}
  th {{
    background: {NAVY};
    color: #fff;
    font-weight: 700;
    padding: 10px 14px;
    text-align: left;
  }}
  td {{
    padding: 9px 14px;
    border-bottom: 1px solid #e0dbd0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{ background: rgba(26,26,46,0.04); }}
  ul {{
    padding-left: 24px;
    margin-bottom: 12px;
  }}
  li {{
    margin-bottom: 6px;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e0dbd0;
    margin: 32px 0;
  }}
  br {{ display: block; margin: 6px 0; content: ""; }}
  .gold {{ color: {GOLD}; font-weight: 700; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    from playwright.sync_api import sync_playwright

    md = MD_PATH.read_text()
    body = md_to_html(md)
    html = build_full_html(body)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=str(PDF_PATH),
            format="A4",
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            print_background=True,
        )
        browser.close()

    size_kb = round(PDF_PATH.stat().st_size / 1024, 1)
    print(f"  → {PDF_PATH} ({size_kb} KB)")


if __name__ == "__main__":
    main()
