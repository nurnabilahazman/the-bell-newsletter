#!/usr/bin/env python3
"""
Children's Activities Weekly Brief Generator

Picks the next unused topic from a list of 52, generates a one-page
HTML brief for it, and writes topic data to .tmp/children_brief_data.json
so that draft_newsletter.py can use the topic in the children's section.

Run this FIRST, before draft_newsletter.py:
  python tools/children_brief_generator.py

No-repeat tracking: config/children_topics_log.json
Weekly brief output: .tmp/unified_product_brief.html
Newsletter data:     .tmp/children_brief_data.json
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

LOG_PATH    = Path("config/children_topics_log.json")
BRIEF_PATH  = Path(".tmp/unified_product_brief.html")
DOCS_PATH   = Path("docs/current_brief.html")   # committed to repo → accessible via GitHub
DATA_PATH   = Path(".tmp/children_brief_data.json")
MODEL       = "llama-3.3-70b-versatile"
BRIEF_URL   = "https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_brief.html"

# 52 topics — one per week for a full year, then auto-resets
ALL_TOPICS = [
    {"topic": "Alphabet Tracing Workbook",         "age": "3–5", "format": "PDF printable"},
    {"topic": "Number Tracing Workbook",            "age": "3–5", "format": "PDF printable"},
    {"topic": "Ocean Explorer Busy Book",           "age": "2–4", "format": "PDF activity pack"},
    {"topic": "Preschool Activity Binder",          "age": "3–5", "format": "PDF binder set"},
    {"topic": "Color and Shape Flashcards",         "age": "2–4", "format": "PDF flashcards"},
    {"topic": "Sight Word Flashcards",              "age": "4–7", "format": "PDF flashcards"},
    {"topic": "Scissor Skills Practice Sheets",     "age": "3–5", "format": "PDF printable"},
    {"topic": "Farm Animals Coloring Pages",        "age": "2–5", "format": "PDF coloring"},
    {"topic": "Safari Animals Coloring Pages",      "age": "2–5", "format": "PDF coloring"},
    {"topic": "Morning Routine Chart",              "age": "2–6", "format": "PDF poster"},
    {"topic": "Reward and Behavior Chart",          "age": "3–8", "format": "PDF printable"},
    {"topic": "Emotions and Feelings Flashcards",   "age": "2–5", "format": "PDF flashcards"},
    {"topic": "Bilingual Alphabet Flashcards",      "age": "2–5", "format": "PDF flashcards"},
    {"topic": "Letter Recognition Bingo",           "age": "4–6", "format": "PDF game"},
    {"topic": "Numbers 1–20 Activity Worksheets",   "age": "3–5", "format": "PDF worksheets"},
    {"topic": "Pre-Writing Practice Sheets",        "age": "3–5", "format": "PDF printable"},
    {"topic": "Pattern Recognition Worksheets",     "age": "3–5", "format": "PDF worksheets"},
    {"topic": "Counting and Sorting Activities",    "age": "2–4", "format": "PDF activity pack"},
    {"topic": "Rhyming Words Flashcards",           "age": "4–6", "format": "PDF flashcards"},
    {"topic": "Opposites Flashcards",               "age": "2–4", "format": "PDF flashcards"},
    {"topic": "Weather Learning Pack",              "age": "3–6", "format": "PDF activity pack"},
    {"topic": "Seasons Activity Worksheets",        "age": "3–5", "format": "PDF worksheets"},
    {"topic": "Solar System Coloring Book",         "age": "4–7", "format": "PDF coloring"},
    {"topic": "Ocean Animals Activity Pack",        "age": "3–6", "format": "PDF activity pack"},
    {"topic": "Dinosaur Activity Workbook",         "age": "4–7", "format": "PDF workbook"},
    {"topic": "Body Parts Flashcards",              "age": "2–4", "format": "PDF flashcards"},
    {"topic": "Healthy Foods Sorting Cards",        "age": "2–5", "format": "PDF game"},
    {"topic": "Community Helpers Learning Pack",    "age": "3–6", "format": "PDF activity pack"},
    {"topic": "Vehicles and Transport Worksheets",  "age": "2–5", "format": "PDF worksheets"},
    {"topic": "Dot-to-Dot Activity Sheets",         "age": "4–7", "format": "PDF activity"},
    {"topic": "Hidden Pictures Activity Book",      "age": "4–7", "format": "PDF activity"},
    {"topic": "Maze Activity Book for Kids",        "age": "4–7", "format": "PDF activity"},
    {"topic": "Word Search for Kids",               "age": "5–8", "format": "PDF activity"},
    {"topic": "Simple Addition Worksheets",         "age": "5–7", "format": "PDF worksheets"},
    {"topic": "Simple Subtraction Worksheets",      "age": "5–7", "format": "PDF worksheets"},
    {"topic": "Money Counting Worksheets",          "age": "5–8", "format": "PDF worksheets"},
    {"topic": "Time-Telling Practice Sheets",       "age": "5–7", "format": "PDF worksheets"},
    {"topic": "Kindergarten Readiness Workbook",    "age": "4–5", "format": "PDF workbook"},
    {"topic": "Writing Prompts for Kids",           "age": "5–8", "format": "PDF printable"},
    {"topic": "Phonics Practice Sheets",            "age": "4–6", "format": "PDF worksheets"},
    {"topic": "CVC Words Flashcards",               "age": "4–6", "format": "PDF flashcards"},
    {"topic": "Blending Sounds Worksheets",         "age": "4–6", "format": "PDF worksheets"},
    {"topic": "Holiday Activity Pack – Christmas",  "age": "2–8", "format": "PDF activity pack"},
    {"topic": "Holiday Activity Pack – Halloween",  "age": "2–8", "format": "PDF activity pack"},
    {"topic": "Holiday Activity Pack – Easter",     "age": "2–8", "format": "PDF activity pack"},
    {"topic": "Back to School Activity Pack",       "age": "3–6", "format": "PDF activity pack"},
    {"topic": "Nature Scavenger Hunt Printable",    "age": "3–7", "format": "PDF printable"},
    {"topic": "Kids Weekly Meal Planner",           "age": "3–8", "format": "PDF printable"},
    {"topic": "Chore Chart for Kids",               "age": "4–8", "format": "PDF printable"},
    {"topic": "Reading Log for Kids",               "age": "5–8", "format": "PDF printable"},
    {"topic": "Insect Learning Pack",               "age": "3–6", "format": "PDF activity pack"},
    {"topic": "Multiplication Flashcards 1–5",      "age": "6–8", "format": "PDF flashcards"},
]


def load_log() -> dict:
    if not LOG_PATH.exists():
        return {"used_topics": [], "current_week": 0, "history": []}
    with open(LOG_PATH) as f:
        return json.load(f)


def save_log(log: dict):
    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def pick_topic(log: dict) -> dict:
    used_names = set(log.get("used_topics", []))
    available  = [t for t in ALL_TOPICS if t["topic"] not in used_names]
    if not available:
        print("  → All 52 topics used — resetting pool from the beginning.")
        log["used_topics"] = []
        available = ALL_TOPICS[:]
    return available[0]


def generate_brief(topic_data: dict, week_num: int, client: Groq) -> dict:
    """Single Groq call that returns structured data used by both the HTML file and the email."""
    prompt = f"""You are writing a product brief for a solo digital product creator selling printables on Etsy.

Topic: {topic_data['topic']}
Age range: {topic_data['age']}
Format: {topic_data['format']}

Return ONLY valid JSON, no markdown, no code fences, no extra text:
{{
  "what_to_build": "2 sentences describing the product specifically — what pages it contains, what kids do with it.",
  "why_it_sells": ["who buys it", "when they search for it", "what problem it solves for parents"],
  "competitors": ["what existing Etsy sellers are doing for this topic (1 sentence)", "a second observation"],
  "differentiation": ["specific thing to add that competitors don't have", "another differentiator", "third differentiator"],
  "build_steps": [
    "Step 1: Open Canva and search templates for...",
    "Step 2: ...",
    "Step 3: ...",
    "Step 4: ...",
    "Step 5: Export as PDF Print and upload to Etsy"
  ],
  "price": "$X.XX",
  "etsy_title": "Full Etsy listing title here (max 140 chars, keyword-rich)",
  "etsy_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}

Rules: price between $3.99–$7.99. Build steps must be specific to this exact product. Tags are what parents type into Etsy search.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=900,
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if model added them
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def build_html_page(topic_data: dict, brief: dict, week_num: int, used_count: int) -> str:
    remaining  = len(ALL_TOPICS) - used_count
    steps_html = "".join(f"<li>{s}</li>" for s in brief.get("build_steps", []))
    diff_html  = "".join(f"<li>{d}</li>" for d in brief.get("differentiation", []))
    why_html   = "".join(f"<li>{w}</li>" for w in brief.get("why_it_sells", []))
    comp_html  = "".join(f"<li>{c}</li>" for c in brief.get("competitors", []))
    tags_str   = ", ".join(brief.get("etsy_tags", []))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Children's Brief — Week {week_num}: {topic_data['topic']}</title>
<style>
  :root {{ --bg:#1A1A2E; --gold:#C9A84C; --text:#E8E0D0; --card:#24243E; --muted:#888; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:Georgia,serif; max-width:760px; margin:40px auto; padding:24px 20px; line-height:1.75; }}
  h1   {{ color:var(--gold); font-size:1.7rem; margin-bottom:4px; }}
  h2   {{ color:var(--gold); font-size:1rem; margin:26px 0 8px; border-bottom:1px solid #333; padding-bottom:4px; text-transform:uppercase; letter-spacing:.05em; }}
  p    {{ margin-bottom:10px; }}
  ul,ol{{ padding-left:20px; margin-bottom:10px; }}
  li   {{ margin-bottom:6px; }}
  strong {{ color:#ddd; }}
  .badge {{ display:inline-block; background:var(--gold); color:var(--bg); font-size:12px; font-weight:bold; padding:3px 14px; border-radius:20px; margin-bottom:14px; letter-spacing:.05em; }}
  .meta  {{ color:var(--muted); font-size:13px; margin-bottom:20px; }}
  .progress {{ background:var(--card); border-radius:8px; padding:12px 16px; margin-bottom:28px; font-size:13px; color:#aaa; display:flex; justify-content:space-between; align-items:center; }}
  .progress strong {{ color:var(--gold); }}
  .bar-wrap {{ background:#333; border-radius:6px; height:6px; width:180px; overflow:hidden; }}
  .bar-fill {{ background:var(--gold); height:100%; border-radius:6px; width:{round(used_count/len(ALL_TOPICS)*100)}%; }}
  .tag {{ display:inline-block; background:#2a2a4e; color:var(--gold); padding:2px 10px; border-radius:12px; font-size:12px; margin:2px; }}
  .footer {{ text-align:center; color:#555; font-size:12px; margin-top:44px; border-top:1px solid #2a2a3e; padding-top:16px; }}
</style>
</head>
<body>
<span class="badge">WEEK {week_num}</span>
<h1>Children's Activities Brief</h1>
<div class="meta">{topic_data['topic']} &nbsp;·&nbsp; Ages {topic_data['age']} &nbsp;·&nbsp; {topic_data['format']} &nbsp;·&nbsp; {datetime.now().strftime("%B %d, %Y")}</div>
<div class="progress">
  <span>Topic <strong>{used_count}</strong> of <strong>{len(ALL_TOPICS)}</strong> &nbsp;—&nbsp; <strong>{remaining} left</strong> before reset</span>
  <div class="bar-wrap"><div class="bar-fill"></div></div>
</div>
<h2>What To Build</h2><p>{brief.get("what_to_build","")}</p>
<h2>Why It Sells</h2><ul>{why_html}</ul>
<h2>What Competitors Are Doing</h2><ul>{comp_html}</ul>
<h2>How To Make Yours Better</h2><ul>{diff_html}</ul>
<h2>How To Build It In Canva</h2><ol>{steps_html}</ol>
<h2>Pricing and Listing</h2>
<p><strong>Launch price:</strong> {brief.get("price","")}</p>
<p><strong>Etsy title:</strong> {brief.get("etsy_title","")}</p>
<p><strong>Tags:</strong> {"".join(f'<span class="tag">{t}</span>' for t in brief.get("etsy_tags",[]))}</p>
<div class="footer">The Bell Newsletter &nbsp;·&nbsp; Children's Activities &nbsp;·&nbsp; Week {week_num}</div>
</body>
</html>"""


def run():
    log        = load_log()
    topic_data = pick_topic(log)
    week_num   = log["current_week"] + 1
    used_count = len(log["used_topics"]) + 1

    # Update log before API call so a crash doesn't re-use the same topic
    log["used_topics"].append(topic_data["topic"])
    log["current_week"] = week_num
    log["last_run"]     = datetime.now().isoformat()
    log.setdefault("history", []).append({
        "week":  week_num,
        "topic": topic_data["topic"],
        "date":  datetime.now().strftime("%Y-%m-%d"),
    })
    save_log(log)

    remaining = len(ALL_TOPICS) - used_count
    print(f"Children's Activities — Week {week_num}: {topic_data['topic']}")
    print(f"  ({remaining} topics remaining before list resets)")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    brief  = generate_brief(topic_data, week_num, client)

    page = build_html_page(topic_data, brief, week_num, used_count)

    # Save to .tmp/ (local use) AND docs/ (committed to repo → accessible via URL)
    BRIEF_PATH.parent.mkdir(exist_ok=True)
    DOCS_PATH.parent.mkdir(exist_ok=True)
    with open(BRIEF_PATH, "w") as f:
        f.write(page)
    with open(DOCS_PATH, "w") as f:
        f.write(page)

    # Save structured data for draft_newsletter.py to use directly in the email
    data = {
        "topic":          topic_data["topic"],
        "age_range":      topic_data["age"],
        "format":         topic_data["format"],
        "week_num":       week_num,
        "what_to_build":  brief.get("what_to_build", ""),
        "build_steps":    brief.get("build_steps", []),
        "price":          brief.get("price", ""),
        "etsy_title":     brief.get("etsy_title", ""),
        "etsy_tags":      brief.get("etsy_tags", []),
        "brief_url":      BRIEF_URL,
    }
    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  Brief → {BRIEF_PATH} + {DOCS_PATH}")
    print(f"  Data  → {DATA_PATH}")
    print(f"  URL   → {BRIEF_URL}")
    return data


if __name__ == "__main__":
    run()
