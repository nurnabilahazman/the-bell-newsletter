# The Bell — Week 2 · May 03, 2026

>>>TAGLINE
Build. Ship. Earn.
>>>END

## 🛠️ SECTION 1 — Project of the Week

**Week 2 of 12: Web Scraper → Google Sheets**

*Data collection*

Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.

>>>PROMPT
You are helping me build a Python web scraper that saves data directly into Google Sheets. Here is exactly what I need:

1. The scraper should accept a URL as input
2. It should extract: page title, all headings (H1, H2, H3), all paragraph text, and all links
3. It should save this data into a Google Sheet with columns: URL, Title, Heading, Content, Link, Date Scraped
4. Use these libraries: requests, BeautifulSoup4, gspread, google-auth, python-dotenv
5. Credentials come from a credentials.json file (Google Service Account)
6. The Sheet ID comes from an environment variable GOOGLE_SHEET_ID in a .env file
7. Handle errors gracefully — if a page fails to load, log the error and continue
8. Add a 1-second delay between requests to avoid getting blocked

Please:
a) Write the complete Python script
b) List every pip install command I need to run
c) Tell me exactly what I need to set up in Google Cloud Console to make this work
d) Show me how to run it with a real example URL
e) Tell me the 3 most common errors I might hit and how to fix them
>>>END

>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section1_projects_guide.md
How to work with Claude on projects, common errors, and the 12-week learning arc.
>>>END

---

## 📦 SECTION 2 — 3 Products to Build This Week

One product per theme. Research done. Prompt ready. Just paste and create.

### 🗂️ Productivity & Trackers

**This week's product:** Paycheck-to-Paycheck Budget Tracker

**Store inspiration:** [2024 2025 Budget Spreadsheet — This product sells well due to its comprehensive and dynamic tracking features, making it easy for customers to organize their finances](https://www.etsy.com/market/2024_2025_budget_spreadsheet)

**What buyers love:**
- Easy to use
- Customizable
- Affordable

**Your edge — make it better:**
- Automated expense categorization
- Integrated savings goals
- Visual spending trend analysis

**How to build it in Canva:**
1. Open Canva → search 'daily planner template' → pick a clean design with a top-priorities section
2. Create one master daily page with: date, top 3 priorities, hourly schedule (6am–10pm), notes, water tracker, gratitude line
3. Add a weekly overview page (Mon–Sun at a glance + weekly goal)
4. Create a 365-day set: duplicate the daily page 365× — or sell a 90-day version (more affordable)
5. Export as PDF Print → upload to Etsy with 'undated' in the title so it sells year-round

**Launch price:** $4.99
**Etsy title:** Daily Productivity Planner Printable | Undated | Top 3 Priorities + Hourly Schedule | PDF
**Tags:** daily planner, productivity planner, printable planner, undated planner, daily schedule, planner printable, time management, to do list, daily organizer, schedule printable, planner pages, hourly planner, work planner

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_productivity_brief.html)

### 📚 Language Learning

**This week's product:** Japanese Hiragana Practice Workbook

**Store inspiration:** [Japanese Hiragana Practice Sheets — This product sells well due to its comprehensive and well-structured practice sheets, making it easy for customers to learn and practice Hiragana](https://www.etsy.com/listing/1094090884/japanese-hiragana-practice-sheets)

**What buyers love:**
- Printable
- Comprehensive
- Affordable

**Your edge — make it better:**
- Audio pronunciation guide
- Interactive exercises
- Progress tracking

**How to build it in Canva:**
1. Open Canva → search 'handwriting practice worksheet' → pick a clean grid-based template
2. Create 46 pages (one per hiragana character): large model character top-left with numbered stroke order, then 6 dotted-trace boxes, then 6 blank practice boxes
3. Add the romaji pronunciation and 2 example words using that character at the bottom of each page
4. Use Noto Sans JP font for the character — test it prints clearly at 72pt before building all 46 pages
5. Include a 2-page hiragana reference chart as a bonus: all 46 characters in a grid with romaji below each

**Launch price:** $3.99
**Etsy title:** Japanese Hiragana Practice Sheets | 46 Characters + Stroke Order | Printable PDF Worksheet
**Tags:** hiragana practice, japanese writing, hiragana worksheet, learn japanese, japanese printable, stroke order, hiragana chart, japanese alphabet, hiragana learning, japanese language, kana worksheet, jlpt study, japanese beginner

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_language_brief.html)

### 👶 Children's Activities

**This week's product:** Ocean Explorer Busy Book

**Store inspiration:** [Busy Books Best Seller — This product sells well due to its engaging and interactive activities, making it easy for customers to keep their children entertained and educated](https://www.etsy.com/market/busy_books_best_seller)

**What buyers love:**
- Colourful
- Interactive
- Educational

**Your edge — make it better:**
- Customizable
- Reusable
- Durable

**How to build it in Canva:**
1. Open Canva → search 'busy book pages' → pick a bright ocean-themed template
2. Create 10+ activity pages: matching, colouring, tracing, counting, puzzles — all ocean-themed
3. Use vibrant blues, teals, and corals — make every page visually exciting for toddlers
4. Add lamination instructions on the cover page (many parents laminate busy book pages)
5. Export as PDF Print → upload to Etsy with 'busy book' prominently in the title

**Launch price:** $4.99
**Etsy title:** Ocean Explorer Busy Book for Toddlers | 20+ Activity Pages | Printable PDF
**Tags:** busy book, toddler activities, ocean theme, printable busy book, preschool activity, no-prep activity, ocean worksheet, busy book pages, toddler busy book, quiet book pages, activity pack kids, screen free kids, ocean animals

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_brief.html)

---

## 🚀 SECTION 3 — SaaS: Bell Transcript

*YouTube & Podcast Summaries in Seconds*

**Phase:** Research · Week 2 of 8

**This week's task:** Define MVP features and build the core transcript extraction script (foundation from Week 4 project)


>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md
Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.
>>>END

---

## ⚡ SECTION 4 — Quick Wins This Week

**1. Improve Product Quality** — Add a preview image showing the product filled in with sample data to give customers an idea of what the product looks like and how it can be used. Use high-quality images and ensure that the sample data is relevant and realistic.

**2. Optimize Pricing** — Research your competitors and price your product competitively, taking into account the value that it provides to customers. Consider offering discounts for bulk purchases or loyalty rewards to incentivize repeat business.

**3. Get First Sales** — Reach out to friends and family to get feedback on your product and ask them to share it with their networks. Participate in online communities related to your product and offer exclusive discounts to members to generate buzz and drive sales.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*