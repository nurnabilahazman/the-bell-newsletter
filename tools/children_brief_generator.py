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
    """Single Groq call returning rich structured data for both the HTML brief and the newsletter email."""
    prompt = f"""You are writing a weekly product brief for a solo digital products creator selling printables on Etsy.

Topic: {topic_data['topic']}
Age range: {topic_data['age']}
Format: {topic_data['format']}

Return ONLY valid JSON. No markdown, no code fences, no extra text:
{{
  "opportunity_score": 8,
  "competition_level": "Medium",
  "demand_level": "High",
  "market_opportunity": "One sentence on why this specific niche is a good opportunity right now.",
  "what_to_build": "2–3 sentences describing the product specifically — what pages it has, how many pages, what the child actually does with it.",
  "why_it_sells": [
    "Who buys it and when (e.g. parents of 3-5 year olds preparing for kindergarten)",
    "The search trigger (e.g. searched year-round, peaks in August back-to-school season)",
    "The emotional reason parents buy it (e.g. want structured screen-free activity)"
  ],
  "top_competitors": [
    {{"name": "Shop or product name", "insight": "What makes it sell — specific detail about their design or positioning"}},
    {{"name": "Another shop or product", "insight": "What makes it sell"}}
  ],
  "market_gaps": [
    "A specific gap in what competitors offer that you can fill",
    "Another gap or opportunity"
  ],
  "differentiation": [
    "Specific feature to add that competitors don't have (be concrete)",
    "Another concrete differentiator",
    "Third differentiator"
  ],
  "build_steps": [
    "Open Canva → search 'kids {topic_data['topic'].lower()} worksheet template' → pick a clean, colourful template",
    "Customise colours to a bright, child-friendly palette (e.g. sky blue, soft yellow, coral)",
    "Add specific content detail for this product type",
    "Check font size is minimum 18pt so children can read easily — add your shop name/logo in footer",
    "Download as PDF Print → upload to Etsy as a digital download listing"
  ],
  "launch_checklist": [
    "Create 25–30 pages minimum (buyers compare page count)",
    "Add a free bonus page (e.g. certificate of completion) — mention in listing",
    "Use all 13 Etsy tags — include age range in at least 3 tags",
    "Upload 5–7 mockup images (use Canva or Placeit for lifestyle mockups)",
    "Price at ${{"$4.99"}} for launch week, raise to ${{"$5.99"}} after first 3 reviews"
  ],
  "price": "$4.99",
  "etsy_title": "Keyword-rich Etsy title here, max 140 characters, include age range and product type",
  "etsy_tags": ["tag one", "tag two", "tag three", "tag four", "tag five", "tag six", "tag seven"]
}}

Rules:
- opportunity_score: integer 1–10
- competition_level: exactly "Low", "Medium", or "High"
- demand_level: exactly "Low", "Medium", or "High"
- price: between $3.99–$7.99
- build_steps: exactly 5 steps, each starting with an action verb, specific to THIS product
- etsy_tags: exactly 7 tags, each under 20 characters, what parents actually search
- All content must be specific to '{topic_data['topic']}' — no generic filler
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
    )
    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def build_html_page(topic_data: dict, brief: dict, week_num: int, used_count: int) -> str:
    remaining   = len(ALL_TOPICS) - used_count
    bar_pct     = round(used_count / len(ALL_TOPICS) * 100)
    score       = brief.get("opportunity_score", 8)
    comp_level  = brief.get("competition_level", "Medium")
    demand      = brief.get("demand_level", "High")
    comp_color  = {"Low": "#3DD68C", "Medium": "#C9A84C", "High": "#E94560"}.get(comp_level, "#C9A84C")
    demand_color= {"Low": "#888", "Medium": "#C9A84C", "High": "#3DD68C"}.get(demand, "#3DD68C")
    date_str    = datetime.now().strftime("%B %d, %Y")

    def li_list(items):
        return "".join(f"<li>{i}</li>" for i in items if i)

    def ol_list(items):
        return "".join(f"<li>{i}</li>" for i in items if i)

    competitors_html = ""
    for c in brief.get("top_competitors", []):
        competitors_html += f"""
        <div class="comp-card">
          <div class="comp-name">{c.get('name','')}</div>
          <div class="comp-insight">{c.get('insight','')}</div>
        </div>"""

    checklist_html = "".join(
        f'<div class="check-item"><span class="check-box"></span><span>{item}</span></div>'
        for item in brief.get("launch_checklist", [])
    )

    tags_html = "".join(
        f'<span class="etsy-tag">{t}</span>' for t in brief.get("etsy_tags", [])
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Children's Activities Brief — Week {week_num}: {topic_data['topic']}</title>
<style>
  :root {{
    --bg:#0B0B14; --card:#12121F; --card2:#191928; --border:#252538;
    --gold:#C9A84C; --gold-dim:rgba(201,168,76,0.12);
    --green:#3DD68C; --green-dim:rgba(61,214,140,0.1);
    --red:#E94560; --blue:#4EA8DE;
    --text:#E2E2E2; --muted:#6B7280;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ scroll-behavior:smooth; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,-apple-system,sans-serif; font-size:15px; line-height:1.7; padding:32px 20px 80px; }}
  .container {{ max-width:960px; margin:0 auto; }}

  /* ── NAV ── */
  .toc {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 24px; margin-bottom:32px; display:flex; flex-wrap:wrap; gap:10px 24px; align-items:center; }}
  .toc-label {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:1px; margin-right:8px; }}
  .toc a {{ color:var(--gold); text-decoration:none; font-size:.88rem; }}
  .toc a:hover {{ text-decoration:underline; }}

  /* ── HERO ── */
  .hero {{ background:linear-gradient(135deg,#12121F 0%,#1A1230 100%); border:1px solid var(--border); border-left:5px solid var(--gold); border-radius:16px; padding:36px 32px; margin-bottom:36px; position:relative; overflow:hidden; }}
  .hero::before {{ content:''; position:absolute; top:-60px; right:-60px; width:220px; height:220px; background:radial-gradient(circle,rgba(201,168,76,.08) 0%,transparent 70%); border-radius:50%; }}
  .hero-week {{ color:var(--gold); font-size:.78rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; }}
  .hero h1 {{ font-size:1.9rem; color:white; font-weight:800; line-height:1.25; margin-bottom:6px; }}
  .hero-sub {{ color:var(--muted); font-size:.95rem; margin-bottom:24px; }}
  .hero-stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:16px; border-top:1px solid var(--border); padding-top:20px; }}
  .stat-label {{ color:var(--muted); font-size:.75rem; text-transform:uppercase; letter-spacing:.5px; }}
  .stat-value {{ font-size:1.35rem; font-weight:700; margin-top:2px; }}

  /* ── PROGRESS BAR ── */
  .progress-wrap {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 20px; margin-bottom:32px; }}
  .progress-top {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:.88rem; }}
  .progress-top strong {{ color:var(--gold); }}
  .progress-top .muted {{ color:var(--muted); font-size:.82rem; }}
  .bar-track {{ background:#1e1e30; border-radius:8px; height:8px; overflow:hidden; }}
  .bar-fill {{ background:linear-gradient(90deg,var(--gold),#e8c56a); height:100%; border-radius:8px; width:{bar_pct}%; transition:width .4s; }}

  /* ── SECTIONS ── */
  section {{ margin-bottom:40px; }}
  .section-header {{ display:flex; align-items:center; gap:12px; margin-bottom:18px; padding-bottom:10px; border-bottom:2px solid var(--border); }}
  .section-icon {{ font-size:1.4rem; }}
  .section-title {{ font-size:1.2rem; font-weight:700; color:white; }}
  .section-sub {{ color:var(--muted); font-size:.85rem; margin-left:auto; }}

  /* ── CARDS ── */
  .card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px 22px; margin-bottom:12px; }}
  .card-title {{ color:var(--gold); font-weight:600; font-size:.85rem; margin-bottom:10px; text-transform:uppercase; letter-spacing:.5px; }}
  .card p {{ color:var(--text); font-size:.95rem; }}
  ul {{ padding-left:20px; margin:8px 0; }}
  ul li {{ margin-bottom:7px; font-size:.93rem; }}
  ol {{ padding-left:20px; margin:8px 0; }}
  ol li {{ margin-bottom:8px; font-size:.93rem; }}

  /* ── COMPETITOR CARDS ── */
  .comp-card {{ background:var(--card2); border:1px solid var(--border); border-radius:10px; padding:14px 18px; margin-bottom:10px; }}
  .comp-name {{ font-weight:700; color:white; font-size:.95rem; margin-bottom:4px; }}
  .comp-insight {{ color:var(--muted); font-size:.88rem; }}

  /* ── MARKET GAPS ── */
  .gap-item {{ background:var(--green-dim); border:1px solid rgba(61,214,140,.2); border-radius:8px; padding:10px 16px; margin-bottom:8px; font-size:.9rem; color:var(--text); }}
  .gap-item::before {{ content:'→ '; color:var(--green); font-weight:700; }}

  /* ── BUILD STEPS ── */
  .step-card {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 18px; margin-bottom:10px; display:flex; gap:14px; align-items:flex-start; }}
  .step-num {{ background:var(--gold); color:#0B0B14; border-radius:50%; width:26px; height:26px; min-width:26px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:.82rem; margin-top:1px; }}
  .step-text {{ font-size:.93rem; color:var(--text); }}

  /* ── CHECKLIST ── */
  .check-item {{ display:flex; align-items:flex-start; gap:12px; padding:9px 0; border-bottom:1px solid var(--border); font-size:.9rem; }}
  .check-item:last-child {{ border-bottom:none; }}
  .check-box {{ width:18px; height:18px; min-width:18px; border:2px solid var(--border); border-radius:4px; margin-top:2px; }}

  /* ── PRICING ── */
  .price-big {{ font-size:2.2rem; font-weight:800; color:var(--gold); }}
  .listing-box {{ background:var(--card2); border:1px solid var(--border); border-radius:10px; padding:16px 18px; margin-top:14px; }}
  .listing-label {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.5px; margin-bottom:5px; }}
  .listing-value {{ color:var(--text); font-size:.92rem; }}
  .etsy-tag {{ display:inline-block; background:var(--gold-dim); color:var(--gold); border:1px solid rgba(201,168,76,.3); padding:3px 10px; border-radius:20px; font-size:.8rem; margin:3px; }}

  /* ── FOOTER ── */
  .footer {{ text-align:center; color:var(--muted); font-size:.82rem; margin-top:60px; border-top:1px solid var(--border); padding-top:20px; }}
</style>
</head>
<body>
<div class="container">

<!-- NAV -->
<nav class="toc">
  <span class="toc-label">Jump to</span>
  <a href="#opportunity">Opportunity</a>
  <a href="#competitors">Competitors</a>
  <a href="#gaps">Market Gaps</a>
  <a href="#build">How To Build</a>
  <a href="#checklist">Checklist</a>
  <a href="#listing">Listing</a>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-week">The Bell Newsletter &nbsp;·&nbsp; Week {week_num} &nbsp;·&nbsp; {date_str}</div>
  <h1>{topic_data['topic']}</h1>
  <div class="hero-sub">Ages {topic_data['age']} &nbsp;·&nbsp; {topic_data['format']} &nbsp;·&nbsp; Children's Activities Niche</div>
  <div class="hero-stats">
    <div>
      <div class="stat-label">Opportunity Score</div>
      <div class="stat-value" style="color:var(--gold)">{score}/10</div>
    </div>
    <div>
      <div class="stat-label">Competition</div>
      <div class="stat-value" style="color:{comp_color}">{comp_level}</div>
    </div>
    <div>
      <div class="stat-label">Demand</div>
      <div class="stat-value" style="color:{demand_color}">{demand}</div>
    </div>
    <div>
      <div class="stat-label">Launch Price</div>
      <div class="stat-value" style="color:var(--green)">{brief.get('price','')}</div>
    </div>
  </div>
</div>

<!-- PROGRESS BAR -->
<div class="progress-wrap">
  <div class="progress-top">
    <span>Topic <strong>{used_count}</strong> of <strong>{len(ALL_TOPICS)}</strong> &nbsp;·&nbsp; Year 1 Progress</span>
    <span class="muted"><strong style="color:var(--gold)">{remaining}</strong> topics remaining before reset</span>
  </div>
  <div class="bar-track"><div class="bar-fill"></div></div>
</div>

<!-- OPPORTUNITY -->
<section id="opportunity">
  <div class="section-header">
    <span class="section-icon">💡</span>
    <span class="section-title">Market Opportunity</span>
  </div>
  <div class="card">
    <div class="card-title">Why This Topic Now</div>
    <p>{brief.get('market_opportunity','')}</p>
  </div>
  <div class="card">
    <div class="card-title">What To Build</div>
    <p>{brief.get('what_to_build','')}</p>
  </div>
  <div class="card">
    <div class="card-title">Why It Sells</div>
    <ul>{li_list(brief.get('why_it_sells',[]))}</ul>
  </div>
</section>

<!-- COMPETITORS -->
<section id="competitors">
  <div class="section-header">
    <span class="section-icon">🔍</span>
    <span class="section-title">Competitor Analysis</span>
    <span class="section-sub">What's already selling on Etsy</span>
  </div>
  {competitors_html}
  <div class="card" style="margin-top:10px">
    <div class="card-title">Your Differentiators</div>
    <ul>{li_list(brief.get('differentiation',[]))}</ul>
  </div>
</section>

<!-- MARKET GAPS -->
<section id="gaps">
  <div class="section-header">
    <span class="section-icon">🎯</span>
    <span class="section-title">Market Gaps</span>
    <span class="section-sub">What competitors are missing</span>
  </div>
  {"".join(f'<div class="gap-item">{g}</div>' for g in brief.get('market_gaps',[]))}
</section>

<!-- BUILD GUIDE -->
<section id="build">
  <div class="section-header">
    <span class="section-icon">🛠️</span>
    <span class="section-title">How To Build It in Canva</span>
    <span class="section-sub">Step by step</span>
  </div>
  {"".join(f'<div class="step-card"><div class="step-num">{i+1}</div><div class="step-text">{s}</div></div>' for i,s in enumerate(brief.get('build_steps',[])))}
</section>

<!-- LAUNCH CHECKLIST -->
<section id="checklist">
  <div class="section-header">
    <span class="section-icon">✅</span>
    <span class="section-title">Launch Checklist</span>
  </div>
  <div class="card">
    {checklist_html}
  </div>
</section>

<!-- LISTING -->
<section id="listing">
  <div class="section-header">
    <span class="section-icon">🏷️</span>
    <span class="section-title">Pricing and Listing</span>
  </div>
  <div class="card">
    <div class="card-title">Launch Price</div>
    <div class="price-big">{brief.get('price','')}</div>
    <p style="color:var(--muted);font-size:.88rem;margin-top:6px">Raise by $1 after your first 3 reviews.</p>
  </div>
  <div class="listing-box">
    <div class="listing-label">Etsy Title</div>
    <div class="listing-value">{brief.get('etsy_title','')}</div>
  </div>
  <div class="listing-box" style="margin-top:10px">
    <div class="listing-label">Etsy Tags</div>
    <div style="margin-top:6px">{tags_html}</div>
  </div>
</section>

<div class="footer">
  The Bell Newsletter &nbsp;·&nbsp; Children's Activities Brief &nbsp;·&nbsp; Week {week_num} &nbsp;·&nbsp; {date_str}<br>
  Generated weekly · New topic every Monday
</div>

</div>
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
