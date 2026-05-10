#!/usr/bin/env python3
"""
Productivity & Trackers Weekly Brief Generator

Every 5 weeks a new unified brief is generated (top 5 products for that block).
The same brief is reused for all 5 weeks in the block, with only the progress
bar updating each week to show current position.

Block 1  (weeks  1– 5): static pre-researched products (no API call)
Block 2  (weeks  6–10): generate new brief at week  6, reuse through week 10
Block 3  (weeks 11–15): generate new brief at week 11, reuse through week 15
... and so on.

Run alongside children_brief_generator.py (step 1 of pipeline):
  python tools/productivity_brief_generator.py

State files:
  config/productivity_topics_log.json   — week counter + topic history
  config/productivity_block_state.json  — current block products (committed to repo)
  docs/current_productivity_brief.html  — this week's brief (committed to repo → URL)
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

LOG_PATH         = Path("config/productivity_topics_log.json")
BLOCK_STATE_PATH = Path("config/productivity_block_state.json")
BRIEF_PATH       = Path(".tmp/unified_productivity_brief.html")
DOCS_PATH        = Path("docs/current_productivity_brief.html")
BASE_HTML_PATH   = Path("docs/unified_product_brief_productivity_base.html")
DATA_PATH        = Path(".tmp/productivity_brief_data.json")
MODEL            = "llama-3.3-70b-versatile"
BRIEF_URL        = "https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_productivity_brief.html"

# Block 1 products — pre-researched, no API call needed
BLOCK1_PRODUCTS = [
    {
        "topic": "Monthly Budget Tracker",
        "rank": 1, "format": "PDF printable",
        "build_steps": [
            "Open Canva → search 'budget tracker template' → pick a clean minimal design with a neutral color scheme",
            "Create 12 monthly overview pages (one per month) — each with income vs expenses table, savings goal row",
            "Add a weekly expense log section (4 pages per month × 12 months = 48 log pages)",
            "Include bonus pages: Annual savings summary, Subscription tracker, Sinking funds tracker",
            "Export as PDF Print (A4 or Letter) → upload to Etsy as a digital download",
        ],
        "price": "$5.99",
        "etsy_title": "Monthly Budget Tracker Printable | 2025–2026 | Income Expense Log | Instant Download PDF",
        "etsy_tags": ["budget tracker", "expense tracker", "monthly planner", "finance printable", "budget printable", "savings tracker", "money tracker", "monthly budget", "household budget", "spending tracker", "bills tracker", "budget template", "personal finance"],
        "what_to_build": "A 60+ page annual budget tracker with monthly overviews, weekly expense logs, and bonus finance pages. Buyers use it to track every dollar in and out for the full year.",
        "why_it_sells": "Budget trackers are a top-5 Etsy bestseller year-round — people search for them every January and after every payday.",
    },
    {
        "topic": "Daily Productivity Planner",
        "rank": 2, "format": "PDF printable",
        "build_steps": [
            "Open Canva → search 'daily planner template' → pick a clean design with a top-priorities section",
            "Create one master daily page with: date, top 3 priorities, hourly schedule (6am–10pm), notes, water tracker, gratitude line",
            "Add a weekly overview page (Mon–Sun at a glance + weekly goal)",
            "Create a 365-day set: duplicate the daily page 365× — or sell a 90-day version (more affordable)",
            "Export as PDF Print → upload to Etsy with 'undated' in the title so it sells year-round",
        ],
        "price": "$4.99",
        "etsy_title": "Daily Productivity Planner Printable | Undated | Top 3 Priorities + Hourly Schedule | PDF",
        "etsy_tags": ["daily planner", "productivity planner", "printable planner", "undated planner", "daily schedule", "planner printable", "time management", "to do list", "daily organizer", "schedule printable", "planner pages", "hourly planner", "work planner"],
        "what_to_build": "An undated daily planner with hourly time blocks, top priorities, water tracker, and gratitude section. Available as a 90-day or 365-day set.",
        "why_it_sells": "Undated planners sell year-round (no expiry date) and consistently rank in Etsy's top printables — every planner buyer needs a daily layout.",
    },
    {
        "topic": "30-Day Habit Tracker",
        "rank": 3, "format": "PDF printable",
        "build_steps": [
            "Open Canva → search 'habit tracker template' → pick a design with a grid layout and room for habit names",
            "Create a single-page monthly habit tracker: 10 habit rows × 31 day columns, plus a monthly reflection section",
            "Make it undated — include a blank 'Month:' field so it works for any month of any year",
            "Add a bonus page: 'How to Build a Habit in 30 Days' — one-page guide with the habit loop explained simply",
            "Export as PDF Print → list as a 5-pack (5 copies of the tracker page) for perceived value",
        ],
        "price": "$3.99",
        "etsy_title": "30 Day Habit Tracker Printable | Monthly Habit Log | Undated | Instant Download PDF",
        "etsy_tags": ["habit tracker", "30 day habit", "monthly tracker", "habit log printable", "goal tracker", "self improvement", "wellness tracker", "daily habits", "habit journal", "routine tracker", "morning routine", "self care", "habit challenge"],
        "what_to_build": "An undated 30-day habit tracker with 10 habit slots, daily checkboxes, and a monthly reflection section. Sold as a 5-pack so buyers can track multiple months.",
        "why_it_sells": "Habit trackers are among the most searched printables on Etsy — they spike in January and September but sell consistently all year.",
    },
    {
        "topic": "Weekly Meal Planner + Grocery List",
        "rank": 4, "format": "PDF printable",
        "build_steps": [
            "Open Canva → search 'meal planner template' → pick a design that shows all 7 days plus a grocery list column",
            "Create a landscape A4 or letter-size page: left side = 7-day meal grid (breakfast/lunch/dinner/snack), right side = grocery list by category",
            "Add a separate grocery list page organised by aisle: Produce, Dairy, Meat, Pantry, Frozen, Other",
            "Include a monthly meal planning calendar page (30-day grid, one meal per box)",
            "Export as PDF Print → sell as a 52-week set (undated, one page per week)",
        ],
        "price": "$3.99",
        "etsy_title": "Weekly Meal Planner Printable + Grocery List | Undated | 52 Week Set | Instant Download",
        "etsy_tags": ["meal planner", "grocery list", "weekly meal plan", "meal planning", "food planner", "family meal planner", "dinner planner", "meal prep planner", "weekly menu", "recipe organizer", "healthy eating", "shopping list", "meal organizer"],
        "what_to_build": "A 52-week undated meal planner with a 7-day grid for all meals, a categorised grocery list, and a monthly planning overview. Buyers print weekly.",
        "why_it_sells": "Meal planners are one of Etsy's top-10 most-purchased printables — families buy them repeatedly because they use a new one every week.",
    },
    {
        "topic": "Goal Setting Workbook (Quarterly Edition)",
        "rank": 5, "format": "PDF workbook",
        "build_steps": [
            "Open Canva → search 'goal setting workbook' → pick a premium, clean design with journaling space",
            "Create a 30+ page quarterly workbook: vision statement, 3 big goals, monthly breakdown, weekly check-ins, and a quarterly review",
            "Add a 'wheel of life' assessment page, a values clarification exercise, and an affirmations page",
            "Use a premium color scheme (navy + gold or charcoal + blush) to position it as a high-value product",
            "Export as PDF Print → price at $6.99–$7.99 (workbooks command higher prices than single trackers)",
        ],
        "price": "$6.99",
        "etsy_title": "Goal Setting Workbook Printable | Quarterly Planner | Vision + Goals + Weekly Review | PDF",
        "etsy_tags": ["goal setting", "quarterly planner", "goal planner", "vision board", "self improvement", "life goals", "mindset journal", "goals worksheet", "year planner", "new year goals", "goal tracker", "annual planner", "bucket list"],
        "what_to_build": "A 30+ page quarterly goal-setting workbook with vision statement, goal breakdowns, monthly milestones, and weekly check-ins. Buyers use it every 3 months.",
        "why_it_sells": "Goal workbooks are a premium product — buyers are willing to pay more because the content is deeper than a single tracker, and they spike every quarter.",
    },
]

# 48-topic pool for blocks 2+ (Groq-generated briefs pick 5 at a time)
ALL_TOPICS = [
    {"topic": "Annual Budget Planner",              "format": "PDF printable"},
    {"topic": "Debt Payoff Tracker",                "format": "PDF printable"},
    {"topic": "Savings Goal Tracker",               "format": "PDF printable"},
    {"topic": "Emergency Fund Tracker",             "format": "PDF printable"},
    {"topic": "Sinking Funds Planner",              "format": "PDF printable"},
    {"topic": "Paycheck Budget Template",           "format": "PDF printable"},
    {"topic": "Bill Payment Tracker",               "format": "PDF printable"},
    {"topic": "Subscription Tracker",               "format": "PDF printable"},
    {"topic": "Net Worth Tracker",                  "format": "PDF or Sheets"},
    {"topic": "Weekly Time Block Planner",          "format": "PDF printable"},
    {"topic": "Morning Routine Planner",            "format": "PDF printable"},
    {"topic": "Evening Routine Checklist",          "format": "PDF printable"},
    {"topic": "Work From Home Planner",             "format": "PDF printable"},
    {"topic": "Student Study Planner",              "format": "PDF printable"},
    {"topic": "Project Planning Workbook",          "format": "PDF printable"},
    {"topic": "Brain Dump + Priority Matrix",       "format": "PDF printable"},
    {"topic": "Annual Review Workbook",             "format": "PDF workbook"},
    {"topic": "Vision Board Planning Kit",          "format": "PDF printable"},
    {"topic": "90-Day Goal Planner",                "format": "PDF workbook"},
    {"topic": "Weekly Self-Review Template",        "format": "PDF printable"},
    {"topic": "Gratitude Journal (30 Days)",        "format": "PDF journal"},
    {"topic": "Mindfulness + Mood Tracker",         "format": "PDF printable"},
    {"topic": "Sleep Tracker + Bedtime Routine",    "format": "PDF printable"},
    {"topic": "Water Intake Tracker",               "format": "PDF printable"},
    {"topic": "Fitness + Workout Tracker",          "format": "PDF printable"},
    {"topic": "Weight Loss Progress Tracker",       "format": "PDF printable"},
    {"topic": "Healthy Habits Challenge (21 Day)",  "format": "PDF printable"},
    {"topic": "Reading Log + Book Tracker",         "format": "PDF printable"},
    {"topic": "Learning Goal Tracker",              "format": "PDF printable"},
    {"topic": "Etsy Shop Planner",                  "format": "PDF printable"},
    {"topic": "Social Media Content Calendar",      "format": "PDF printable"},
    {"topic": "Blog Post Planner",                  "format": "PDF printable"},
    {"topic": "Freelancer Income Tracker",          "format": "PDF or Sheets"},
    {"topic": "Client Onboarding Checklist",        "format": "PDF printable"},
    {"topic": "Invoice + Expense Log",              "format": "PDF printable"},
    {"topic": "Home Cleaning Schedule",             "format": "PDF printable"},
    {"topic": "Home Maintenance Checklist",         "format": "PDF printable"},
    {"topic": "Moving Checklist + Planner",         "format": "PDF printable"},
    {"topic": "Declutter Challenge (30 Day)",       "format": "PDF printable"},
    {"topic": "Travel Planner + Packing List",      "format": "PDF printable"},
    {"topic": "Vacation Budget Planner",            "format": "PDF printable"},
    {"topic": "Wedding Planning Checklist",         "format": "PDF printable"},
    {"topic": "Baby Shower Planning Kit",           "format": "PDF printable"},
    {"topic": "New Year Goal Setting Kit",          "format": "PDF workbook"},
    {"topic": "Self-Care Planner (Weekly)",         "format": "PDF printable"},
    {"topic": "Classroom Management Planner",       "format": "PDF printable"},
    {"topic": "Teacher Lesson Planner",             "format": "PDF printable"},
    {"topic": "Small Business Starter Planner",     "format": "PDF workbook"},
]


# ── State helpers ──────────────────────────────────────────────────────────────

def load_log() -> dict:
    if not LOG_PATH.exists():
        return {"used_topics": [], "current_week": 0, "history": []}
    with open(LOG_PATH) as f:
        return json.load(f)


def save_log(log: dict):
    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)


def load_block_state() -> dict:
    if not BLOCK_STATE_PATH.exists():
        return {}
    with open(BLOCK_STATE_PATH) as f:
        return json.load(f)


def save_block_state(state: dict):
    BLOCK_STATE_PATH.parent.mkdir(exist_ok=True)
    with open(BLOCK_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def get_block_info(week_num: int) -> tuple:
    """Returns (block_num, week_in_block) — both 1-based."""
    block_num     = (week_num - 1) // 5 + 1
    week_in_block = (week_num - 1) % 5 + 1
    return block_num, week_in_block


def pick_5_topics(log: dict) -> list:
    used_names = set(log.get("used_topics", []))
    available  = [t for t in ALL_TOPICS if t["topic"] not in used_names]
    if len(available) < 5:
        print("  → Topic pool exhausted — resetting for next cycle.")
        log["used_topics"] = []
        available = ALL_TOPICS[:]
    return available[:5]


# ── API call ───────────────────────────────────────────────────────────────────

def generate_block_products(topics: list, block_num: int, client: Groq) -> list:
    """One Groq call → 5 product specs for a new 5-week block."""
    topics_str = "\n".join(
        f"{i+1}. {t['topic']} ({t['format']})"
        for i, t in enumerate(topics)
    )
    prompt = f"""You are writing product specs for a solo digital products creator selling printables on Etsy.
Generate exactly 5 product briefs for these Productivity & Trackers products (Block {block_num}):

{topics_str}

Return ONLY a valid JSON array of 5 objects. No markdown, no code fences:
[
  {{
    "topic": "exact topic name",
    "format": "format type",
    "price": "$4.99",
    "etsy_title": "Keyword-rich title, max 140 chars, include format type and key benefit",
    "etsy_tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"],
    "build_steps": [
      "Open Canva → search relevant template → pick clean minimal design",
      "Step 2 starting with action verb, specific to this product",
      "Step 3",
      "Step 4",
      "Export as PDF Print → upload to Etsy as a digital download"
    ],
    "what_to_build": "2 sentences: exactly what pages the product contains and what the buyer does with it.",
    "why_it_sells": "1 sentence: who buys it, when, and why it converts."
  }}
]

Rules:
- Exactly 5 objects in the same order as the input list
- price: $3.99–$8.99 (workbooks can go up to $8.99)
- build_steps: exactly 5 steps, action verb first, highly specific to EACH product
- etsy_tags: exactly 7 tags, each under 20 characters, what buyers actually search on Etsy
- All content specific to each individual product — no generic filler
- Productivity target buyer: adults aged 20–45, mostly women, buying for home/work/finances
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2500,
    )
    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    products = json.loads(raw.strip())
    for i, p in enumerate(products):
        p["rank"]   = i + 1
        p["format"] = topics[i]["format"]
    return products


# ── HTML builders ──────────────────────────────────────────────────────────────

RANK_COLORS = ["var(--gold)", "#A8A8A8", "#CD7F32", "var(--blue)", "var(--purple)"]
RANK_EMOJIS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]


def _progress_bar_html(products: list, week_in_block: int, week_num: int) -> str:
    steps_html = ""
    block_start_week = week_num - week_in_block + 1

    for i, p in enumerate(products):
        pos      = i + 1
        abs_week = block_start_week + i
        if pos < week_in_block:
            dot    = "background:#3DD68C;border-color:#3DD68C;"
            label  = "color:#3DD68C;"
            wlabel = f"✓ Wk {abs_week}"
        elif pos == week_in_block:
            dot    = "background:#C9A84C;border-color:#C9A84C;box-shadow:0 0 8px rgba(201,168,76,0.6);"
            label  = "color:#C9A84C;font-weight:700;"
            wlabel = f"▶ Wk {abs_week}"
        else:
            dot    = "background:transparent;border-color:#252538;"
            label  = "color:#6B7280;"
            wlabel = f"Wk {abs_week}"

        short = p["topic"].split(" — ")[0].split(" (")[0].strip()
        steps_html += f"""
          <div style="display:flex;flex-direction:column;align-items:center;gap:5px;flex:1;min-width:58px;max-width:112px;">
            <div style="width:22px;height:22px;border-radius:50%;border:2px solid;{dot}"></div>
            <div style="font-size:0.72rem;text-align:center;{label}">{wlabel}</div>
            <div style="font-size:0.67rem;color:#6B7280;text-align:center;line-height:1.3;">{short}</div>
          </div>"""

    bar_pct      = round(week_in_block / 5 * 100)
    weeks_left   = 5 - week_in_block
    current_name = products[week_in_block - 1]["topic"]

    return f"""
  <div style="background:#12121F;border:1px solid #252538;border-radius:14px;padding:22px 26px;margin-bottom:36px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
      <div>
        <div style="color:#C9A84C;font-size:0.75rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;">5-Week Block Progress</div>
        <div style="color:#E2E2E2;font-size:1.05rem;font-weight:700;">Week {week_in_block} of 5 &nbsp;·&nbsp; This Week: {current_name}</div>
      </div>
      <div style="color:#6B7280;font-size:0.82rem;">{weeks_left} week{"s" if weeks_left != 1 else ""} left in this block</div>
    </div>
    <div style="background:#1e1e30;border-radius:8px;height:7px;overflow:hidden;margin-bottom:18px;">
      <div style="background:linear-gradient(90deg,#C9A84C,#e8c56a);height:100%;border-radius:8px;width:{bar_pct}%;"></div>
    </div>
    <div style="display:flex;gap:6px;justify-content:space-around;flex-wrap:wrap;">
      {steps_html}
    </div>
  </div>
"""


def _action_plan_section_html(product_name: str, week_num: int) -> str:
    """Dynamic interactive launch checklist focused on the current week's product."""
    keyword = (product_name
               .replace("—", "").replace("–", "")
               .replace("(", "").replace(")", "")
               .replace("  ", " ").strip().lower())

    phases = [
        {
            "phase": "Research Your Market",
            "icon": "🔍",
            "color": "#4EA8DE",
            "steps": [
                (f'Search Etsy for <strong>"{keyword}"</strong> — screenshot the first 8 listings. '
                 "Note each one's price, page count, review count, and what their thumbnail shows. "
                 "This is your competitive landscape before you build anything.",
                 "~30 min"),
                ("Click the top 2–3 bestsellers and read ALL their 1–3 star reviews. "
                 "Write down every complaint — those gaps are exactly where your product wins "
                 "(e.g. 'wish there was more space to write', 'too generic', 'colours were different from preview').",
                 "~15 min"),
                ("Open Pinterest, search the same keyword, save 10–15 images to a mood-board folder in Canva: "
                 "colors, layouts, fonts, and styles buyers are already engaging with.",
                 "~15 min"),
            ],
        },
        {
            "phase": "Plan Before You Open Canva",
            "icon": "📝",
            "color": "#9B72CF",
            "steps": [
                ("Write your complete page list before touching Canva — e.g. "
                 "<em>Cover · Page 2: How to use · Pages 3–14: Monthly overviews · Pages 15–26: Weekly logs · Page 27: Annual summary</em>. "
                 "Target <strong>25+ pages minimum</strong> — buyers compare page count and mention it in reviews.",
                 "~15 min"),
                ("Commit to your one unique angle (from the brief above) — "
                 "a bonus section, a design style, or a niche focus that competitors don't have. "
                 "Write it on a sticky note where you can see it while building — it keeps every page decision consistent.",
                 "~5 min"),
            ],
        },
        {
            "phase": "Build in Canva",
            "icon": "🎨",
            "color": "#C9A84C",
            "steps": [
                ("Open Canva → follow the 5 build steps in the brief above → "
                 "work through every page on your content list in order. "
                 "Use a clean neutral palette (cream, warm grey, one accent) — minimalist designs outsell busy ones for productivity products.",
                 "2–4 hrs"),
                ("Proof every page before exporting: consistent fonts, consistent colours, "
                 "enough white space in every fill-in area (test-fill one page yourself first). "
                 "Fix everything now — updating files after your first sale is much harder.",
                 "~20 min"),
                ('<strong>Export as "PDF Print"</strong> (not "Standard PDF"). '
                 "PDF Print preserves 300 dpi resolution. "
                 "Blurry or pixelated printables get 1-star reviews — sharp ones get 5-star ones.",
                 "~5 min"),
            ],
        },
        {
            "phase": "Create Listing Images",
            "icon": "📸",
            "color": "#3DD68C",
            "steps": [
                ("<strong>Thumbnail first — it drives more Etsy clicks than any other factor.</strong> "
                 "Show the product flat on a clean background with text callouts: page count, 'Instant Download', key benefit. "
                 'Test it: open Etsy and compare your thumbnail side-by-side with competitors. Does yours stop the scroll?',
                 "~30 min"),
                ("Create 4–6 supporting images: 2 inside-page samples (your best pages), "
                 "1 lifestyle mockup on a desk with coffee/pen — use Canva's mockup feature (search 'planner mockup') "
                 "or <strong>Placeit.net</strong> (free tier). Add one 'What's Inside' summary listing every section.",
                 "~30 min"),
            ],
        },
        {
            "phase": "Publish on Etsy",
            "icon": "🚀",
            "color": "#E94560",
            "steps": [
                ("Create your Etsy listing. <strong>Paste the Etsy title exactly as shown</strong> in the brief. "
                 "Description: lead with what's included and page count, then how to download and print, then FAQs. "
                 "Use all 7 tags from the brief plus 6 more variations you can think of (aim for all 13 tags).",
                 "~25 min"),
                ("Set your launch price, upload all images (thumbnail goes first) and your PDF. Hit Publish. "
                 "Then: test-download your own listing using a second browser — "
                 "open the PDF and confirm every page looks correct before you promote it anywhere.",
                 "~15 min"),
            ],
        },
        {
            "phase": "Promote & Grow",
            "icon": "📈",
            "color": "#4EA8DE",
            "steps": [
                ("Post 2–3 Pinterest pins linking to your Etsy listing — "
                 "Pinterest is the #1 external traffic source for Etsy printables. "
                 "Pin to boards like 'Printable Planners', 'Budget Tracker', 'Productivity Tools', 'Etsy Digital Downloads'.",
                 "~20 min"),
                ("After your first sale, message the buyer within 24 hours: "
                 "<em>\"Thanks so much! Hope the planner is useful. "
                 "If you have a moment, a review means the world to a small shop 🙏\"</em> "
                 "— warm, brief, never pushy. Reviews are Etsy's #1 ranking signal.",
                 "~2 min"),
                ("At the 2-week mark: Etsy Stats → Search Terms. "
                 "Terms with views but no sales = thumbnail or price issue. "
                 "Terms that convert to sales = add them to your title and tags. "
                 "After 3 reviews, raise your price by $1 as suggested in the brief.",
                 "~15 min"),
            ],
        },
    ]

    total_steps = sum(len(p["steps"]) for p in phases)

    phases_html = ""
    step_num = 0
    for ph in phases:
        color      = ph["color"]
        items_html = ""
        for text, time_est in ph["steps"]:
            step_num += 1
            item_id   = "pt_ap_w" + str(week_num) + "_s" + str(step_num)
            items_html += (
                '\n          <div class="ap-item" data-id="' + item_id + '" '
                'onclick="toggleAP(\'' + item_id + '\')">'
                '\n            <div class="ap-check"></div>'
                '\n            <div style="flex:1;">'
                '\n              <div class="ap-text">' + text + '</div>'
                '\n              <div class="ap-time">' + time_est + '</div>'
                '\n            </div>'
                '\n          </div>'
            )
        n = len(ph["steps"])
        phases_html += (
            '\n        <div style="margin-bottom:18px;border:1px solid #252538;'
            'border-left:3px solid ' + color + ';border-radius:0 10px 10px 0;overflow:hidden;">'
            '\n          <div class="ap-phase-hdr" style="background:#191928;padding:11px 18px;'
            'border-bottom:1px solid #252538;">'
            '\n            <span style="font-size:1.05rem;">' + ph["icon"] + '</span>'
            '\n            <span style="font-weight:700;color:white;font-size:0.95rem;margin-left:8px;">'
            + ph["phase"] + '</span>'
            '\n            <span style="color:#6B7280;font-size:0.75rem;margin-left:auto;">'
            + str(n) + ' step' + ('s' if n != 1 else '') + '</span>'
            '\n          </div>'
            '\n          <div style="padding:2px 18px 10px;">' + items_html + '\n          </div>'
            '\n        </div>'
        )

    return f"""
  <!-- DYNAMIC ACTION PLAN — injected by productivity_brief_generator.py -->
  <style>
    .ap-item {{ cursor:pointer; display:flex; gap:14px; align-items:flex-start;
               padding:11px 0; border-bottom:1px solid #252538;
               transition:opacity .2s; -webkit-user-select:none; user-select:none; }}
    .ap-item:last-child {{ border-bottom:none; }}
    .ap-item:hover {{ opacity:.82; }}
    .ap-check {{ width:22px; height:22px; min-width:22px; border:2px solid #252538;
                border-radius:50%; margin-top:3px; transition:all .25s;
                background:transparent; flex-shrink:0; position:relative; }}
    .ap-item.ap-done .ap-check {{ background:#C9A84C; border-color:#C9A84C; }}
    .ap-item.ap-done .ap-check::after {{ content:"✓"; position:absolute;
      top:50%; left:50%; transform:translate(-50%,-50%);
      color:#0B0B14; font-size:12px; font-weight:800; }}
    .ap-item.ap-done .ap-text {{ color:#6B7280; text-decoration:line-through; }}
    .ap-text {{ color:#E2E2E2; font-size:0.9rem; line-height:1.6; }}
    .ap-time {{ color:#6B7280; font-size:0.72rem; background:#1e1e30;
               border:1px solid #252538; border-radius:10px;
               padding:2px 9px; display:inline-block; margin-top:5px; }}
    .ap-phase-hdr {{ display:flex; align-items:center; }}
  </style>

  <section id="action">
    <div class="section-header">
      <span class="section-icon">✅</span>
      <span class="section-title">This Week&#39;s Action Plan</span>
      <span class="section-sub">Week {week_num} &nbsp;·&nbsp; {product_name}</span>
    </div>

    <div style="background:#12121F;border:1px solid #252538;border-radius:12px;
                padding:18px 22px;margin-bottom:24px;display:flex;
                align-items:center;gap:20px;flex-wrap:wrap;">
      <div style="flex:1;min-width:180px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
          <span style="color:#E2E2E2;font-size:0.88rem;font-weight:600;">Launch Progress</span>
          <span style="color:#C9A84C;font-size:0.88rem;" id="pt-ap-text">0 of {total_steps} steps complete</span>
        </div>
        <div style="background:#1e1e30;border-radius:6px;height:8px;overflow:hidden;">
          <div id="pt-ap-fill" style="background:linear-gradient(90deg,#C9A84C,#e8c56a);
               height:100%;border-radius:6px;width:0%;transition:width .3s;"></div>
        </div>
      </div>
      <div style="text-align:center;min-width:52px;">
        <div id="pt-ap-pct" style="font-size:1.55rem;font-weight:800;color:#C9A84C;line-height:1;">0%</div>
        <div style="font-size:0.68rem;color:#6B7280;margin-top:2px;">complete</div>
      </div>
    </div>

    {phases_html}
  </section>

  <script>
    (function() {{
      var KEY = 'bell_pt_ap_w{week_num}';
      function save(id, val) {{
        var d = JSON.parse(localStorage.getItem(KEY) || '{{}}');
        d[id] = val; localStorage.setItem(KEY, JSON.stringify(d));
      }}
      window.toggleAP = function(id) {{
        var el = document.querySelector('[data-id="' + id + '"]');
        el.classList.toggle('ap-done');
        save(id, el.classList.contains('ap-done'));
        refresh();
      }};
      function refresh() {{
        var total = document.querySelectorAll('.ap-item').length;
        var done  = document.querySelectorAll('.ap-item.ap-done').length;
        document.getElementById('pt-ap-text').textContent = done + ' of ' + total + ' steps complete';
        var pct = total ? Math.round(done / total * 100) : 0;
        document.getElementById('pt-ap-fill').style.width = pct + '%';
        document.getElementById('pt-ap-pct').textContent  = pct + '%';
      }}
      var saved = JSON.parse(localStorage.getItem(KEY) || '{{}}');
      document.querySelectorAll('.ap-item').forEach(function(el) {{
        if (saved[el.dataset.id]) el.classList.add('ap-done');
      }});
      refresh();
    }})();
  </script>
"""


def _build_etsy_description(product: dict) -> str:
    """Build a ready-to-paste Etsy description for a productivity product."""
    name   = product.get("topic", "")
    fmt    = product.get("format", "printable")
    price  = product.get("price", "$4.99")
    tags   = product.get("etsy_tags", [])
    title  = product.get("etsy_title", name)
    what   = product.get("what_to_build", f"A ready-to-print {fmt}.")

    primary = tags[0] if tags else name.lower()

    lines = []
    lines.append(name + " | Printable PDF | Instant Download")
    lines.append("")
    lines.append(what)
    lines.append("")
    lines.append("─" * 40)
    lines.append("WHAT'S INCLUDED")
    lines.append("─" * 40)
    lines.append("• Format: " + fmt)
    lines.append("• High resolution: 300 dpi — prints sharp at home")
    lines.append("• Size: US Letter (8.5 x 11 in) — easy to resize to A4")
    lines.append("• Instant digital download — no physical item is shipped")
    lines.append("")
    lines.append("─" * 40)
    lines.append("HOW TO DOWNLOAD & PRINT")
    lines.append("─" * 40)
    lines.append("1. Complete your purchase on Etsy")
    lines.append("2. Click the download link in your confirmation email (or go to Etsy > Purchases & Reviews)")
    lines.append("3. Open the PDF on your computer or tablet")
    lines.append("4. Print at home or at a local print shop — standard paper works great")
    lines.append("Print and file in a ring binder, or use as a digital planner on your tablet")
    lines.append("")
    lines.append("─" * 40)
    lines.append("FILE DETAILS")
    lines.append("─" * 40)
    lines.append("• File type: PDF")
    lines.append("• Resolution: 300 dpi")
    lines.append("• Compatible with Adobe Reader (free) and most PDF viewers")
    lines.append("• Digital product only — no physical item will be mailed")
    lines.append("")
    lines.append("─" * 40)
    lines.append("FAQ")
    lines.append("─" * 40)
    lines.append("Q: Can I print multiple copies?")
    lines.append("A: Yes! Your purchase covers unlimited personal-use prints for your household.")
    lines.append("")
    lines.append("Q: Can I print on A4 paper?")
    lines.append("A: Yes — in your print settings, select 'Fit to Page' or 'Scale to A4' and it will resize automatically.")
    lines.append("")
    lines.append("Q: I can't find my download. Help?")
    lines.append("A: Check your Etsy account under Purchases & Reviews, or look for the Etsy confirmation email. Still stuck? Message me and I'll help within 24 hours.")
    lines.append("")
    lines.append("Q: Can I share this file with others?")
    lines.append("A: This file is licensed for personal use only. Please do not redistribute or resell.")
    lines.append("")
    lines.append("─" * 40)
    lines.append("Loved it? A quick review means the world to a small shop and helps other buyers find this resource. Thank you!")
    lines.append("Questions? I respond within 24 hours.")

    return "\n".join(lines)


def _build_modification_prompt(product: dict) -> str:
    """Build a Claude/ChatGPT modification prompt for a productivity product."""
    name  = product.get("topic", "")
    fmt   = product.get("format", "printable")
    price = product.get("price", "$4.99")
    title = product.get("etsy_title", name)
    tags  = product.get("etsy_tags", [])

    tags_str = ", ".join(tags)

    lines = []
    lines.append("I have an Etsy digital printable product with the following details:")
    lines.append("")
    lines.append("Product name: " + name)
    lines.append("Format: " + fmt)
    lines.append("Current price: " + price)
    lines.append("Current Etsy title: " + title)
    lines.append("Current tags: " + tags_str)
    lines.append("")
    lines.append("I want to modify this product as follows:")
    lines.append("[DESCRIBE YOUR CHANGES HERE]")
    lines.append("")
    lines.append("Please return:")
    lines.append("1. Updated Etsy title (max 140 chars; put the primary keyword in the first 30 characters)")
    lines.append("2. All 13 Etsy tags (use synonyms — do NOT repeat words already in the title)")
    lines.append("3. Full Etsy description with: hook sentence, what's included, who it's for, how to download & print, file details, FAQ (4 Q&As), review request")
    lines.append("4. Suggested price (with brief reasoning)")

    return "\n".join(lines)


def _seo_tip_html(product: dict) -> str:
    """Build the SEO Quick-Tips box for a product card (productivity generator)."""
    tags    = product.get("etsy_tags", [])
    title   = product.get("etsy_title", "")
    fmt     = product.get("format", "").lower()
    primary = tags[0] if tags else ""
    first30 = title[:30] if title else ""

    if "flashcard" in fmt:
        category = "Paper &amp; Party Supplies &rarr; Stationery &rarr; Flashcards"
    elif "workbook" in fmt or "worksheet" in fmt:
        category = "Paper &amp; Party Supplies &rarr; Stationery &rarr; Printables"
    elif "planner" in fmt:
        category = "Paper &amp; Party Supplies &rarr; Stationery &rarr; Planner Pages"
    elif "phrasebook" in fmt:
        category = "Books, Movies &amp; Music &rarr; Books &rarr; Language Instruction"
    elif "journal" in fmt:
        category = "Paper &amp; Party Supplies &rarr; Stationery &rarr; Journals"
    else:
        category = "Paper &amp; Party Supplies &rarr; Stationery &rarr; Printables"

    primary_esc = primary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    first30_esc = first30.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    html  = '      <div style="border-left:3px solid #3DD68C;background:#0f1f18;'
    html += 'border-radius:0 8px 8px 0;padding:12px 16px;margin-top:14px;">'
    html += '<div style="color:#3DD68C;font-size:0.75rem;font-weight:700;'
    html += 'text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">'
    html += 'SEO Quick-Tips</div>'
    html += '<div style="display:grid;gap:5px;font-size:0.82rem;">'
    html += '<div><span style="color:#6B7280;">Primary keyword:</span> '
    html += '<span style="color:#E2E2E2;font-weight:600;">' + primary_esc + '</span></div>'
    html += '<div><span style="color:#6B7280;">Title first 30 chars</span> '
    html += '<span style="color:#6B7280;font-size:0.74rem;">(shows on mobile)</span>'
    html += '<span style="color:#6B7280;">:</span> '
    html += '<span style="color:#E2E2E2;font-weight:600;">' + first30_esc + '</span></div>'
    html += '<div><span style="color:#6B7280;">Etsy category:</span> '
    html += '<span style="color:#E2E2E2;">' + category + '</span></div>'
    html += '<div style="color:#6B7280;font-size:0.78rem;margin-top:4px;border-top:1px solid #252538;padding-top:6px;">'
    html += 'Put primary keyword in first 30 title chars. Tags &ne; title words &mdash; use synonyms.</div>'
    html += '</div></div>'
    return html


def _extra_sections_html(product: dict, rank: int, week_num: int) -> str:
    """Build the SEO tip box + collapsible description/prompt section for one product card."""
    card_id = "ex_r" + str(rank) + "_w" + str(week_num)

    desc_raw   = _build_etsy_description(product)
    prompt_raw = _build_modification_prompt(product)

    desc_escaped   = desc_raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    prompt_escaped = prompt_raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    seo_box = _seo_tip_html(product)

    html  = seo_box
    html += '\n      <div style="margin-top:14px;">'
    html += '\n        <button onclick="toggleExtra(\'' + card_id + '\')" '
    html += 'style="background:#C9A84C;color:#0B0B14;border:none;border-radius:8px;'
    html += 'padding:8px 16px;font-size:0.82rem;font-weight:700;cursor:pointer;'
    html += 'display:flex;align-items:center;gap:6px;">'
    html += '&#128203; Listing Description &amp; Modification Tools'
    html += '<span id="' + card_id + '_arrow" style="transition:transform .25s;">&#9660;</span>'
    html += '</button>'
    html += '\n        <div id="' + card_id + '" style="display:none;margin-top:10px;">'
    # ── Tags chips ──
    tags     = product.get("etsy_tags", [])
    tags_csv = ", ".join(tags)
    tags_esc = tags_csv.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html += '\n          <div style="margin-bottom:14px;">'
    html += '\n            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">'
    html += '\n              <div style="color:#3DD68C;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Etsy Tags (' + str(len(tags)) + ')</div>'
    html += '\n              <button onclick="copyTA(\'' + card_id + '_tags\', this)" '
    html += 'style="background:#1e1e30;color:#3DD68C;border:1px solid #3DD68C;border-radius:6px;'
    html += 'padding:4px 10px;font-size:0.75rem;cursor:pointer;">Copy All</button>'
    html += '\n            </div>'
    html += '\n            <div style="display:flex;flex-wrap:wrap;gap:5px;margin-bottom:8px;">'
    for _t in tags:
        _te = _t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html += ('<span style="background:#0f1f18;color:#3DD68C;border:1px solid #3DD68C;'
                 'border-radius:20px;padding:3px 10px;font-size:0.75rem;">' + _te + '</span>')
    html += '</div>'
    html += '\n            <textarea id="' + card_id + '_tags" readonly style="display:none;">' + tags_esc + '</textarea>'
    html += '\n          </div>'


    html += '\n          <div style="margin-bottom:14px;">'
    html += '\n            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">'
    html += '\n              <div style="color:#4EA8DE;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Full Etsy Description</div>'
    html += '\n              <button onclick="copyTA(\'' + card_id + '_desc\', this)" '
    html += 'style="background:#1e1e30;color:#4EA8DE;border:1px solid #4EA8DE;border-radius:6px;'
    html += 'padding:4px 10px;font-size:0.75rem;cursor:pointer;">Copy</button>'
    html += '\n            </div>'
    html += '\n            <textarea id="' + card_id + '_desc" readonly '
    html += 'style="width:100%;min-height:260px;background:#1e1e30;color:#E2E2E2;'
    html += 'border:1px solid #252538;border-radius:8px;padding:12px;font-family:monospace;'
    html += 'font-size:0.8rem;line-height:1.5;resize:vertical;">'
    html += desc_escaped
    html += '</textarea>'
    html += '\n          </div>'

    html += '\n          <div>'
    html += '\n            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">'
    html += '\n              <div style="color:#9B72CF;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Modification Prompt</div>'
    html += '\n              <button onclick="copyTA(\'' + card_id + '_prompt\', this)" '
    html += 'style="background:#1e1e30;color:#9B72CF;border:1px solid #9B72CF;border-radius:6px;'
    html += 'padding:4px 10px;font-size:0.75rem;cursor:pointer;">Copy</button>'
    html += '\n            </div>'
    html += '\n            <textarea id="' + card_id + '_prompt" readonly '
    html += 'style="width:100%;min-height:280px;background:#1e1e30;color:#E2E2E2;'
    html += 'border:1px solid #252538;border-radius:8px;padding:12px;font-family:monospace;'
    html += 'font-size:0.8rem;line-height:1.5;resize:vertical;">'
    html += prompt_escaped
    html += '</textarea>'
    html += '\n          </div>'

    html += '\n        </div>'
    html += '\n      </div>\n'
    return html


def _extra_sections_js() -> str:
    """Return the JS block for toggleExtra and copyTA (injected once per page)."""
    return """  <script>
    window.toggleExtra = function(id) {
      var el = document.getElementById(id);
      var arrow = document.getElementById(id + '_arrow');
      var open = el.style.display === 'block';
      el.style.display = open ? 'none' : 'block';
      if (arrow) arrow.style.transform = open ? '' : 'rotate(180deg)';
    };
    window.copyTA = function(id, btn) {
      var el = document.getElementById(id);
      if (!el) return;
      el.select();
      try { document.execCommand('copy'); } catch(e) {}
      if (btn) {
        var orig = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(function(){ btn.textContent = orig; }, 1500);
      }
    };
  </script>
"""


def build_block1_html(week_in_block: int, week_num: int) -> str:
    """Block 1: read the static base brief, inject progress bar + highlight card + dynamic action plan."""
    with open(BASE_HTML_PATH) as f:
        html = f.read()

    progress = _progress_bar_html(BLOCK1_PRODUCTS, week_in_block, week_num)
    target  = "  </div>\n\n  <!-- ── SECTION 1: COMPETITOR MAP ── -->"
    replace = "  </div>\n" + progress + "  <!-- ── SECTION 1: COMPETITOR MAP ── -->"
    html    = html.replace(target, replace, 1)

    rank_class  = f'class="product-card rank-{week_in_block}"'
    highlighted = (
        f'class="product-card rank-{week_in_block}" '
        'style="box-shadow:0 0 0 2px #C9A84C,0 0 28px rgba(201,168,76,0.18);border-color:#C9A84C;"'
    )
    html = html.replace(rank_class, highlighted, 1)

    # Inject extra sections into each product card
    for rank in range(1, 6):
        product     = BLOCK1_PRODUCTS[rank - 1]
        extras      = _extra_sections_html(product, rank, week_num)
        next_marker = (f'class="product-card rank-{rank + 1}"' if rank < 5
                       else '  <section id="action">')
        next_pos    = html.find(next_marker)
        if next_pos == -1:
            continue
        insert_at   = html.rfind('      </div>\n', 0, next_pos)
        if insert_at == -1:
            continue
        insert_after = insert_at + len('      </div>\n')
        html         = html[:insert_after] + extras + html[insert_after:]

    action_start = html.find('  <section id="action">')
    action_end   = html.find('  </section>', action_start) + len('  </section>')
    product_name = BLOCK1_PRODUCTS[week_in_block - 1]["topic"]
    new_action   = _action_plan_section_html(product_name, week_num)
    html         = html[:action_start] + new_action + html[action_end:]

    # Inject JS once before </body>
    html = html.replace('</body>\n</html>', _extra_sections_js() + '</body>\n</html>')

    return html


def build_block_html(products: list, week_in_block: int, week_num: int, block_num: int) -> str:
    """Build unified brief HTML for Blocks 2+."""
    date_str       = datetime.now().strftime("%B %d, %Y")
    progress_block = _progress_bar_html(products, week_in_block, week_num)
    action_plan    = _action_plan_section_html(products[week_in_block - 1]["topic"], week_num)

    cards_html = ""
    for i, p in enumerate(products):
        rank       = i + 1
        is_current = (rank == week_in_block)
        highlight  = (
            ' style="box-shadow:0 0 0 2px #C9A84C,0 0 28px rgba(201,168,76,0.18);border-color:#C9A84C;"'
            if is_current else ""
        )
        current_badge = (
            '<span style="display:inline-block;background:rgba(201,168,76,0.15);'
            'color:#C9A84C;border:1px solid #C9A84C;border-radius:20px;'
            'padding:2px 10px;font-size:0.72rem;font-weight:700;margin-left:10px;'
            'vertical-align:middle;">▶ THIS WEEK</span>'
            if is_current else ""
        )
        steps_html = "".join(
            f'<div class="step-card"><div class="step-num">{j+1}</div><div class="step-text">{s}</div></div>'
            for j, s in enumerate(p.get("build_steps", []))
        )
        tags_html = "".join(
            f'<span class="etsy-tag">{t}</span>' for t in p.get("etsy_tags", [])
        )
        abs_week   = week_num - week_in_block + rank
        rank_color = RANK_COLORS[i]

        cards_html += f"""
    <div class="product-card rank-{rank}"{highlight}>
      <div class="product-rank">{RANK_EMOJIS[i]}</div>
      <div class="product-name">{p["topic"]}{current_badge}</div>
      <div class="product-meta">
        <span class="meta-chip">Price: <span>{p.get("price", "$4.99")}</span></span>
        <span class="meta-chip">Format: <span>{p.get("format", "")}</span></span>
        <span class="meta-chip" style="border-color:{rank_color};color:{rank_color};">Week {abs_week}</span>
      </div>
      <div class="card" style="margin-bottom:14px;">
        <div class="card-title">What To Build</div>
        <p>{p.get("what_to_build", "")}</p>
      </div>
      <div class="card" style="margin-bottom:14px;">
        <div class="card-title">Why It Sells</div>
        <p>{p.get("why_it_sells", "")}</p>
      </div>
      <div style="margin-bottom:14px;">
        <div class="card-title" style="color:#C9A84C;font-size:0.85rem;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px;">How To Build in Canva</div>
        {steps_html}
      </div>
      <div class="seo-block">
        <div class="seo-label">Etsy Title</div>
        <div class="seo-value">{p.get("etsy_title", "")}</div>
        <div class="tag-row" style="margin-top:10px;">{tags_html}</div>
      </div>
{_extra_sections_html(p, rank, week_num)}    </div>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Productivity & Trackers Brief — Block {block_num} (Weeks {week_num - week_in_block + 1}–{week_num - week_in_block + 5})</title>
<style>
  :root {{
    --bg:#0B0B14; --card:#12121F; --card2:#191928; --border:#252538;
    --gold:#C9A84C; --gold-dim:rgba(201,168,76,0.12);
    --green:#3DD68C; --green-dim:rgba(61,214,140,0.1);
    --accent:#E94560; --blue:#4EA8DE; --purple:#9B72CF;
    --text:#E2E2E2; --muted:#6B7280;
    --tag-bg:rgba(201,168,76,0.14);
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ scroll-behavior:smooth; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,-apple-system,sans-serif; font-size:15px; line-height:1.7; padding:32px 20px 80px; }}
  .container {{ max-width:1060px; margin:0 auto; }}
  .toc {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px 24px; margin-bottom:36px; display:flex; flex-wrap:wrap; gap:10px 24px; align-items:center; }}
  .toc-label {{ color:var(--muted); font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin-right:8px; }}
  .toc a {{ color:var(--gold); text-decoration:none; font-size:0.88rem; }}
  .toc a:hover {{ text-decoration:underline; }}
  .hero {{ background:linear-gradient(135deg,#12121F 0%,#0D1A14 100%); border:1px solid var(--border); border-left:5px solid var(--gold); border-radius:16px; padding:40px 36px; margin-bottom:40px; position:relative; overflow:hidden; }}
  .hero::before {{ content:''; position:absolute; top:-60px; right:-60px; width:220px; height:220px; background:radial-gradient(circle,rgba(61,214,140,0.06) 0%,transparent 70%); border-radius:50%; }}
  .hero-badge {{ color:var(--green); font-size:0.78rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }}
  .hero h1 {{ font-size:2.1rem; color:white; font-weight:800; line-height:1.25; margin-bottom:10px; }}
  .hero .subtitle {{ color:var(--muted); font-size:1rem; margin-bottom:28px; }}
  .hero-stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:16px; border-top:1px solid var(--border); padding-top:24px; }}
  .stat-label {{ color:var(--muted); font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px; }}
  .stat-value {{ color:white; font-size:1.4rem; font-weight:700; margin-top:2px; }}
  .stat-value.gold {{ color:var(--gold); }}
  .stat-value.green {{ color:var(--green); }}
  section {{ margin-bottom:48px; }}
  .section-header {{ display:flex; align-items:center; gap:12px; margin-bottom:20px; padding-bottom:12px; border-bottom:2px solid var(--border); }}
  .section-icon {{ font-size:1.5rem; }}
  .section-title {{ font-size:1.35rem; font-weight:700; color:white; }}
  .section-sub {{ color:var(--muted); font-size:0.88rem; margin-left:auto; }}
  .card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:22px 24px; margin-bottom:14px; }}
  .card-title {{ color:var(--gold); font-weight:600; font-size:0.9rem; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px; }}
  .card p {{ color:var(--text); font-size:0.95rem; }}
  .product-card {{ background:var(--card); border:1px solid var(--border); border-radius:14px; padding:28px; margin-bottom:20px; position:relative; overflow:hidden; }}
  .product-card::before {{ content:''; position:absolute; top:0; left:0; width:4px; height:100%; }}
  .product-card.rank-1::before {{ background:var(--gold); }}
  .product-card.rank-2::before {{ background:#A8A8A8; }}
  .product-card.rank-3::before {{ background:#CD7F32; }}
  .product-card.rank-4::before {{ background:var(--blue); }}
  .product-card.rank-5::before {{ background:var(--purple); }}
  .product-rank {{ font-size:2rem; line-height:1; margin-bottom:8px; }}
  .product-name {{ font-size:1.3rem; font-weight:800; color:white; margin-bottom:6px; }}
  .product-meta {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }}
  .meta-chip {{ background:var(--card2); border:1px solid var(--border); border-radius:20px; padding:4px 12px; font-size:0.8rem; color:var(--text); }}
  .meta-chip span {{ color:var(--gold); font-weight:600; }}
  .step-card {{ background:var(--card2); border:1px solid var(--border); border-radius:10px; padding:12px 16px; margin-bottom:8px; display:flex; gap:14px; align-items:flex-start; }}
  .step-num {{ background:var(--gold); color:#0B0B14; border-radius:50%; width:24px; height:24px; min-width:24px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.8rem; margin-top:2px; }}
  .step-text {{ font-size:0.9rem; color:var(--text); }}
  .seo-block {{ background:var(--card2); border:1px solid var(--border); border-radius:10px; padding:16px; margin-top:14px; }}
  .seo-label {{ color:var(--muted); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }}
  .seo-value {{ color:white; font-weight:600; font-size:0.95rem; }}
  .etsy-tag {{ display:inline-block; background:var(--tag-bg); border:1px solid var(--gold); color:var(--gold); padding:3px 10px; border-radius:20px; font-size:0.76rem; margin:2px; }}
  .footer {{ text-align:center; color:var(--muted); font-size:0.78rem; margin-top:60px; padding-top:20px; border-top:1px solid var(--border); }}
  @media (max-width:768px) {{
    body {{ font-size:14px; padding:16px 12px 60px; }}
    .container {{ max-width:100%; }}
    .hero {{ padding:22px 16px; margin-bottom:20px; }}
    .hero h1 {{ font-size:1.45rem; }}
    .hero .subtitle {{ font-size:0.86rem; }}
    .hero-stats {{ grid-template-columns:repeat(2,1fr); gap:8px; padding-top:16px; }}
    .product-card {{ padding:16px; }}
    .card {{ padding:14px; }}
    .toc {{ gap:6px 12px; padding:12px 14px; }}
    table {{ display:block; overflow-x:auto; width:100%; }}
    .step-card {{ flex-direction:column; gap:8px; }}
  }}
</style>
</head>
<body>
<div class="container">

  <nav class="toc">
    <span class="toc-label">Jump to</span>
    <a href="#products">Top 5 Products</a>
    <a href="#action">Action Plan</a>
  </nav>

  <div class="hero">
    <div class="hero-badge">📊 Productivity & Trackers Brief — Block {block_num}</div>
    <h1>Your Next 5 Products to Build</h1>
    <div class="subtitle">Weeks {week_num - week_in_block + 1}–{week_num - week_in_block + 5} &nbsp;·&nbsp; 5 ready-to-build products with full specs</div>
    <div class="hero-stats">
      <div class="stat">
        <div class="stat-label">Products in Block</div>
        <div class="stat-value gold">5</div>
      </div>
      <div class="stat">
        <div class="stat-label">Current Week</div>
        <div class="stat-value gold">Week {week_num}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Sweet Spot Price</div>
        <div class="stat-value green">$3.99 – $7.99</div>
      </div>
      <div class="stat">
        <div class="stat-label">Generated</div>
        <div class="stat-value" style="font-size:0.95rem;color:var(--muted)">{date_str}</div>
      </div>
    </div>
  </div>

  {progress_block}

  <section id="products">
    <div class="section-header">
      <span class="section-icon">🗂️</span>
      <span class="section-title">5 Products — One Per Week</span>
      <span class="section-sub">Complete specs · ready to open Canva</span>
    </div>

    {cards_html}
  </section>

  {action_plan}

  <div class="footer">
    The Bell Newsletter &nbsp;·&nbsp; Productivity & Trackers Brief &nbsp;·&nbsp; Block {block_num} &nbsp;·&nbsp; {date_str}<br>
    New brief generated every 5 weeks · New topic every Monday
  </div>

</div>
{_extra_sections_js()}</body>
</html>"""


# ── Main entry point ───────────────────────────────────────────────────────────

def run():
    log                      = load_log()
    week_num                 = log["current_week"] + 1
    block_num, week_in_block = get_block_info(week_num)

    print(f"Productivity & Trackers — Week {week_num} (Block {block_num}, position {week_in_block}/5)")

    # ── Block 1 (weeks 1–5): static base brief, no API call ──────────────────
    if block_num == 1:
        product = BLOCK1_PRODUCTS[week_in_block - 1]
        print(f"  Phase 1: {product['topic']}")

        log["current_week"] = week_num
        log["last_run"]     = datetime.now().isoformat()
        log.setdefault("history", []).append({
            "week": week_num, "topic": product["topic"],
            "date": datetime.now().strftime("%Y-%m-%d"), "block": 1,
        })
        save_log(log)

        page = build_block1_html(week_in_block, week_num)
        data = {
            "topic":       product["topic"],
            "format":      product["format"],
            "week_num":    week_num,
            "build_steps": product["build_steps"],
            "price":       product["price"],
            "etsy_title":  product["etsy_title"],
            "etsy_tags":   product["etsy_tags"],
            "brief_url":   BRIEF_URL,
            "block":       1,
        }

    # ── Blocks 2+ (weeks 6, 11, 16 …): generate or reuse block brief ─────────
    else:
        block_state = load_block_state()

        if block_state.get("block_num") == block_num:
            products = block_state["products"]
            print(f"  Reusing block {block_num} brief ({week_in_block}/5)")
        else:
            topics = pick_5_topics(log)
            print(f"  Generating new brief for block {block_num}: {[t['topic'] for t in topics]}")

            client   = Groq(api_key=os.getenv("GROQ_API_KEY"))
            products = generate_block_products(topics, block_num, client)

            for t in topics:
                log["used_topics"].append(t["topic"])

            save_block_state({
                "block_num":      block_num,
                "products":       products,
                "generated_week": week_num,
                "generated_date": datetime.now().strftime("%Y-%m-%d"),
            })

        product = products[week_in_block - 1]
        print(f"  This week: {product['topic']}")

        log["current_week"] = week_num
        log["last_run"]     = datetime.now().isoformat()
        log.setdefault("history", []).append({
            "week":  week_num, "topic": product["topic"],
            "date":  datetime.now().strftime("%Y-%m-%d"), "block": block_num,
        })
        save_log(log)

        page = build_block_html(products, week_in_block, week_num, block_num)
        data = {
            "topic":       product["topic"],
            "format":      product.get("format", ""),
            "week_num":    week_num,
            "build_steps": product.get("build_steps", []),
            "price":       product.get("price", ""),
            "etsy_title":  product.get("etsy_title", ""),
            "etsy_tags":   product.get("etsy_tags", []),
            "brief_url":   BRIEF_URL,
            "block":       block_num,
        }

    BRIEF_PATH.parent.mkdir(exist_ok=True)
    DOCS_PATH.parent.mkdir(exist_ok=True)
    with open(BRIEF_PATH, "w") as f:
        f.write(page)
    with open(DOCS_PATH, "w") as f:
        f.write(page)

    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  Brief → {BRIEF_PATH} + {DOCS_PATH}")
    print(f"  Data  → {DATA_PATH}")
    print(f"  URL   → {BRIEF_URL}")
    return data


if __name__ == "__main__":
    run()
