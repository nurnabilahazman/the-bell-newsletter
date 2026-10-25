# The Bell — Week 6 · October 25, 2026

>>>TAGLINE
Build. Ship. Earn.
>>>END

## 🛠️ SECTION 1 — Project of the Week

**Week 6 of 12: Price Monitor + Alert**

*Web monitoring*

Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.

>>>PROMPT
You are helping me build a Python price monitor that tracks product prices and sends email alerts. Here is exactly what I need:

1. Read a list of products to track from a CSV (columns: product_name, url, target_price, css_selector_for_price)
2. Visit each URL, extract the current price using the CSS selector
3. Compare with target price — if current price is at or below target, send an email alert with product name, current price, target price, and the URL
4. Save all price checks to a log CSV (product_name, url, price_found, date_checked, alert_sent)
5. Use: requests, BeautifulSoup4, smtplib, pandas, python-dotenv
6. Rotate between 3 different User-Agent strings to avoid getting blocked

Please:
a) Write the complete script
b) Explain how to find the right CSS selector for a price on any website (with a real example from Amazon or Shopee)
c) Show me a sample tracking CSV with 3 products
d) Tell me how to schedule this to run every 6 hours on my Mac
e) What should I do if a site blocks my scraper?
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

**Store inspiration:** [Wilson’s “Budget Spreadsheet” — simple clean Google Sheet that auto‑calculates remaining cash and visualizes savings progress, driving repeat buys](https://www.businessinsider.com/how-to-make-passive-income-selling-on-etsy-creator-influencer-2022-3)

**What buyers love:**
- Auto‑update totals
- Color‑coded expense categories
- Easy copy‑paste for new months

**Your edge — make it better:**
- Add a built‑in debt‑snowball calculator
- Include a printable one‑page summary in gold/navy colors
- Provide a 12‑month “Goal Tracker” tab with conditional formatting for milestones

**How to build it in Canva:**
1. Open Canva → search 'goal setting workbook' → pick a premium, clean design with journaling space
2. Create a 30+ page quarterly workbook: vision statement, 3 big goals, monthly breakdown, weekly check-ins, and a quarterly review
3. Add a 'wheel of life' assessment page, a values clarification exercise, and an affirmations page
4. Use a premium color scheme (navy + gold or charcoal + blush) to position it as a high-value product
5. Export as PDF Print → price at $6.99–$7.99 (workbooks command higher prices than single trackers)

**Launch price:** $6.99
**Etsy title:** Goal Setting Workbook Printable | Quarterly Planner | Vision + Goals + Weekly Review | PDF
**Tags:** goal setting, quarterly planner, goal planner, vision board, self improvement, life goals, mindset journal, goals worksheet, year planner, new year goals, goal tracker, annual planner, bucket list

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_productivity_brief.html)

### 📚 Language Learning

**This week's product:** Beginner Japanese Kana Workbook – Hiragana & Katakana (Level 1)

**Store inspiration:** [“JapaneseStudySheets” — clean printable PDFs that combine stroke order charts with practice grids, selling because learners can print and reuse instantly](https://www.youtube.com/watch?v=jOxmBhokJ_k)

**What buyers love:**
- Large practice boxes
- Stroke‑order illustrations
- Printable on A4

**Your edge — make it better:**
- Include audio QR codes for each character
- Add a “Mini‑Quiz” review page after every 10 chars
- Use gold accents for correct‑answer highlights while keeping navy for headings

**How to build it in Canva:**
1. Open Canva → search 'booklet template' → pick a compact, travel-guide-style layout (A5 or half-letter size)
2. Create 5 sections (one per language): Greetings, Numbers, Directions, Restaurant/Food, Shopping, Emergency, Hotel — 10 phrases per topic per language
3. Add pronunciation in brackets after each phrase (IPA not needed — use approximate English sounds, e.g. 'SAY: bon-ZHOOR')
4. Design a 'Quick Reference Card' single page per language — top 20 most essential phrases only — that buyers can print, fold, and carry in a wallet
5. Export as PDF Print → also offer a compact 'wallet card' export at A6 size as a second file

**Launch price:** $6.99
**Etsy title:** Travel Phrasebook Printable | 5 Languages Spanish French Italian German Portuguese | Instant Download
**Tags:** travel phrasebook, language phrases, travel printable, phrasebook printable, travel essentials, language guide, europe travel, travel guide, vacation phrases, backpacker tips, tourist phrases, multilingual, phrase guide

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_language_brief.html)

### 👶 Children's Activities

**This week's product:** Editable Kids Reward Chart (5 Designs)

**Store inspiration:** [“KiddoRewards” — offers 5 pre‑made editable Canva reward charts that parents can instantly customize, selling because they’re printable, colorful, and reusable](https://www.youtube.com/watch?v=twbqCcCWRm8)

**What buyers love:**
- Bright color palettes
- Editable text boxes for chores
- Printable on 8.5×11 paper

**Your edge — make it better:**
- Add a gold “Star‑Earned” sticker layer that users can copy‑paste, provide a navy‑themed “Progress Tracker” page, include QR code linking to a free printable “Reward Coupon” template, offer 2 extra designs for weekend tasks

**How to build it in Canva:**
1. Open Canva → create 5 chart designs: stars, animals, space, rainbow, superhero themes
2. Make each chart editable — add text boxes for child's name and weekly goal
3. Include sticker dots or checkboxes for 30 days of tracking on each design
4. Add a matching 'Certificate of Achievement' for each of the 5 themes
5. Export as PDF Print → mention '5 designs included' in the Etsy listing title

**Launch price:** $4.99
**Etsy title:** Editable Kids Reward Chart | 5 Designs | Printable Behavior Chart | Stars Animals Space
**Tags:** reward chart, behavior chart, kids chore chart, printable chart, star chart, potty training, editable chart, chore chart kids, good behavior, kids sticker chart, parenting tool, daily routine chart, responsibility chart

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_brief.html)

---

## 🚀 SECTION 3 — SaaS: Bell Transcript

*YouTube & Podcast Summaries in Seconds*

**Phase:** Launch · Week 6 of 8

**This week's task:** Deploy to the internet using a free hosting service, get a domain name, write the landing page


>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md
Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.
>>>END

---

## ⚡ SECTION 4 — Quick Wins This Week

**1. Polish the Visuals** — Open each Canva design, replace placeholder images with crisp icons from free libraries, and apply the Bell navy/gold palette to all headings for a cohesive look.

**2. Price Tier Smartly** — List the 5‑design bundle at $12.99 and offer a single‑design add‑on for $3.49; include “Instant Download” and “Unlimited Edits” tags to attract buyers.

**3. Boost First Sales** — Post a carousel on Instagram showing a filled‑in chart for a real child, add a swipe‑up link to your Etsy listing, and use the hashtag #KidsRewardChart to capture organic traffic.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*