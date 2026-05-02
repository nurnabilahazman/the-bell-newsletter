#!/usr/bin/env python3
"""
Converts .tmp/draft.md into a branded Bell HTML email.
Handles >>>PROMPT blocks, section headers, and Bell styling.
Saves to .tmp/formatted_email.html.
Usage: python tools/format_email.py
"""

import re
from pathlib import Path

DRAFT_PATH  = Path(".tmp/draft.md")
OUTPUT_PATH = Path(".tmp/formatted_email.html")

CSS = """
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background-color: #f4f4f4; font-family: Georgia, serif; }
  .wrapper { max-width: 620px; margin: 30px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }

  /* Header */
  .header { background-color: #1a1a2e; padding: 28px 36px; }
  .header-brand { color: #C9A84C; font-size: 26px; font-weight: bold; letter-spacing: 6px; margin: 0; }
  .header-tagline { color: #a0a8c0; font-size: 12px; margin: 4px 0 0; letter-spacing: 3px; }
  .header-week { color: #e0e0e0; font-size: 13px; margin: 10px 0 0; }

  /* Section blocks */
  .section { padding: 28px 36px 8px; border-bottom: 1px solid #f0f0f5; }
  .section:last-of-type { border-bottom: none; }
  .section-label {
    display: inline-block; background: #1a1a2e; color: #C9A84C;
    font-family: Arial, sans-serif; font-size: 10px; font-weight: bold;
    letter-spacing: 2px; padding: 4px 12px; border-radius: 3px; margin-bottom: 16px;
  }
  .section h2 {
    color: #1a1a2e; font-size: 20px; font-weight: bold;
    margin: 0 0 6px; padding: 0; border: none;
  }
  .section-intro { color: #666; font-size: 14px; font-family: Arial, sans-serif; margin: 0 0 20px; }

  /* Theme sub-headers inside section 2 */
  .theme-header { color: #1a1a2e; font-size: 16px; font-weight: bold; margin: 24px 0 4px; }
  .theme-product { font-size: 15px; color: #222; margin: 0 0 12px; }
  .theme-meta { font-family: Arial, sans-serif; font-size: 13px; color: #555; margin: 0 0 6px; }
  .theme-meta strong { color: #1a1a2e; }

  /* Body text */
  .body-text { color: #222222; font-size: 15px; line-height: 1.75; margin: 0 0 14px; }
  ul { padding-left: 20px; margin: 4px 0 14px; }
  li { color: #333; font-size: 14px; line-height: 1.6; margin-bottom: 6px; }
  a { color: #0055aa; text-decoration: none; }
  a:hover { text-decoration: underline; }
  strong { color: #111; }
  em { color: #555; }

  /* Prompt box */
  .prompt-box {
    background: #f7f7fb; border-left: 4px solid #C9A84C;
    border-radius: 0 6px 6px 0; padding: 16px 20px; margin: 16px 0 24px;
  }
  .prompt-label {
    font-family: Arial, sans-serif; font-size: 10px; font-weight: bold;
    color: #C9A84C; letter-spacing: 2px; margin-bottom: 10px;
  }
  .prompt-content {
    font-family: 'Courier New', Courier, monospace; font-size: 12.5px;
    color: #2a2a3a; line-height: 1.65; white-space: pre-wrap; word-break: break-word;
  }

  /* Tagline banner */
  .tagline-bar {
    background: #1a1a2e; color: #C9A84C; text-align: center;
    font-family: Arial, sans-serif; font-size: 11px; font-weight: bold;
    letter-spacing: 4px; padding: 8px;
  }

  /* Doc reference box */
  .doc-box {
    background: #fffdf0; border-left: 4px solid #1a1a2e;
    border-radius: 0 6px 6px 0; padding: 12px 16px; margin: 16px 0 20px;
    display: flex; align-items: flex-start; gap: 10px;
  }
  .doc-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
  .doc-text { font-family: Arial, sans-serif; font-size: 13px; color: #333; }
  .doc-text strong { color: #1a1a2e; display: block; margin-bottom: 2px; }
  .doc-text a { color: #1a1a2e; text-decoration: underline; font-size: 12px; }
  .doc-text span { color: #666; font-size: 12px; }

  /* Tips section */
  .tip { margin-bottom: 14px; font-size: 15px; line-height: 1.7; }
  .tip-num { color: #C9A84C; font-weight: bold; font-family: Arial, sans-serif; }

  /* Divider */
  .divider { border: none; border-top: 1px solid #ebebf5; margin: 4px 0; }

  /* Footer */
  .footer {
    background: #f8f8fc; padding: 20px 36px; text-align: center;
    font-family: Arial, sans-serif; font-size: 12px; color: #999;
    border-top: 1px solid #e8e8f0;
  }
"""

SECTION_LABELS = {
    "🛠️": "SECTION 1 — PROJECT",
    "📦": "SECTION 2 — PRODUCTS",
    "🚀": "SECTION 3 — SAAS",
    "⚡": "SECTION 4 — QUICK WINS",
}


def inline_md(text: str) -> str:
    # Save links first so underscores inside URLs aren't treated as italic markers
    saved, slots = [], []
    def _save(m):
        idx = len(saved)
        saved.append(f'<a href="{m.group(2)}">{m.group(1)}</a>')
        slots.append(f"\x00LINK{idx}\x00")
        return slots[-1]
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _save, text)
    # Apply bold/italic on text that no longer contains link URLs
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_',       r'<em>\1</em>', text)
    # Restore links
    for slot, link in zip(slots, saved):
        text = text.replace(slot, link)
    return text


def parse_draft(md: str) -> tuple[str, str, list]:
    """
    Returns (subject, tagline, sections)
    sections = list of dicts: {label, html}
    """
    subject  = "The Bell — Weekly Newsletter"
    tagline  = "Build. Ship. Earn."
    sections = []

    # Split into blocks by top-level section markers
    lines = md.split("\n")
    current_section_label = ""
    current_lines         = []
    in_prompt             = False
    prompt_lines          = []

    def flush_section():
        nonlocal current_section_label, current_lines
        if current_lines:
            html = render_section_lines(current_lines)
            sections.append({"label": current_section_label, "html": html})
        current_section_label = ""
        current_lines         = []

    for line in lines:

        # Title
        if line.startswith("# "):
            subject = line[2:].strip()
            continue

        # Tagline block
        if line.strip() == ">>>TAGLINE":
            continue
        if line.strip() == ">>>END" and not in_prompt:
            continue

        # Prompt start
        if line.strip() == ">>>PROMPT":
            in_prompt    = True
            prompt_lines = []
            continue

        # Doc reference start
        if line.strip() == ">>>DOC":
            in_prompt    = True   # reuse the same flag, different tag
            prompt_lines = ["__DOC__"]
            continue

        # Prompt/Doc end
        if line.strip() == ">>>END" and in_prompt:
            in_prompt = False
            if prompt_lines and prompt_lines[0] == "__DOC__":
                # DOC block: lines[1]=filepath, lines[2]=description
                doc_path = prompt_lines[1] if len(prompt_lines) > 1 else ""
                doc_desc = prompt_lines[2] if len(prompt_lines) > 2 else ""
                current_lines.append(("DOC", f"{doc_path}||{doc_desc}"))
            else:
                prompt_text = "\n".join(prompt_lines)
                current_lines.append(("PROMPT", prompt_text))
            continue

        if in_prompt:
            prompt_lines.append(line)
            continue

        # Section 2 heading (## 🛠️ / ## 📦 / etc.)
        if line.startswith("## "):
            flush_section()
            text  = line[3:].strip()
            label = next((v for k, v in SECTION_LABELS.items() if k in text), text)
            current_section_label = label
            current_lines.append(("H2", text))
            continue

        # H3
        if line.startswith("### "):
            current_lines.append(("H3", line[4:].strip()))
            continue

        # HR
        if line.strip() in ("---", "***", "___"):
            current_lines.append(("HR", ""))
            continue

        # Bullet
        if line.startswith("- ") or line.startswith("* "):
            current_lines.append(("LI", line[2:].strip()))
            continue

        # Numbered list
        if re.match(r'^\d+\. ', line):
            content = re.sub(r'^\d+\. ', '', line).strip()
            current_lines.append(("NUM", content))
            continue

        # Empty
        if not line.strip():
            current_lines.append(("BLANK", ""))
            continue

        # Regular text
        current_lines.append(("P", line.strip()))

    flush_section()
    return subject, tagline, sections


def render_section_lines(token_list: list) -> str:
    html_parts = []
    in_ul      = False
    in_ol      = False

    def close_list():
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    for kind, content in token_list:
        if kind == "H2":
            close_list()
            # Strip leading emoji for display
            display = re.sub(r'^[\U0001F300-\U0001FFFF☀-⛿✀-➿]+\s*', '', content)
            display = re.sub(r'^(SECTION \d+ — )', '', display)
            html_parts.append(f'<h2 style="color:#1a1a2e;font-size:20px;margin:0 0 6px;border:none;">{inline_md(display)}</h2>')

        elif kind == "H3":
            close_list()
            html_parts.append(f'<p class="theme-header">{inline_md(content)}</p>')

        elif kind == "P":
            close_list()
            # Italic-only lines (skill description)
            if content.startswith("*") and content.endswith("*") and not content.startswith("**"):
                html_parts.append(f'<p class="section-intro">{inline_md(content)}</p>')
            else:
                html_parts.append(f'<p class="body-text">{inline_md(content)}</p>')

        elif kind == "LI":
            if not in_ul:
                close_list()
                html_parts.append('<ul>')
                in_ul = True
            html_parts.append(f'<li>{inline_md(content)}</li>')

        elif kind == "NUM":
            close_list()
            # Tips numbered items
            m = re.match(r'\*\*(.+?)\*\*\s*—\s*(.*)', content)
            if m:
                html_parts.append(
                    f'<p class="tip"><span class="tip-num">→</span> '
                    f'<strong>{m.group(1)}</strong> — {inline_md(m.group(2))}</p>'
                )
            else:
                html_parts.append(f'<p class="body-text">{inline_md(content)}</p>')

        elif kind == "PROMPT":
            close_list()
            safe = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(
                f'<div class="prompt-box">'
                f'<div class="prompt-label">📋 COPY THIS PROMPT INTO CLAUDE</div>'
                f'<div class="prompt-content">{safe}</div>'
                f'</div>'
            )

        elif kind == "DOC":
            close_list()
            parts    = content.split("||", 1)
            doc_path = parts[0].strip()
            doc_desc = parts[1].strip() if len(parts) > 1 else ""
            doc_name = doc_path.split("/")[-1]
            html_parts.append(
                f'<div class="doc-box">'
                f'<div class="doc-icon">📄</div>'
                f'<div class="doc-text">'
                f'<strong>Reference Document</strong>'
                f'<a href="{doc_path}">{doc_name}</a><br>'
                f'<span>{doc_desc}</span>'
                f'</div></div>'
            )

        elif kind == "HR":
            close_list()
            html_parts.append('<hr class="divider">')

        elif kind == "BLANK":
            pass  # skip blank lines

    close_list()
    return "\n".join(html_parts)


def build_html(subject: str, tagline: str, sections: list) -> str:
    week_match = re.search(r'Week (\d+)', subject)
    week_label = f"Week {week_match.group(1)}" if week_match else ""

    sections_html = ""
    for sec in sections:
        if not sec["html"].strip():
            continue
        label_html = (
            f'<div class="section-label">{sec["label"]}</div>' if sec["label"] else ""
        )
        sections_html += f'<div class="section">{label_html}{sec["html"]}</div>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="wrapper">

    <div class="header">
      <p class="header-brand">BELL</p>
      <p class="header-tagline">NEWSLETTER</p>
      <p class="header-week">{subject}</p>
    </div>

    <div class="tagline-bar">{tagline}</div>

    {sections_html}

    <div class="footer">
      The Bell — Weekly newsletter for builders.<br>
      Reply <strong>"unsubscribe"</strong> to leave.
    </div>

  </div>
</body>
</html>"""


def main():
    if not DRAFT_PATH.exists():
        print(f"ERROR: {DRAFT_PATH} not found. Run draft_newsletter.py first.")
        raise SystemExit(1)

    with open(DRAFT_PATH) as f:
        md = f.read()

    subject, tagline, sections = parse_draft(md)
    html = build_html(subject, tagline, sections)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(html)

    print(f"Subject : {subject}")
    print(f"Sections: {len(sections)}")
    print(f"HTML saved to {OUTPUT_PATH} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
