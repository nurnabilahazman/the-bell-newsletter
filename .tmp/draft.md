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

**This week's product:** Paycheck-to-Paycheck Budget Tracker

**Store inspiration:** [Budget Planner Google Sheet – Monthly Budget Spreadsheet by EtsyHunt — Simple, drag‑and‑drop layout with pre‑filled categories that auto‑calculate net worth and savings goals.](https://ehunt.ai/etsy-competitor-research/best-etsy-budget-planner)

**What buyers love:**
- Easy monthly overview
- Automatic savings tracker
- Clear debt payoff timeline

**Your edge — make it better:**
- Add a “Year‑in‑Review” dashboard with charts
- Include a “Flexible Paycheck Split” sheet that auto‑splits income between fixed and variable expenses
- Offer a printable “Expense Snapshot” for quick review

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

**This week's product:** Mandarin Beginner Vocabulary & Grammar Workbook – 1–3 Months

**Store inspiration:** [Mandarin Learning Pack by LanguageCraft — Concise, topic‑based lessons with practice sheets that mix vocabulary flashcards, fill‑in‑the‑blank grammar, and a spaced‑repetition review.](https://www.languagecraft.com/mandarin-beginner-workbook)

**What buyers love:**
- Clear layout
- Built‑in practice
- Instant feedback

**Your edge — make it better:**
- Add a “Listening Cue” audio link per page
- Provide a QR code linking to a pronunciation guide
- Include a “Progress Tracker” page that auto‑marks completed sections

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

**Store inspiration:** [Counting Fun – Kids Workbook by Little Learners — Bright, age‑appropriate layouts with large number shapes, bold numbers, and simple counting exercises. Price: $5.99.](https://www.littlelearners.com/number-tracing-counting-workbook)

**What buyers love:**
- Clear numbering
- Engaging activities
- Easy printing

**Your edge — make it better:**
- Add a “Progress Sticker” slot on each page
- Provide a “Parent Guide” sheet with suggested playtime
- Include a “Color‑by‑Number” bonus page

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

**1. Show a Sample Page** — Upload a high‑resolution preview image of a completed number‑tracing page so buyers see the exact layout and font before buying.

**2. Set a Clear Price Point** — Price the workbook at $5.99 and include a “Bundle Deal” that adds the sticker sheet for $0.99 to encourage upselling.

**3. Use Social Proof** — Add a customer testimonial with a photo of a child using the workbook in your Etsy listing; this boosts trust and drives first sales.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*