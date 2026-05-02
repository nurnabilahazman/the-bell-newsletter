#!/usr/bin/env python3
"""
Generates The Bell weekly newsletter — 4 sections, all prompts included.
Reads: config/curriculum.json, config/saas_progress.json, .tmp/product_research.json
Saves: .tmp/draft.md
Usage: python tools/draft_newsletter.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CURRICULUM_PATH      = Path("config/curriculum.json")
SAAS_PATH            = Path("config/saas_progress.json")
RESEARCH_PATH        = Path(".tmp/product_research.json")
OUTPUT_PATH          = Path(".tmp/draft.md")
CHILDREN_DATA_PATH     = Path(".tmp/children_brief_data.json")
PRODUCTIVITY_DATA_PATH = Path(".tmp/productivity_brief_data.json")
LANGUAGE_DATA_PATH     = Path(".tmp/language_brief_data.json")

MODEL = "llama-3.3-70b-versatile"


# ── loaders ────────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def get_section1(curriculum: dict) -> dict:
    week_num = curriculum.get("current_week", 1)
    projects = curriculum.get("projects", [])
    project  = next((p for p in projects if p["week"] == week_num), {})
    return {
        "week_num":    week_num,
        "total_weeks": len(projects),
        "title":       project.get("title", ""),
        "skill":       project.get("skill", ""),
        "prompt":      project.get("build_prompt", ""),
        "status":      project.get("status", "upcoming")
    }


def get_section3(saas: dict) -> dict:
    week_num   = saas.get("current_week", 1)
    milestones = saas.get("milestones", [])
    current    = next((m for m in milestones if m["week"] == week_num), {})
    return {
        "app_name":  saas.get("app_name", ""),
        "tagline":   saas.get("tagline", ""),
        "phase":     current.get("phase", ""),
        "task":      current.get("task", ""),
        "prompt":    current.get("task_prompt", ""),
        "week_num":  week_num,
        "total":     len(milestones)
    }


# ── groq call for section 2 (products) + section 4 (tips) ─────────────────────

def generate_dynamic_sections(client: Groq, research: dict, children_topic: str = "") -> str:
    themes_text = ""
    for t in research.get("themes", []):
        research_snippets = "\n".join(
            f"  - [{r['title']}]({r['url']}): {r['content'][:300]}"
            for r in t.get("research", [])[:4]
        )
        themes_text += f"""
THEME: {t['theme_name']}
Description: {t['description']}
Format: {t['format']}
Price range: {t['price_range']}
Research findings:
{research_snippets}
"""

    children_override = (
        f"SPECIAL INSTRUCTION: For the 'children' theme, this week's assigned topic is '{children_topic}'. "
        f"Build every field (PRODUCT, STORE_INSPO, BUYERS_LOVE, YOUR_EDGE, PROMPT) specifically around '{children_topic}'. "
        "Do not substitute a different children's product."
    ) if children_topic else ""

    prompt = f"""You are writing two sections of The Bell — a weekly newsletter for someone building and selling digital products. They have zero design experience and use AI to create everything.

PRODUCT RESEARCH DATA:
{themes_text}

Generate EXACTLY the following. Follow the format precisely — it will be parsed by code.

---

SECTION2_START

THEME_START: productivity
PRODUCT: [specific product name, e.g. "Paycheck-to-Paycheck Budget Tracker"]
STORE_INSPO: [store name or product title] — [1 sentence on what makes it sell well] — URL: [use a real URL from the research data above, pick the most relevant Etsy/Gumroad/product link]
BUYERS_LOVE: [thing 1] | [thing 2] | [thing 3]
YOUR_EDGE: [specific improvement 1] | [specific improvement 2] | [specific improvement 3]
PROMPT_START
[Write a detailed Claude creation prompt — minimum 200 words. Tell Claude exactly what to create: the full content/structure of the product, every tab/sheet/section if it's a spreadsheet, every page if it's a printable PDF, formulas, colour scheme using Bell colours (navy #1A1A2E, gold #C9A84C), what makes it look professional, how to make it immediately usable. The person will paste this directly into Claude to create the product.]
PROMPT_END
THEME_END

THEME_START: language
PRODUCT: [specific product]
STORE_INSPO: [store] — [what works]
BUYERS_LOVE: [thing 1] | [thing 2] | [thing 3]
YOUR_EDGE: [improvement 1] | [improvement 2] | [improvement 3]
PROMPT_START
[Detailed creation prompt — minimum 200 words. Same level of detail as above. For language products: specify exactly which language, what level (beginner/intermediate), what content to include on each page, layout instructions, font suggestions for the target language characters if applicable.]
PROMPT_END
THEME_END

THEME_START: children
PRODUCT: [specific product]
STORE_INSPO: [store] — [what works]
BUYERS_LOVE: [thing 1] | [thing 2] | [thing 3]
YOUR_EDGE: [improvement 1] | [improvement 2] | [improvement 3]
PROMPT_START
[Detailed creation prompt — minimum 200 words. For children's products: specify age range, reading level, activity type, how many pages, what goes on each page, colour scheme, font size, safety/simplicity considerations.]
PROMPT_END
THEME_END

SECTION2_END

---

SECTION4_START
TIP1_TITLE: [short title]
TIP1_BODY: [1-2 specific, actionable sentences about product quality — something concrete they can do today]
TIP2_TITLE: [short title]
TIP2_BODY: [1-2 specific, actionable sentences about pricing or listing optimisation]
TIP3_TITLE: [short title]
TIP3_BODY: [1-2 specific, actionable sentences about getting first sales or visibility]
SECTION4_END

{children_override}
Rules:
- Be specific. Real product names, real price points ($3–$18), real strategies.
- Creation prompts must be detailed enough for someone with zero design skills.
- Tips must be immediately actionable — not "consider diversifying" but "add a preview image showing the product filled in with sample data."
- Never use: "highlights the importance of", "it's essential", "navigate", "landscape".
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
    )
    return response.choices[0].message.content


# ── parsers ────────────────────────────────────────────────────────────────────

def parse_theme_block(block: str) -> dict:
    def extract(tag: str) -> str:
        start = f"{tag}:"
        for line in block.splitlines():
            if line.strip().startswith(start):
                return line.split(":", 1)[1].strip()
        return ""

    def extract_prompt(text: str) -> str:
        if "PROMPT_START" in text and "PROMPT_END" in text:
            return text.split("PROMPT_START", 1)[1].split("PROMPT_END", 1)[0].strip()
        return ""

    return {
        "product":     extract("PRODUCT"),
        "store_inspo": extract("STORE_INSPO"),
        "buyers_love": [x.strip() for x in extract("BUYERS_LOVE").split("|")],
        "your_edge":   [x.strip() for x in extract("YOUR_EDGE").split("|")],
        "prompt":      extract_prompt(block)
    }


def parse_dynamic(raw: str) -> tuple[list, dict]:
    themes = []
    tips   = {}

    # Parse themes
    theme_icons = {"productivity": "🗂️", "language": "📚", "children": "👶"}
    theme_names = {
        "productivity": "Productivity & Trackers",
        "language":     "Language Learning",
        "children":     "Children's Activities"
    }
    for theme_id in ["productivity", "language", "children"]:
        marker_start = f"THEME_START: {theme_id}"
        marker_end   = "THEME_END"
        if marker_start in raw:
            block = raw.split(marker_start, 1)[1].split(marker_end, 1)[0]
            data  = parse_theme_block(block)
            data["id"]   = theme_id
            data["icon"] = theme_icons[theme_id]
            data["name"] = theme_names[theme_id]
            themes.append(data)

    # Parse tips
    def extract_tip(n: int, key: str) -> str:
        tag = f"TIP{n}_{key}:"
        for line in raw.splitlines():
            if line.strip().startswith(tag):
                return line.split(":", 1)[1].strip()
        return ""

    tips = {
        "tip1": {"title": extract_tip(1, "TITLE"), "body": extract_tip(1, "BODY")},
        "tip2": {"title": extract_tip(2, "TITLE"), "body": extract_tip(2, "BODY")},
        "tip3": {"title": extract_tip(3, "TITLE"), "body": extract_tip(3, "BODY")},
    }

    return themes, tips


# ── assemble draft ─────────────────────────────────────────────────────────────

def assemble_draft(s1: dict, themes: list, s3: dict, tips: dict, today: str, children_data: dict = None, productivity_data: dict = None, language_data: dict = None) -> str:
    lines = []

    # Title
    lines.append(f"# The Bell — Week {s1['week_num']} · {today}")
    lines.append("")
    lines.append(">>>TAGLINE")
    lines.append("Build. Ship. Earn.")
    lines.append(">>>END")
    lines.append("")

    # ── Section 1 ──────────────────────────────────────────────────────────────
    lines.append("## 🛠️ SECTION 1 — Project of the Week")
    lines.append("")
    lines.append(f"**Week {s1['week_num']} of {s1['total_weeks']}: {s1['title']}**")
    lines.append("")

    skill_short = s1['skill'].split("—")[0].strip() if "—" in s1['skill'] else s1['skill']
    lines.append(f"*{skill_short}*")
    lines.append("")

    if s1['status'] == 'completed':
        lines.append("✅ **Already built** — but the prompt is below if you want to revisit or rebuild it.")
    else:
        lines.append("Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.")
    lines.append("")
    lines.append(">>>PROMPT")
    lines.append(s1['prompt'])
    lines.append(">>>END")
    lines.append("")
    lines.append(">>>DOC")
    lines.append("https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section1_projects_guide.md")
    lines.append("How to work with Claude on projects, common errors, and the 12-week learning arc.")
    lines.append(">>>END")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 2 ──────────────────────────────────────────────────────────────
    lines.append("## 📦 SECTION 2 — 3 Products to Build This Week")
    lines.append("")
    lines.append("One product per theme. Research done. Prompt ready. Just paste and create.")
    lines.append("")

    for theme in themes:
        lines.append(f"### {theme['icon']} {theme['name']}")
        lines.append("")
        lines.append(f"**This week's product:** {theme['product']}")
        lines.append("")
        # Split store_inspo into text and URL if present
        inspo_text = theme['store_inspo']
        inspo_url  = ""
        if "URL:" in inspo_text:
            parts      = inspo_text.split("URL:", 1)
            inspo_text = parts[0].strip().rstrip("—").strip()
            inspo_url  = parts[1].strip()

        if inspo_url:
            lines.append(f"**Store inspiration:** [{inspo_text}]({inspo_url})")
        else:
            lines.append(f"**Store inspiration:** {inspo_text}")
        lines.append("")
        lines.append("**What buyers love:**")
        for item in theme['buyers_love']:
            if item:
                lines.append(f"- {item}")
        lines.append("")
        lines.append("**Your edge — make it better:**")
        for item in theme['your_edge']:
            if item:
                lines.append(f"- {item}")
        lines.append("")
        brief_data = None
        if theme["id"] == "children" and children_data:
            brief_data = children_data
        elif theme["id"] == "productivity" and productivity_data:
            brief_data = productivity_data
        elif theme["id"] == "language" and language_data:
            brief_data = language_data

        if brief_data:
            build_steps = brief_data.get("build_steps", [])
            price       = brief_data.get("price", "")
            etsy_title  = brief_data.get("etsy_title", "")
            etsy_tags   = ", ".join(brief_data.get("etsy_tags", []))
            brief_url   = brief_data.get("brief_url", "")
            if build_steps:
                lines.append("**How to build it in Canva:**")
                for i, step in enumerate(build_steps, 1):
                    lines.append(f"{i}. {step}")
                lines.append("")
            if price or etsy_title:
                lines.append(f"**Launch price:** {price}")
                if etsy_title:
                    lines.append(f"**Etsy title:** {etsy_title}")
                if etsy_tags:
                    lines.append(f"**Tags:** {etsy_tags}")
                lines.append("")
            if brief_url:
                lines.append(f"[📋 View this week's full brief →]({brief_url})")
                lines.append("")
        else:
            lines.append(">>>PROMPT")
            lines.append(theme['prompt'])
            lines.append(">>>END")
            lines.append("")

    lines.append("---")
    lines.append("")

    # ── Section 3 ──────────────────────────────────────────────────────────────
    lines.append(f"## 🚀 SECTION 3 — SaaS: {s3['app_name']}")
    lines.append("")
    lines.append(f"*{s3['tagline']}*")
    lines.append("")
    lines.append(f"**Phase:** {s3['phase']} · Week {s3['week_num']} of {s3['total']}")
    lines.append("")
    lines.append(f"**This week's task:** {s3['task']}")
    lines.append("")

    if s3['prompt']:
        lines.append("Paste this into Claude to execute the task:")
        lines.append("")
        lines.append(">>>PROMPT")
        lines.append(s3['prompt'])
        lines.append(">>>END")

    lines.append("")
    lines.append(">>>DOC")
    lines.append("https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md")
    lines.append("Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.")
    lines.append(">>>END")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Section 4 ──────────────────────────────────────────────────────────────
    lines.append("## ⚡ SECTION 4 — Quick Wins This Week")
    lines.append("")

    for i, key in enumerate(["tip1", "tip2", "tip3"], 1):
        t = tips.get(key, {})
        if t.get("title") and t.get("body"):
            lines.append(f"**{i}. {t['title']}** — {t['body']}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append('*The Bell drops every week. Reply "unsubscribe" to leave.*')

    return "\n".join(lines)


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    curriculum        = load_json(CURRICULUM_PATH)
    saas              = load_json(SAAS_PATH)
    research          = load_json(RESEARCH_PATH)
    children_data     = load_json(CHILDREN_DATA_PATH)
    productivity_data = load_json(PRODUCTIVITY_DATA_PATH)
    language_data     = load_json(LANGUAGE_DATA_PATH)

    if not curriculum:
        print("ERROR: config/curriculum.json not found.")
        raise SystemExit(1)

    children_topic = children_data.get("topic", "")
    if children_topic:
        print(f"Children's topic (Week {children_data.get('week_num', '?')}): {children_topic}")
    else:
        print("No children's topic found — run children_brief_generator.py first for a specific topic.")

    productivity_topic = productivity_data.get("topic", "")
    if productivity_topic:
        print(f"Productivity topic (Week {productivity_data.get('week_num', '?')}): {productivity_topic}")
    else:
        print("No productivity topic found — run productivity_brief_generator.py first.")

    language_topic = language_data.get("topic", "")
    if language_topic:
        print(f"Language topic (Week {language_data.get('week_num', '?')}): {language_topic}")
    else:
        print("No language topic found — run language_brief_generator.py first.")

    today = datetime.now().strftime("%B %d, %Y")
    s1    = get_section1(curriculum)
    s3    = get_section3(saas)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if not research:
        print("WARNING: No product research found. Run research_products.py first.")
        print("         Generating newsletter without Section 2 product details...")
        themes = []
        tips   = {}
    else:
        print("Generating product recommendations and tips with Groq...")
        raw_dynamic    = generate_dynamic_sections(client, research, children_topic)
        themes, tips   = parse_dynamic(raw_dynamic)
        print(f"  → {len(themes)} products generated")

    print("Assembling newsletter...")
    draft = assemble_draft(s1, themes, s3, tips, today, children_data, productivity_data, language_data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(draft)

    word_count = len(draft.split())
    print(f"Draft saved to {OUTPUT_PATH} ({word_count} words)")


if __name__ == "__main__":
    main()
