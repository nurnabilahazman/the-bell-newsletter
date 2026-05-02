# Workflow: Weekly Newsletter Pipeline

## Objective
Produce and send a weekly personal finance newsletter by scraping RSS feeds and Reddit, drafting with Claude, formatting as HTML, sending via Gmail, and logging the edition to Google Sheets.

## Required Inputs
- `.env` file with all keys populated (see `.env` for the full list)
- `credentials.json` in project root (Google Service Account for Sheets)
- Subscribers added to `RECIPIENT_EMAILS` in `.env`

## Expected Outputs
- Email delivered to all recipients in `RECIPIENT_EMAILS`
- New row appended to Google Sheet logging this edition

## Intermediate Files (all in `.tmp/`, regenerated each run)
| File | Produced By | Consumed By |
|---|---|---|
| `unified_product_brief.html` | `children_brief_generator.py` | You (open in browser) |
| `children_brief_data.json` | `children_brief_generator.py` | `draft_newsletter.py` |
| `rss_content.json` | `scrape_rss.py` | `draft_newsletter.py` |
| `reddit_content.json` | `scrape_reddit.py` | `draft_newsletter.py` |
| `draft.md` | `draft_newsletter.py` | `format_email.py`, `send_email.py`, `log_to_sheets.py` |
| `formatted_email.html` | `format_email.py` | `send_email.py` |

## Persistent Files (survive across runs)
| File | Purpose |
|---|---|
| `config/children_topics_log.json` | Tracks which children's topics have been used (no-repeat system) |

---

## Steps

### Step 0 — Generate Children's Brief (NEW — run this first)
```bash
python tools/children_brief_generator.py
```
- Picks this week's children's activity topic from a list of 52 (no repeats)
- Updates `config/children_topics_log.json` with the used topic
- Output: `.tmp/unified_product_brief.html` (open in browser — your weekly build guide)
- Output: `.tmp/children_brief_data.json` (passes topic to draft_newsletter.py)
- If all 52 topics are used, the list resets automatically

### Step 1 — Scrape RSS Feeds
```bash
python tools/scrape_rss.py
```
- Pulls latest articles from feeds listed in `RSS_FEEDS` (.env)
- Output: `.tmp/rss_content.json`
- If a feed fails, it logs a WARNING and continues — not a blocker

### Step 2 — Scrape Reddit
```bash
python tools/scrape_reddit.py
```
- Pulls top posts from r/personalfinance, r/investing, r/financialindependence
- Uses Reddit's public JSON API (no auth required)
- Output: `.tmp/reddit_content.json`
- Includes a 1-second delay between subreddits to avoid rate limiting

### Step 3 — Draft Newsletter with Claude
```bash
python tools/draft_newsletter.py
```
- Reads both `.tmp/*.json` files and calls Claude (`claude-sonnet-4-6`)
- Output: `.tmp/draft.md`
- **Review the draft before proceeding.** Open `.tmp/draft.md` and check:
  - Are the stories accurate and relevant?
  - Are the links real (not hallucinated)?
  - Is the tone right?
- Edit `.tmp/draft.md` manually if needed before continuing

### Step 4 — Format as HTML Email
```bash
python tools/format_email.py
```
- Converts `.tmp/draft.md` to a mobile-friendly HTML email
- Output: `.tmp/formatted_email.html`
- Open in a browser to preview before sending

### Step 5 — Send Email
```bash
# Dry run first (always recommended)
python tools/send_email.py --dry-run

# Send for real
python tools/send_email.py
```
- Sends via Gmail SMTP using App Password
- Recipients from `RECIPIENT_EMAILS` in `.env`
- Subject extracted automatically from the draft H1

### Step 6 — Log to Google Sheets
```bash
python tools/log_to_sheets.py
```
- Appends one row: Date, Subject, RSS count, Reddit count, Word count, Status
- Requires `credentials.json` and `GOOGLE_SHEET_ID` in `.env`

---

## Running It All at Once
```bash
python tools/children_brief_generator.py && \
python tools/research_products.py && \
python tools/scrape_rss.py && \
python tools/scrape_reddit.py && \
python tools/draft_newsletter.py && \
python tools/format_email.py && \
python tools/send_email.py --dry-run
```
Review the dry run, then send for real:
```bash
python tools/send_email.py && python tools/log_to_sheets.py
```
After running: open `.tmp/unified_product_brief.html` in your browser — this week's children's activity build guide.

---

## Edge Cases & Known Quirks

**RSS feed returns no articles**
- Check the feed URL is still valid (feeds change or die)
- Update `RSS_FEEDS` in `.env` with a working replacement
- The script will still proceed with whatever articles it got

**Reddit rate limiting (429 error)**
- Reddit's public API allows ~60 requests/min for unauthenticated traffic
- The 1-second sleep between subreddits prevents this for normal use
- If you hit it anyway, wait 1 minute and re-run `scrape_reddit.py`

**Claude produces hallucinated links**
- Always review `.tmp/draft.md` before sending
- Check that every link in "Top Stories" and "Reddit Pulse" matches a real URL from the source data
- If a link looks wrong, fix it manually in the draft

**Gmail SMTP auth failure**
- Make sure you're using an App Password, not your regular Gmail password
- Generate one at: Google Account → Security → 2-Step Verification → App passwords
- `GMAIL_APP_PASSWORD` should be the 16-character code (no spaces)

**Google Sheets: "File not found" error**
- Make sure you've shared the sheet with your service account email
- The service account email is in `credentials.json` under `client_email`
- Share the sheet with that email as Editor

---

## First-Time Setup Checklist
- [ ] Fill in all keys in `.env`
- [ ] Generate Gmail App Password and add to `.env`
- [ ] Create Google Cloud project, enable Sheets API, download `credentials.json`
- [ ] Share your tracking Google Sheet with the service account email
- [ ] Add `GOOGLE_SHEET_ID` (from the sheet URL) to `.env`
- [ ] Install dependencies: `pip install feedparser requests anthropic gspread google-auth python-dotenv`
- [ ] Run a dry-run end-to-end to verify everything works

## Install Dependencies
```bash
pip install feedparser requests anthropic gspread google-auth python-dotenv
```
