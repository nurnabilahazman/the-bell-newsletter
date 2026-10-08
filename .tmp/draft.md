# The Bell — Week 4 · October 08, 2026

>>>TAGLINE
Build. Ship. Earn.
>>>END

## 🛠️ SECTION 1 — Project of the Week

**Week 4 of 12: YouTube Transcript + Summary Tool**

*API integration*

Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.

>>>PROMPT
You are helping me build a Python tool that extracts transcripts from YouTube videos and generates structured summaries. This will eventually become my SaaS product. Here is exactly what I need:

1. Accept a YouTube URL as input
2. Extract the full transcript using the youtube-transcript-api library
3. Send the transcript to Groq API (model: llama-3.3-70b-versatile) with this prompt structure:
   - 3-sentence summary
   - 5 key takeaways (bullet points)
   - Action items mentioned
   - Timestamps for the most important moments
4. Save the output as both a .txt file and a .json file
5. Also generate a clean HTML page showing the summary nicely formatted
6. Use these libraries: youtube-transcript-api, groq, python-dotenv
7. API key comes from GROQ_API_KEY in .env

Please:
a) Write the complete Python script
b) List every pip install I need
c) Handle these edge cases: video has no transcript, transcript is in wrong language, video is private
d) Show me how to run it with a real YouTube URL
e) Tell me what I would need to add to turn this into a simple web app someone could use in their browser
>>>END

>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section1_projects_guide.md
How to work with Claude on projects, common errors, and the 12-week learning arc.
>>>END

---

## 📦 SECTION 2 — 3 Products to Build This Week

One product per theme. Research done. Prompt ready. Just paste and create.

### 🗂️ Productivity & Trackers

**This week's product:** 2025 Ultimate Budget & Goal Tracker Spreadsheet

**Store inspiration:** [Ultimate Annual Budget Spreadsheet — Offers a clean, pre‑formatted sheet with built‑in monthly, quarterly, and yearly views, making it instant‑ready for users;](https://www.etsy.com/market/best_selling_budget_template)

**What buyers love:**
- Instant usability
- Built‑in formulas
- Elegant navy & gold color theme

**Your edge — make it better:**
- Add a customizable “Cash Flow” dashboard
- Include a “Savings Goal Progress” gauge
- Embed a “Debt Snowball” calculator

**How to build it in Canva:**
1. Open Canva → search 'habit tracker template' → pick a design with a grid layout and room for habit names
2. Create a single-page monthly habit tracker: 10 habit rows × 31 day columns, plus a monthly reflection section
3. Make it undated — include a blank 'Month:' field so it works for any month of any year
4. Add a bonus page: 'How to Build a Habit in 30 Days' — one-page guide with the habit loop explained simply
5. Export as PDF Print → list as a 5-pack (5 copies of the tracker page) for perceived value

**Launch price:** $3.99
**Etsy title:** 30 Day Habit Tracker Printable | Monthly Habit Log | Undated | Instant Download PDF
**Tags:** habit tracker, 30 day habit, monthly tracker, habit log printable, goal tracker, self improvement, wellness tracker, daily habits, habit journal, routine tracker, morning routine, self care, habit challenge

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_productivity_brief.html)

### 📚 Language Learning

**This week's product:** Japanese Hiragana & Katakana Practice Workbook – Beginner Level

**Store inspiration:** [Hiragana Katakana Practice Sheets — Provides 104 character sheets, includes stroke order guidance and trace‑able grids;](https://www.etsy.com/market/japanese_hiragana_practice_goodnotes_worksheets)

**What buyers love:**
- Clear stroke order
- Printable PDF
- Beginner‑friendly layout

**Your edge — make it better:**
- Add a “Quiz” page with multiple choice stroke order questions
- Include a progress tracker for each character
- Provide a “Pronunciation Guide” audio link (optional)

**How to build it in Canva:**
1. Open Canva → search 'cheat sheet template' → pick a clean, information-dense single-page layout
2. Create 10 pages (one per grammar rule): present tense conjugation, gender + articles, adjective agreement, negation, question formation, past tense (passé composé), future tense, pronouns, prepositions, and common irregular verbs
3. Each page: rule headline → formula in a colored box → 5 example sentences in a table → 'common mistake to avoid' callout box
4. Use a clean academic color scheme: dark navy, white, gold accent — feels premium and study-worthy
5. Add a double-sided summary card (A5 size) as a bonus page — buyers can print it separately and keep it on their desk

**Launch price:** $5.99
**Etsy title:** French Grammar Cheat Sheets | 10 Essential Rules | Study Guide | Printable PDF Instant Download
**Tags:** french grammar, french cheat sheet, learn french, french study guide, french printable, grammar reference, french conjugation, french language, french learning, french teacher, french worksheet, learn francais, french beginner

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_language_brief.html)

### 👶 Children's Activities

**This week's product:** Number Tracing + Counting Workbook (1–20)

**Store inspiration:** [Busy Book Best Seller – Toddler Busy Book Printable – Offers 120 pages with animal illustrations, easy tracing, and interactive cutouts;](https://www.etsy.com/market/busy_book_best_seller)

**What buyers love:**
- Simple numbers
- Engaging illustrations
- Ready‑to‑print layout

**Your edge — make it better:**
- Dedicated counting activity with tally marks
- Include a “Progress Tracker” with stickers
- Provide a “Parent Guide” PDF for usage tips

**How to build it in Canva:**
1. Open Canva → search 'number tracing worksheet' → pick a clean, colourful template
2. Create 20+ pages: one per number with a large traceable digit + counting objects to circle
3. Add a 'count and circle' activity on each page to reinforce number recognition
4. Include bonus pages: number bonds, number ordering, and a certificate of completion
5. Export as PDF Print → upload to Etsy with age range (3–5) in title and all tags

**Launch price:** $4.99
**Etsy title:** Number Tracing Workbook 1-20 for Preschoolers | 30 Pages | Printable PDF
**Tags:** number tracing, counting worksheet, number recognition, preschool math, number workbook, kindergarten prep, math printable, counting printable, trace and count, preschool numbers, number learning, early math, number practice

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_brief.html)

---

## 🚀 SECTION 3 — SaaS: Bell Transcript

*YouTube & Podcast Summaries in Seconds*

**Phase:** Build · Week 4 of 8

**This week's task:** Add user accounts — sign up, log in, track how many transcripts each user has used


>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md
Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.
>>>END

---

## ⚡ SECTION 4 — Quick Wins This Week

**1. Show Sample Data** — Add a preview image of the workbook filled in with a sample number (e.g., number 5) to demonstrate tracing and counting layout.

**2. Highlight Price Value** — Include a sidebar in your listing that shows a 20% discount coupon code and mentions the $8 price, emphasizing “Only $8 for a complete 1–20 tracing set.”

**3. Leverage Parent Reviews** — Ask early buyers to leave a quick 5‑star review and share a photo of their child using the workbook in the description.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*