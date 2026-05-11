# The Bell — Week 3 · May 11, 2026

>>>TAGLINE
Build. Ship. Earn.
>>>END

## 🛠️ SECTION 1 — Project of the Week

**Week 3 of 12: PDF Invoice Generator**

*Document automation*

Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.

>>>PROMPT
You are helping me build a Python script that automatically generates professional PDF invoices. Here is exactly what I need:

1. Read invoice data from a CSV file (columns: client_name, client_email, service_description, quantity, unit_price, invoice_date, due_date, invoice_number)
2. Generate one PDF per row with a professional layout including: my logo (logo.svg), invoice number, dates, itemised table, subtotal, tax (8%), total, payment instructions
3. Save each PDF as invoice_[invoice_number].pdf in an /output folder
4. Also send the PDF via email to the client_email automatically
5. Use these libraries: reportlab (for PDF), smtplib (for email), pandas (for CSV), python-dotenv
6. Email credentials come from .env file (GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

Please:
a) Write the complete Python script
b) List every pip install command I need
c) Show me a sample CSV with 3 rows I can use to test it
d) Walk me through running it step by step
e) Tell me how I can customise the colours and fonts to match my brand
>>>END

>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section1_projects_guide.md
How to work with Claude on projects, common errors, and the 12-week learning arc.
>>>END

---

## 📦 SECTION 2 — 3 Products to Build This Week

One product per theme. Research done. Prompt ready. Just paste and create.

### 🗂️ Productivity & Trackers

**This week's product:** Monthly Budget Tracker

**Store inspiration:** [Best Selling Budget — The most popular budget trackers on Etsy are those that offer a simple, easy-to-use format with clear headings and sections for income, expenses, and savings](https://www.etsy.com/market/best_selling_budget)

**What buyers love:**
- Easy to use
- Customizable
- Affordable

**Your edge — make it better:**
- Automated expense categorization
- Budgeting tips and resources
- Space for notes and goals

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

**This week's product:** Japanese Hiragana Workbook

**Store inspiration:** [Japanese Hiragana Practice — The most popular Japanese Hiragana practice workbooks on Etsy are those that offer a comprehensive and structured approach to learning the Hiragana alphabet, with plenty of practice exercises and quizzes](https://www.etsy.com/market/japanese_hiragana_practice)

**What buyers love:**
- Comprehensive lessons
- Practice exercises
- Quizzes and tests

**Your edge — make it better:**
- Audio recordings of native speakers
- Interactive flashcards
- Progress tracking and feedback

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

**Store inspiration:** [Busy Book Best Seller — The most popular busy books on Etsy are those that offer a fun and interactive way for children to learn and explore, with a variety of activities and games](https://www.etsy.com/market/busy_book_best_seller)

**What buyers love:**
- Interactive activities
- Colourful illustrations
- Durable construction

**Your edge — make it better:**
- Customizable name and picture page
- Reusable stickers and stencils
- Additional activity pages for older children

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

**Phase:** Build · Week 3 of 8

**This week's task:** Build a simple web interface using Flask so users can paste a YouTube URL and get a summary in the browser


>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md
Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.
>>>END

---

## ⚡ SECTION 4 — Quick Wins This Week

**1. Enhance Product Quality** — To enhance the quality of your digital products, make sure to include clear instructions and examples, and use high-quality images and graphics. For example, if you're creating a budget tracker, include a sample budget with realistic numbers to help users understand how to use the template.

**2. Optimize Your Listings** — To optimize your listings for better sales, make sure to include relevant keywords in your title and description, and use high-quality images that showcase your product. For example, if you're selling a Japanese Hiragana workbook, include keywords like "Japanese language learning" and "Hiragana practice" in your title and description.

**3. Get Your First Sales** — To get your first sales, make sure to promote your products on social media and other online platforms, and offer discounts or promotions to attract new customers. For example, you could offer a 10% discount on your Ocean Explorer Busy Book for the first 10 customers, or share a free sample page on your social media channels to generate interest.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*