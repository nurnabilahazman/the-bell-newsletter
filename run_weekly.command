#!/bin/bash
# ============================================================
#  THE BELL — Weekly Newsletter Runner
#  Double-click this file in Finder to run the full pipeline.
#  It will open TWO browser tabs when done:
#    1. This week's Children's Activities build brief
#    2. The newsletter email preview (not sent yet)
# ============================================================

NEWSLETTER_DIR="/Users/nabilahazman/Documents/coding money project/Section 1_Project of the Week/Newsletter"

cd "$NEWSLETTER_DIR" || { echo "ERROR: Can't find the Newsletter folder."; read -n 1; exit 1; }

clear
echo "========================================"
echo "   THE BELL — WEEKLY PIPELINE"
echo "========================================"
echo ""

# ── Step 1: Children's Brief ──────────────────────────────
echo "[ 1 / 6 ]  Picking this week's children's topic..."
python3 tools/children_brief_generator.py
if [ $? -ne 0 ]; then
  echo ""
  echo "ERROR: Children's brief generator failed."
  echo "Check that GROQ_API_KEY is in your .env file."
  echo ""
  read -p "Press Enter to close." dummy; exit 1
fi
echo ""

# ── Step 2: Product Research ──────────────────────────────
echo "[ 2 / 6 ]  Researching product themes (Tavily)..."
python3 tools/research_products.py
if [ $? -ne 0 ]; then
  echo ""
  echo "WARNING: Product research failed. Continuing without it."
  echo "(Newsletter will still generate but Section 2 may be light.)"
  echo ""
fi
echo ""

# ── Step 3: RSS Feeds ────────────────────────────────────
echo "[ 3 / 6 ]  Scraping RSS feeds..."
python3 tools/scrape_rss.py
echo ""

# ── Step 4: Reddit ────────────────────────────────────────
echo "[ 4 / 6 ]  Scraping Reddit..."
python3 tools/scrape_reddit.py
echo ""

# ── Step 5: Draft Newsletter ──────────────────────────────
echo "[ 5 / 6 ]  Drafting newsletter with Groq..."
python3 tools/draft_newsletter.py
if [ $? -ne 0 ]; then
  echo ""
  echo "ERROR: Newsletter draft failed."
  echo "Check that GROQ_API_KEY is in your .env file."
  echo ""
  read -p "Press Enter to close." dummy; exit 1
fi
echo ""

# ── Step 6: Format as HTML Email ─────────────────────────
echo "[ 6 / 6 ]  Formatting as HTML email..."
python3 tools/format_email.py
if [ $? -ne 0 ]; then
  echo ""
  echo "ERROR: Email formatting failed."
  echo ""
  read -p "Press Enter to close." dummy; exit 1
fi
echo ""

# ── Done — open previews ──────────────────────────────────
echo "========================================"
echo "   PIPELINE COMPLETE"
echo "========================================"
echo ""
echo "Opening previews in your browser..."
echo ""

open ".tmp/unified_product_brief.html"
sleep 1
open ".tmp/formatted_email.html"

echo "Two browser tabs just opened:"
echo ""
echo "  TAB 1 →  unified_product_brief.html"
echo "           Your step-by-step build guide for this week's"
echo "           children's activity product. Read this before Canva."
echo ""
echo "  TAB 2 →  formatted_email.html"
echo "           The newsletter PREVIEW — exactly what your"
echo "           subscribers will see. NOT sent yet."
echo ""
echo "────────────────────────────────────────"
echo "  HAPPY WITH THE PREVIEW? SEND IT:"
echo ""
echo "  Open a terminal in the Newsletter folder, then run:"
echo "  python3 tools/send_email.py"
echo ""
echo "  (or run: python3 tools/send_email.py --dry-run first"
echo "   to double-check the subject line and recipients)"
echo "────────────────────────────────────────"
echo ""
read -p "Press Enter to close this window." dummy
