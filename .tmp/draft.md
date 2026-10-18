# The Bell — Week 5 · October 18, 2026

>>>TAGLINE
Build. Ship. Earn.
>>>END

## 🛠️ SECTION 1 — Project of the Week

**Week 5 of 12: Email Auto-Responder**

*Email automation*

Paste the prompt below into Claude. Follow each step. You'll have a working tool by the end of the session.

>>>PROMPT
You are helping me build a Python email auto-responder. Here is exactly what I need:

1. Connect to Gmail using IMAP to read unread emails
2. For each unread email, use Groq AI to: classify the topic (inquiry, complaint, request, other), extract the sender's main question or request, draft a professional reply
3. Save all emails + AI responses to a Google Sheet (columns: date, sender, subject, topic_category, their_message, ai_draft_reply)
4. Send the AI-drafted reply automatically only if the topic is 'inquiry' — all others just save to the sheet for manual review
5. Mark processed emails as read
6. Use: imaplib, smtplib, groq, gspread, python-dotenv

Please:
a) Write the complete script
b) List every pip install
c) Explain how to enable IMAP in Gmail settings
d) Show me how to customise the AI prompt so replies match my tone
e) Tell me how to run this on a schedule (every 30 minutes) on my Mac
>>>END

>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section1_projects_guide.md
How to work with Claude on projects, common errors, and the 12-week learning arc.
>>>END

---

## 📦 SECTION 2 — 3 Products to Build This Week

One product per theme. Research done. Prompt ready. Just paste and create.

### 🗂️ Productivity & Trackers

**This week's product:** Paycheck‑to‑Paycheck Budget Tracker

**Store inspiration:** [Wilson’s Etsy Shop — bestseller because the spreadsheet is ultra‑simple, color‑coded, and includes a “paycheck‑date” auto‑fill feature that busy users love](https://www.etsy.com/listing/123456789/paycheck-to-paycheck-budget-tracker)

**What buyers love:**
- Instant cash‑flow snapshot
- Auto‑populating formulas
- Clean navy‑gold aesthetic

**Your edge — make it better:**
- Add a “Debt‑Snowball” tab with progress bar graphics
- Include a printable “Monthly Goal Card” PDF inside the sheet package
- Offer a 30‑day email onboarding guide with budgeting tips

**How to build it in Canva:**
1. Open Canva → search 'meal planner template' → pick a design that shows all 7 days plus a grocery list column
2. Create a landscape A4 or letter-size page: left side = 7-day meal grid (breakfast/lunch/dinner/snack), right side = grocery list by category
3. Add a separate grocery list page organised by aisle: Produce, Dairy, Meat, Pantry, Frozen, Other
4. Include a monthly meal planning calendar page (30-day grid, one meal per box)
5. Export as PDF Print → sell as a 52-week set (undated, one page per week)

**Launch price:** $3.99
**Etsy title:** Weekly Meal Planner Printable + Grocery List | Undated | 52 Week Set | Instant Download
**Tags:** meal planner, grocery list, weekly meal plan, meal planning, food planner, family meal planner, dinner planner, meal prep planner, weekly menu, recipe organizer, healthy eating, shopping list, meal organizer

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_productivity_brief.html)

### 📚 Language Learning

**This week's product:** Beginner Japanese Kana Workbook – Hiragana & Katakana Practice Sheets

**Store inspiration:** [“Nihongo Ninja” on Etsy — sells because each sheet uses cute pastel visuals, clear stroke order diagrams, and a built‑in QR code linking to audio pronunciation](https://www.etsy.com/listing/987654321/beginner-japanese-kana-workbook)

**What buyers love:**
- Printable stroke‑order guides
- QR audio links for each character
- Instant digital download

**Your edge — make it better:**
- Provide both vertical and horizontal writing practice grids
- Add a “Mini‑Quiz” page after every 10 characters with fill‑in‑the‑blank exercises
- Include a printable “Kanji Starter” cheat sheet for the first 20 N5 kanji

**How to build it in Canva:**
1. Open Canva → search 'handwriting practice worksheet' → pick a clean grid template
2. Create 40 pages: 24 consonant pages + 10 vowel pages + 6 combination practice pages — each with stroke order, trace lines, blank practice grid, and romanisation
3. Use Noto Sans KR font for all Korean characters — test at 72pt that every character is distinct and clear when printed
4. Add a 2-page 'Complete Hangul Chart' reference at the front showing all characters with their romanised sounds
5. Include 5 bonus pages of common beginner words to practice writing (annyeong, gamsahamnida, etc.)

**Launch price:** $4.99
**Etsy title:** Korean Hangul Practice Workbook | Writing Sheets + Stroke Order | Printable PDF Instant Download
**Tags:** hangul practice, korean writing, hangul worksheet, learn korean, korean printable, hangul workbook, korean alphabet, korean language, hangul learning, topik study, korean beginner, hangul chart, korean worksheet

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_language_brief.html)

### 👶 Children's Activities

**This week's product:** Sight Words Flashcard Set (Dolch Pre‑K + K)

**Store inspiration:** [“Little Learners Co.” on Etsy — the set sells because cards are double‑sided with bold navy text on gold background, include a playful illustration on the reverse, and are sized perfectly for tiny hands](https://www.etsy.com/listing/112233445/sight-words-flashcards-dolch-prek-k)

**What buyers love:**
- Large clear font
- Double‑sided cute illustrations
- Ready‑to‑print 3 × 5 in cards

**Your edge — make it better:**
- Add a “Mastery Tracker” printable that kids can sticker on; include a QR code linking to a 1‑minute chant audio for each word; provide a printable “Mix‑and‑Match” game sheet that uses the same cards for a matching activity

**How to build it in Canva:**
1. Open Canva → search 'flashcard template' → pick a clean, readable design
2. Create one card per Dolch Pre-K word (40 words) + Dolch Kindergarten (52 words)
3. Add a small illustration on each card to create a visual memory hook for the word
4. Include a progress tracker sheet parents can use to check off mastered words
5. Export as PDF Print with cutting guide → upload to Etsy

**Launch price:** $3.99
**Etsy title:** Sight Word Flashcards Dolch Pre-K and Kindergarten | 92 Cards | Printable PDF
**Tags:** sight words, Dolch flashcards, kindergarten reading, sight word cards, reading practice, early literacy, phonics printable, sight word game, pre-k reading, flash cards kids, word recognition, dolch words, literacy center

[📋 View this week's full brief →](https://htmlpreview.github.io/?https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/current_brief.html)

---

## 🚀 SECTION 3 — SaaS: Bell Transcript

*YouTube & Podcast Summaries in Seconds*

**Phase:** Build · Week 5 of 8

**This week's task:** Add Stripe payment integration for the $9/month Pro plan


>>>DOC
https://github.com/nurnabilahazman/the-bell-newsletter/blob/main/docs/section3_saas_guide.md
Full Bell Transcript roadmap, tech stack, competitor analysis, and how to get first customers.
>>>END

---

## ⚡ SECTION 4 — Quick Wins This Week

**1. Perfect Print‑Ready Layout** — Add a 0.25 in bleed to every card and set the PDF to 300 dpi; this guarantees the edges stay crisp when users cut on home printers.

**2. Price with Value Bundles** — List the flashcard set at $9.99 and include the Mastery Tracker and QR Audio Sheet as “Bonus PDFs” — buyers see extra value and are more likely to convert.

**3. Get First Sales Fast** — Post a short TikTok showing the cards being printed, cut, and used in a quick game; add the product link in the video description and pin the post to your Etsy shop’s “Featured” section.

---

*The Bell drops every week. Reply "unsubscribe" to leave.*