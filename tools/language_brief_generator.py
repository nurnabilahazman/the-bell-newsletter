#!/usr/bin/env python3
"""
Language Learning Weekly Brief Generator

Every 5 weeks a new unified brief is generated (top 5 products for that block).
The same brief is reused for all 5 weeks in the block, with only the progress
bar updating each week to show current position.

Block 1  (weeks  1– 5): static pre-researched products (no API call)
Block 2  (weeks  6–10): generate new brief at week  6, reuse through week 10
Block 3  (weeks 11–15): generate new brief at week 11, reuse through week 15
... and so on.

Run alongside other brief generators (step 1 of pipeline):
  python tools/language_brief_generator.py

State files:
  config/language_topics_log.json   — week counter + topic history
  config/language_block_state.json  — current block products (committed to repo)
  docs/current_language_brief.html  — this week's brief (committed to repo → URL)
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

LOG_PATH         = Path("config/language_topics_log.json")
BLOCK_STATE_PATH = Path("config/language_block_state.json")
BRIEF_PATH       = Path(".tmp/unified_language_brief.html")
DOCS_PATH        = Path("docs/current_language_brief.html")
BASE_HTML_PATH   = Path("docs/unified_product_brief_language_base.html")
DATA_PATH        = Path(".tmp/language_brief_data.json")
MODEL            = "llama-3.3-70b-versatile"
BRIEF_URL        = "https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_language_brief.html"

# Block 1 products — pre-researched, no API call needed
BLOCK1_PRODUCTS = [
    {
        "topic": "Spanish Beginner Vocabulary Flashcards (100 Words)",
        "rank": 1, "format": "PDF flashcards",
        "build_steps": [
            "Open Canva → search 'flashcard template' → pick a clean design with space for a large word and a smaller back panel",
            "Create 100 cards: front = Spanish word (large, centered) + pronunciation in brackets below; back = English translation + example sentence in italics",
            "Color-code by category: nouns (soft blue), verbs (warm coral), adjectives (muted green) — add a small dot in the top corner",
            "Add a 'How to study' bonus page explaining the spaced repetition method in 5 simple steps",
            "Export as PDF Print → also export a '4-cards-per-page' layout as a second file for paper-saving printing",
        ],
        "price": "$4.99",
        "etsy_title": "Spanish Vocabulary Flashcards Beginner | 100 Words | Printable PDF | Instant Download",
        "etsy_tags": ["spanish flashcards", "spanish vocabulary", "learn spanish", "spanish printable", "spanish beginner", "vocabulary cards", "language learning"],
        "what_to_build": "100 double-sided flashcards covering core beginner Spanish vocabulary across 8 categories (greetings, numbers, food, colors, family, body, verbs, adjectives). Each card has the Spanish word + pronunciation on the front and English + an example sentence on the back.",
        "why_it_sells": "Spanish is the #1 most-studied language on Etsy — beginner vocabulary flashcards are a top-10 printable category with consistent year-round demand.",
    },
    {
        "topic": "Japanese Hiragana Practice Sheets",
        "rank": 2, "format": "PDF worksheets",
        "build_steps": [
            "Open Canva → search 'handwriting practice worksheet' → pick a clean grid-based template",
            "Create 46 pages (one per hiragana character): large model character top-left with numbered stroke order, then 6 dotted-trace boxes, then 6 blank practice boxes",
            "Add the romaji pronunciation and 2 example words using that character at the bottom of each page",
            "Use Noto Sans JP font for the character — test it prints clearly at 72pt before building all 46 pages",
            "Include a 2-page hiragana reference chart as a bonus: all 46 characters in a grid with romaji below each",
        ],
        "price": "$3.99",
        "etsy_title": "Japanese Hiragana Practice Sheets | 46 Characters + Stroke Order | Printable PDF Worksheet",
        "etsy_tags": ["hiragana practice", "japanese writing", "hiragana worksheet", "learn japanese", "japanese printable", "stroke order", "hiragana chart"],
        "what_to_build": "48 pages: 46 character practice sheets with stroke-order guide, trace lines, and blank practice boxes, plus a 2-page full hiragana reference chart. Covers the complete hiragana syllabary for absolute beginners.",
        "why_it_sells": "Japanese is the fastest-growing language learning niche on Etsy — hiragana is the first step every beginner takes, and practice sheet searches are consistent and high-volume.",
    },
    {
        "topic": "French Grammar Cheat Sheets (10 Essential Rules)",
        "rank": 3, "format": "PDF reference sheets",
        "build_steps": [
            "Open Canva → search 'cheat sheet template' → pick a clean, information-dense single-page layout",
            "Create 10 pages (one per grammar rule): present tense conjugation, gender + articles, adjective agreement, negation, question formation, past tense (passé composé), future tense, pronouns, prepositions, and common irregular verbs",
            "Each page: rule headline → formula in a colored box → 5 example sentences in a table → 'common mistake to avoid' callout box",
            "Use a clean academic color scheme: dark navy, white, gold accent — feels premium and study-worthy",
            "Add a double-sided summary card (A5 size) as a bonus page — buyers can print it separately and keep it on their desk",
        ],
        "price": "$5.99",
        "etsy_title": "French Grammar Cheat Sheets | 10 Essential Rules | Study Guide | Printable PDF Instant Download",
        "etsy_tags": ["french grammar", "french cheat sheet", "learn french", "french study guide", "french printable", "grammar reference", "french conjugation"],
        "what_to_build": "10 single-page reference sheets covering the most essential French grammar rules, each with the rule, formula, examples, and a common mistake callout. Plus a bonus double-sided summary card.",
        "why_it_sells": "Grammar reference sheets are a high-perceived-value product — buyers pay more because they feel like a study resource, not just a flashcard, and they get used repeatedly over months of study.",
    },
    {
        "topic": "Korean Hangul Writing Practice Workbook",
        "rank": 4, "format": "PDF workbook",
        "build_steps": [
            "Open Canva → search 'handwriting practice worksheet' → pick a clean grid template",
            "Create 40 pages: 24 consonant pages + 10 vowel pages + 6 combination practice pages — each with stroke order, trace lines, blank practice grid, and romanisation",
            "Use Noto Sans KR font for all Korean characters — test at 72pt that every character is distinct and clear when printed",
            "Add a 2-page 'Complete Hangul Chart' reference at the front showing all characters with their romanised sounds",
            "Include 5 bonus pages of common beginner words to practice writing (annyeong, gamsahamnida, etc.)",
        ],
        "price": "$4.99",
        "etsy_title": "Korean Hangul Practice Workbook | Writing Sheets + Stroke Order | Printable PDF Instant Download",
        "etsy_tags": ["hangul practice", "korean writing", "hangul worksheet", "learn korean", "korean printable", "hangul workbook", "korean alphabet"],
        "what_to_build": "A 47-page workbook covering all 40 Hangul characters with stroke-order guides, trace lines, blank practice grids, and a romanisation key. Includes a full Hangul reference chart and 5 pages of common beginner words.",
        "why_it_sells": "Korean is the second-fastest growing language niche on Etsy, driven by K-pop and K-drama interest — Hangul writing practice is the entry point for most beginners and consistently tops language learning searches.",
    },
    {
        "topic": "Travel Phrasebook — 5 Languages (Spanish, French, Italian, German, Portuguese)",
        "rank": 5, "format": "PDF phrasebook",
        "build_steps": [
            "Open Canva → search 'booklet template' → pick a compact, travel-guide-style layout (A5 or half-letter size)",
            "Create 5 sections (one per language): Greetings, Numbers, Directions, Restaurant/Food, Shopping, Emergency, Hotel — 10 phrases per topic per language",
            "Add pronunciation in brackets after each phrase (IPA not needed — use approximate English sounds, e.g. 'SAY: bon-ZHOOR')",
            "Design a 'Quick Reference Card' single page per language — top 20 most essential phrases only — that buyers can print, fold, and carry in a wallet",
            "Export as PDF Print → also offer a compact 'wallet card' export at A6 size as a second file",
        ],
        "price": "$6.99",
        "etsy_title": "Travel Phrasebook Printable | 5 Languages Spanish French Italian German Portuguese | Instant Download",
        "etsy_tags": ["travel phrasebook", "language phrases", "travel printable", "phrasebook printable", "travel essentials", "language guide", "europe travel"],
        "what_to_build": "A 40+ page compact phrasebook covering 5 European languages across 7 travel scenarios (50 phrases per language = 250 phrases total), plus a wallet-sized quick reference card for each language.",
        "why_it_sells": "Multi-language travel phrasebooks have a distinct buyer (pre-trip travelers) who searches for them in spring/summer — the 5-language bundle justifies a higher price and competes well against single-language products.",
    },
]

# 48-topic pool for blocks 2+ (Groq-generated briefs pick 5 at a time)
ALL_TOPICS = [
    {"topic": "Spanish Verb Conjugation Charts (Present, Past, Future)",  "language": "Spanish",   "format": "PDF reference sheets"},
    {"topic": "Spanish 200-Word Intermediate Vocabulary Flashcards",      "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "Spanish Body Parts Flashcards",                            "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "Spanish Food and Drink Vocabulary Cards",                  "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "DELE A1/A2 Vocabulary Study Pack",                         "language": "Spanish",   "format": "PDF study pack"},
    {"topic": "Japanese Katakana Practice Sheets",                        "language": "Japanese",  "format": "PDF worksheets"},
    {"topic": "JLPT N5 Vocabulary Flashcards (800 Words)",                "language": "Japanese",  "format": "PDF flashcards"},
    {"topic": "Japanese Numbers and Counters Reference Sheet",            "language": "Japanese",  "format": "PDF reference sheet"},
    {"topic": "Japanese Kanji N5 Practice Workbook",                      "language": "Japanese",  "format": "PDF workbook"},
    {"topic": "Japanese Beginner Grammar Cheat Sheets",                   "language": "Japanese",  "format": "PDF reference sheets"},
    {"topic": "Korean TOPIK 1 Vocabulary Flashcards",                     "language": "Korean",    "format": "PDF flashcards"},
    {"topic": "Korean Numbers (Native + Sino) Reference Sheet",           "language": "Korean",    "format": "PDF reference sheet"},
    {"topic": "Korean Grammar Patterns Beginner Cheat Sheet",             "language": "Korean",    "format": "PDF reference sheet"},
    {"topic": "Korean Food Vocabulary Flashcards",                        "language": "Korean",    "format": "PDF flashcards"},
    {"topic": "K-Drama Phrases Flashcard Set",                            "language": "Korean",    "format": "PDF flashcards"},
    {"topic": "French Vocabulary Flashcards — 100 Core Words",            "language": "French",    "format": "PDF flashcards"},
    {"topic": "French Verb Conjugation Cheat Sheet",                      "language": "French",    "format": "PDF reference sheet"},
    {"topic": "French Numbers and Days of the Week Flashcards",           "language": "French",    "format": "PDF flashcards"},
    {"topic": "DELF A1/A2 Vocabulary Study Pack",                         "language": "French",    "format": "PDF study pack"},
    {"topic": "French Adjectives and Agreement Reference Sheet",          "language": "French",    "format": "PDF reference sheet"},
    {"topic": "Mandarin Chinese Pinyin Practice Worksheets",              "language": "Mandarin",  "format": "PDF worksheets"},
    {"topic": "HSK 1 Vocabulary Flashcards (150 Words)",                  "language": "Mandarin",  "format": "PDF flashcards"},
    {"topic": "Mandarin Tones Practice Sheet",                            "language": "Mandarin",  "format": "PDF reference sheet"},
    {"topic": "Chinese Numbers and Counting Flashcards",                  "language": "Mandarin",  "format": "PDF flashcards"},
    {"topic": "Italian Beginner Vocabulary Flashcards",                   "language": "Italian",   "format": "PDF flashcards"},
    {"topic": "Italian Verb Conjugation Reference Sheet",                 "language": "Italian",   "format": "PDF reference sheet"},
    {"topic": "German Beginner Vocabulary Flashcards",                    "language": "German",    "format": "PDF flashcards"},
    {"topic": "German Grammar Cases Cheat Sheet (Nominativ/Akkusativ)",   "language": "German",    "format": "PDF reference sheet"},
    {"topic": "German der/die/das Article Flashcards",                    "language": "German",    "format": "PDF flashcards"},
    {"topic": "Arabic Alphabet Writing Practice Sheets",                  "language": "Arabic",    "format": "PDF worksheets"},
    {"topic": "Arabic Beginner Vocabulary Flashcards",                    "language": "Arabic",    "format": "PDF flashcards"},
    {"topic": "Portuguese Beginner Vocabulary Flashcards",                "language": "Portuguese","format": "PDF flashcards"},
    {"topic": "Russian Cyrillic Alphabet Practice Sheets",                "language": "Russian",   "format": "PDF worksheets"},
    {"topic": "Russian Beginner Vocabulary Flashcards",                   "language": "Russian",   "format": "PDF flashcards"},
    {"topic": "Language Learning Planner (30-Day Study Schedule)",        "language": "Any",       "format": "PDF planner"},
    {"topic": "Vocabulary Journal (Blank Template)",                      "language": "Any",       "format": "PDF journal"},
    {"topic": "Language Study Habit Tracker",                             "language": "Any",       "format": "PDF printable"},
    {"topic": "Bilingual Spanish-English Flashcards for Kids",            "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "Bilingual French-English Flashcards for Kids",             "language": "French",    "format": "PDF flashcards"},
    {"topic": "Bilingual Mandarin-English Flashcards for Kids",           "language": "Mandarin",  "format": "PDF flashcards"},
    {"topic": "GCSE Spanish Revision Flashcard Pack",                     "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "GCSE French Vocabulary Revision Cards",                    "language": "French",    "format": "PDF flashcards"},
    {"topic": "IB Spanish Vocabulary Study Pack",                         "language": "Spanish",   "format": "PDF study pack"},
    {"topic": "Italian Travel Phrasebook",                                "language": "Italian",   "format": "PDF phrasebook"},
    {"topic": "Japanese Travel Phrasebook",                               "language": "Japanese",  "format": "PDF phrasebook"},
    {"topic": "Korean Travel Phrasebook",                                 "language": "Korean",    "format": "PDF phrasebook"},
    {"topic": "Latin American Spanish Slang Flashcards",                  "language": "Spanish",   "format": "PDF flashcards"},
    {"topic": "Spanish Irregular Verbs Flashcard Set",                    "language": "Spanish",   "format": "PDF flashcards"},
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
        f"{i+1}. {t['topic']} (Language: {t.get('language','')}, {t['format']})"
        for i, t in enumerate(topics)
    )
    prompt = f"""You are writing product specs for a solo digital products creator selling language learning printables on Etsy.
Generate exactly 5 product briefs for these Language Learning products (Block {block_num}):

{topics_str}

Return ONLY a valid JSON array of 5 objects. No markdown, no code fences:
[
  {{
    "topic": "exact topic name",
    "language": "target language",
    "format": "format type",
    "price": "$4.99",
    "etsy_title": "Keyword-rich title, max 140 chars, include language name and product type",
    "etsy_tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"],
    "build_steps": [
      "Open Canva → search relevant template → pick clean academic or pastel design",
      "Step 2 starting with action verb, specific to this product and language",
      "Step 3 — include language-specific detail (font recommendation, pronunciation note, etc.)",
      "Step 4",
      "Export as PDF Print → upload to Etsy as a digital download"
    ],
    "what_to_build": "2 sentences: exactly what cards/pages the product contains and what the learner does with it.",
    "why_it_sells": "1 sentence: who buys it, when, and why it converts on Etsy."
  }}
]

Rules:
- Exactly 5 objects in the same order as the input list
- price: $3.99–$7.99 (reference packs/bundles can go up to $7.99)
- build_steps: exactly 5 steps, action verb first, highly specific to EACH product including font recommendations for non-Latin scripts (use Noto font family)
- etsy_tags: exactly 7 tags, each under 20 characters, what language learners actually search on Etsy
- All content specific to each individual product — no generic filler
- For non-Latin scripts: always recommend Noto Sans/Serif fonts and mention testing character rendering
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
        p["rank"]     = i + 1
        p["format"]   = topics[i]["format"]
        p["language"] = topics[i].get("language", "")
    return products


# ── HTML builders ──────────────────────────────────────────────────────────────

RANK_COLORS = ["var(--gold)", "#A8A8A8", "#CD7F32", "var(--blue)", "var(--purple)"]
RANK_EMOJIS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]


def _progress_bar_html(products: list, week_in_block: int, week_num: int) -> str:
    steps_html       = ""
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
                 "Note each one's price, card/page count, review count, and thumbnail style. "
                 "This is your competitive landscape before you build anything.",
                 "~30 min"),
                ("Click the top 2–3 bestsellers and read ALL their 1–3 star reviews. "
                 "Common language product complaints: 'font too hard to read', 'not enough example sentences', "
                 "'wish it had pronunciation guides', 'too basic'. "
                 "Each complaint is a gap your product can fill.",
                 "~15 min"),
                ("Open Pinterest, search the same keyword, save 10–15 images to a mood-board folder in Canva: "
                 "card layouts, color schemes, fonts for the target script, styles that feel study-worthy and approachable.",
                 "~15 min"),
            ],
        },
        {
            "phase": "Plan Before You Open Canva",
            "icon": "📝",
            "color": "#9B72CF",
            "steps": [
                ("Write your complete content list before touching Canva — e.g. "
                 "<em>100 vocabulary cards: front = word + pronunciation, back = English + example sentence; "
                 "bonus: 2-page reference chart + study tips page</em>. "
                 "Target <strong>50+ cards or 20+ pages minimum</strong> — buyers compare counts in reviews.",
                 "~15 min"),
                ("For non-Latin scripts (Japanese, Korean, Arabic, Chinese): "
                 "open Canva NOW and test your chosen Noto font at your target print size. "
                 "Type 5 sample characters and export a test page → confirm every character renders correctly and legibly. "
                 "Fix the font before building 50 cards, not after.",
                 "~10 min"),
            ],
        },
        {
            "phase": "Build in Canva",
            "icon": "🎨",
            "color": "#C9A84C",
            "steps": [
                ("Open Canva → follow the 5 build steps in the brief above → "
                 "work through every card or page on your content list in order. "
                 "Duplicate pages/cards rather than creating from scratch — one layout change propagates everywhere.",
                 "2–4 hrs"),
                ("Proof every card/page before exporting: consistent fonts, foreign characters rendering correctly, "
                 "pronunciation guides accurate, example sentences grammatically correct (use DeepL or a native speaker check for key sentences). "
                 "Fix everything now.",
                 "~20 min"),
                ('<strong>Export as "PDF Print"</strong> (not "Standard PDF"). '
                 "PDF Print preserves 300 dpi — foreign script characters that look fine on screen can become blurry at Standard quality. "
                 "If making flashcards, also export a '4-up per page' version as a second file.",
                 "~5 min"),
            ],
        },
        {
            "phase": "Create Listing Images",
            "icon": "📸",
            "color": "#3DD68C",
            "steps": [
                ("<strong>Thumbnail first.</strong> "
                 "Language learning thumbnails that convert show the foreign script prominently — "
                 "a buyer searching 'Japanese flashcards' needs to immediately see Japanese characters. "
                 "Add text callouts: card/page count, language name, 'Instant Download'. "
                 "Test it: does your thumbnail clearly signal the language before a buyer can read the text?",
                 "~30 min"),
                ("Create 4–6 supporting images: 2 card/page samples showing front AND back, "
                 "1 lifestyle mockup (cards spread on a desk with a highlighter — use Canva's mockup feature or Placeit.net free tier), "
                 "1 'What's included' overview page, 1 close-up showing the foreign script clearly at full size.",
                 "~30 min"),
            ],
        },
        {
            "phase": "Publish on Etsy",
            "icon": "🚀",
            "color": "#E94560",
            "steps": [
                ("Create your Etsy listing. <strong>Paste the Etsy title exactly as shown</strong> in the brief. "
                 "Description: lead with what's included and card/page count, then how to download and print, then FAQs. "
                 "Use all 7 tags from the brief plus 6 more variations (aim for all 13 Etsy slots).",
                 "~25 min"),
                ("Set your launch price, upload all images (thumbnail first) and your PDF. Hit Publish. "
                 "Then: test-download your own listing → open the PDF → confirm all foreign characters render correctly in the downloaded file.",
                 "~15 min"),
            ],
        },
        {
            "phase": "Promote & Grow",
            "icon": "📈",
            "color": "#4EA8DE",
            "steps": [
                ("Post 2–3 Pinterest pins linking to your Etsy listing. "
                 "Pin to boards like 'Language Learning Resources', 'Learn [Language]', 'Study Printables'. "
                 "Language learners are also active on Reddit — share a genuine free sample page in the relevant subreddit "
                 "(r/languagelearning, r/LearnSpanish, r/LearnJapanese) as a resource to drive organic traffic.",
                 "~20 min"),
                ("After your first sale, message the buyer: "
                 "<em>\"Thanks so much! Hope the [product name] is helpful for your [language] studies. "
                 "If you have a moment, a review means everything to a small shop 🙏\"</em>",
                 "~2 min"),
                ("At the 2-week mark: Etsy Stats → Search Terms. "
                 "Language products often rank for the specific language name + product type. "
                 "If you see searches for a related language (e.g., you sell Spanish flashcards but people find you searching 'French flashcards') "
                 "— that's your next product to build.",
                 "~15 min"),
            ],
        },
    ]

    total_steps = sum(len(p["steps"]) for p in phases)

    phases_html = ""
    step_num    = 0
    for ph in phases:
        color      = ph["color"]
        items_html = ""
        for text, time_est in ph["steps"]:
            step_num += 1
            item_id   = "ll_ap_w" + str(week_num) + "_s" + str(step_num)
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
  <!-- DYNAMIC ACTION PLAN — injected by language_brief_generator.py -->
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
          <span style="color:#C9A84C;font-size:0.88rem;" id="ll-ap-text">0 of {total_steps} steps complete</span>
        </div>
        <div style="background:#1e1e30;border-radius:6px;height:8px;overflow:hidden;">
          <div id="ll-ap-fill" style="background:linear-gradient(90deg,#C9A84C,#e8c56a);
               height:100%;border-radius:6px;width:0%;transition:width .3s;"></div>
        </div>
      </div>
      <div style="text-align:center;min-width:52px;">
        <div id="ll-ap-pct" style="font-size:1.55rem;font-weight:800;color:#C9A84C;line-height:1;">0%</div>
        <div style="font-size:0.68rem;color:#6B7280;margin-top:2px;">complete</div>
      </div>
    </div>

    {phases_html}
  </section>

  <script>
    (function() {{
      var KEY = 'bell_ll_ap_w{week_num}';
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
        document.getElementById('ll-ap-text').textContent = done + ' of ' + total + ' steps complete';
        var pct = total ? Math.round(done / total * 100) : 0;
        document.getElementById('ll-ap-fill').style.width = pct + '%';
        document.getElementById('ll-ap-pct').textContent  = pct + '%';
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
    """Build a ready-to-paste Etsy description for a language learning product."""
    name   = product.get("topic", "")
    fmt    = product.get("format", "printable")
    price  = product.get("price", "$4.99")
    tags   = product.get("etsy_tags", [])
    title  = product.get("etsy_title", name)
    what   = product.get("what_to_build", f"A ready-to-print {fmt}.")
    lang   = product.get("language", "")

    primary  = tags[0] if tags else name.lower()
    lang_str = f" for {lang}" if lang else ""

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
    lines.append("Print and cut out flashcards, or study from the screen on your tablet")
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
    lines.append("A: Yes! Your purchase covers unlimited personal-use prints.")
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
    lines.append("Loved it? A quick review means the world to a small shop and helps other learners find this resource. Thank you!")
    lines.append("Questions? I respond within 24 hours.")

    return "\n".join(lines)


def _build_modification_prompt(product: dict) -> str:
    """Build a Claude/ChatGPT modification prompt for a language learning product."""
    name  = product.get("topic", "")
    fmt   = product.get("format", "printable")
    price = product.get("price", "$4.99")
    title = product.get("etsy_title", name)
    tags  = product.get("etsy_tags", [])
    lang  = product.get("language", "")

    tags_str = ", ".join(tags)
    lang_line = f"Language: {lang}\n" if lang else ""

    lines = []
    lines.append("I have an Etsy digital printable product with the following details:")
    lines.append("")
    lines.append("Product name: " + name)
    lines.append(lang_line.rstrip())
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
    """Build the SEO Quick-Tips box for a product card (language generator)."""
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

    html += '\n          <div style="margin-bottom:14px;">'
    html += '\n            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">'
    html += '\n              <div style="color:#4EA8DE;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">Full Etsy Description</div>'
    html += '\n              <button onclick="copyTA(\'' + card_id + '_desc\')" '
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
    html += '\n              <button onclick="copyTA(\'' + card_id + '_prompt\')" '
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
    window.copyTA = function(id) {
      var el = document.getElementById(id);
      if (!el) return;
      navigator.clipboard.writeText(el.value).catch(function() {
        el.select(); document.execCommand('copy');
      });
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
        tags_html  = "".join(
            f'<span class="etsy-tag">{t}</span>' for t in p.get("etsy_tags", [])
        )
        abs_week   = week_num - week_in_block + rank
        rank_color = RANK_COLORS[i]
        lang_chip  = (
            f'<span class="meta-chip" style="border-color:#4EA8DE;color:#4EA8DE;">'
            f'Lang: <span style="color:#4EA8DE;">{p.get("language","")}</span></span>'
            if p.get("language") else ""
        )

        cards_html += f"""
    <div class="product-card rank-{rank}"{highlight}>
      <div class="product-rank">{RANK_EMOJIS[i]}</div>
      <div class="product-name">{p["topic"]}{current_badge}</div>
      <div class="product-meta">
        <span class="meta-chip">Price: <span>{p.get("price", "$4.99")}</span></span>
        <span class="meta-chip">Format: <span>{p.get("format", "")}</span></span>
        {lang_chip}
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
<title>Language Learning Brief — Block {block_num} (Weeks {week_num - week_in_block + 1}–{week_num - week_in_block + 5})</title>
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
  .hero {{ background:linear-gradient(135deg,#12121F 0%,#0D1220 100%); border:1px solid var(--border); border-left:5px solid var(--gold); border-radius:16px; padding:40px 36px; margin-bottom:40px; position:relative; overflow:hidden; }}
  .hero::before {{ content:''; position:absolute; top:-60px; right:-60px; width:220px; height:220px; background:radial-gradient(circle,rgba(78,168,222,0.07) 0%,transparent 70%); border-radius:50%; }}
  .hero-badge {{ color:var(--blue); font-size:0.78rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }}
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
    <div class="hero-badge">📚 Language Learning Brief — Block {block_num}</div>
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
      <span class="section-icon">📖</span>
      <span class="section-title">5 Products — One Per Week</span>
      <span class="section-sub">Complete specs · ready to open Canva</span>
    </div>

    {cards_html}
  </section>

  {action_plan}

  <div class="footer">
    The Bell Newsletter &nbsp;·&nbsp; Language Learning Brief &nbsp;·&nbsp; Block {block_num} &nbsp;·&nbsp; {date_str}<br>
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

    print(f"Language Learning — Week {week_num} (Block {block_num}, position {week_in_block}/5)")

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
            "language":    product.get("language", ""),
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
            "language":    product.get("language", ""),
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
