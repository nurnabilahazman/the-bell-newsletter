# Content Plan — All 5 Projects
## Carousel slides + LinkedIn posts + design instructions

**Brand:** Cream `#F5F0E8` · Navy `#1A1A2E` · Gold `#C9A84C`
**Style reference:** Matt Gray (specific numbers, clean numbered steps) + Ruben Hassid (golden artifact verbatim, honest limitations, whispered save CTA)

---

---

# WEEK 1 — Excel Formula Generator
**Tool URL:** http://localhost:5001 (share screenshot — deploy before posting)

---

## CAROUSEL — 5 Slides

### S1 — THE HOOK
**Headline (large, center):** I waited 20 minutes for IT to write me one Excel formula.

**Sub-copy (smaller, below):** So I built a tool that does it in 3 seconds. Free.

**Design:**
- Background: Navy `#1A1A2E`
- Headline: White, 36–44px, bold, centered
- Sub-copy: Gold `#C9A84C`, 16px, centered below
- Bottom right corner: small Bell logo / "The Bell" wordmark in cream
- NO photos. Pure type — this is a Matt Gray hook card.
- Optional: a subtle gold underline separator between headline and sub-copy

---

### S2 — THE PROBLEM
**Headline:** The formula bar is blank. IT says 3 days.

**Sub-copy:** You know what you need. You just don't know the syntax.

**Design:**
- Background: Cream `#F5F0E8`
- Simple two-column layout:
  - LEFT box (navy border): labelled "The old way" — bullet list in muted grey: "Google VLOOKUP → get wrong answer → email IT → wait 3 days → still wrong"
  - RIGHT box (gold border): labelled "What should exist" — stays BLANK intentionally (creates tension)
- This blank right box is the pattern interrupt — the reader fills it in mentally
- Headline above in navy, 28px

---

### S3 — THE BUILD
**Headline:** Plain English in. Excel formula out.

**Sub-copy:** Describe what you need. Get the formula, the explanation, and a fix if it errors.

**Design:**
- SCREENSHOT of the actual Week 1 app (localhost:5001)
- Take a real screenshot with a filled-in example: input "Give me a formula that sums column B only if column A says London"
- Add a gold circle annotation around the copy button
- Add "The Bell" watermark badge bottom right
- Slide has light cream background, screenshot floats in card with subtle shadow

---

### S4 — THE PROOF (Golden Artifact)
**Headline:** I typed: "sum column B only if column A says London"

**Sub-copy:** It returned =SUMIF(A:A,"London",B:B). With an explanation. In 4 seconds.

**Design:**
- Split card design:
  - TOP half: cream bg, INPUT label in gold uppercase, the typed sentence in navy italic
  - BOTTOM half: navy bg, OUTPUT label in gold uppercase, the formula in monospace white font (as if a code block)
- Below formula: a short grey explanation text "Sums values in B only where A matches 'London'"
- This is the most important slide — the formula verbatim IS the proof

---

### S5 — THE GIFT
**Headline:** Free. No login. Just describe your problem and copy the formula.

**Sub-copy:** (Save this the next time IT has a 3-day queue and you need one formula)

**Design:**
- Background: Navy `#1A1A2E`
- Headline: White, bold, centered
- Sub-copy: Muted cream/grey, italic, small — this is the "whisper" CTA
- A pill button in gold: "Try it at [URL]" — but make it look like a Canva shape, not a real button
- Bottom: "Week 1 of 5 · The Bell · Build in Public"

---

## LINKEDIN TEXT POST — Week 1

```
I waited 20 minutes for IT to write me one Excel formula.

So I built a tool that does it in 3 seconds.

Here's exactly how it works:

1. You describe your data problem in plain English
2. AI translates it into the exact Excel formula
3. It explains WHY the formula works
4. If it errors, paste the error — it fixes it

The prompt I used to build it in Claude Code:
"Build a Flask web app. User types what they want in Excel. Groq API translates it to a formula and explains it. Add a copy button. Bell brand colors: cream, navy, gold."

That was it. 2 hours start to finish.

3 things nobody tells you about building tools with AI:
→ The hardest part is the UI, not the logic
→ Your first test case is always wrong — build in error correction from the start
→ "Explain why" matters more than the output itself

This is Week 1 of 5. Each week I build something that solves a real work problem — and post the build.

Free to use. No login. Link in bio.

(Save this if you've ever spent 20 minutes on a formula that should take 20 seconds)
```

**Post design notes:**
- Post first, then pin carousel in comments
- First comment: screenshot of the formula output as social proof

---
---

# WEEK 2 — Job Calculator
**Tool URL:** http://localhost:5002

---

## CAROUSEL — 5 Slides

### S1 — THE HOOK
**Headline:** Stop asking "should I take this job?"

**Sub-copy:** I built a calculator that gives you a score, a verdict, and the one question you forgot to ask.

**Design:**
- Background: Navy `#1A1A2E`
- Headline: White, bold, 36px, centered
- Below headline: 4 verdict pills arranged horizontally — "Strong Yes" (green), "Lean Yes" (gold), "Lean No" (amber), "Strong No" (red) — like a screenshot teaser
- Sub-copy: cream, 15px, below pills
- Bell branding bottom right

---

### S2 — THE PROBLEM
**Headline:** The salary looks good. The gut feeling doesn't.

**Sub-copy:** Most people decide on the number. Then spend 6 months realizing they missed the real question.

**Design:**
- Cream background
- A simple diagram: "What people focus on" vs "What actually decides it"
  - LEFT (small, one item): Salary number
  - RIGHT (bigger, 4 items): Manager, growth path, learning curve, culture
- Show the imbalance visually — RIGHT side is larger/bolder
- Navy headings, gold accent on "What actually decides it"

---

### S3 — THE BUILD
**Headline:** Rate the offer. Rate the manager. Rate the reality.

**Sub-copy:** The tool weighs all 6 factors and tells you the real question — the one that should actually decide this.

**Design:**
- SCREENSHOT of the tool's form page (3 sections visible: The Offer, The Opportunity, The Reality)
- Light cream frame around screenshot
- Add a gold arrow annotation pointing to "The Reality" section — this is the section people skip
- Caption below screenshot: "The section most people skip is the one that matters most"

---

### S4 — THE PROOF
**Headline:** Score: 74. Verdict: Lean Yes.

**Sub-copy:** "The salary is fair. The real question: what does the 3-year growth path actually look like here?"

**Design:**
- SCREENSHOT of the results page showing:
  - Score circle (74, navy with gold border)
  - Verdict pill ("Lean Yes" in gold)
  - The "Real Question" card highlighted
- Keep the screenshot clean — this is real proof
- Gold annotation box around "The Real Question" section
- No additional graphic elements needed — the result speaks

---

### S5 — THE GIFT
**Headline:** Free. 2 minutes to fill in. One verdict.

**Sub-copy:** And 3 questions to ask the hiring manager before you sign. (Save this for when you get an offer and don't know what to do)

**Design:**
- Navy background
- The 4 verdict pills stacked or arranged neatly in center
- White text: "Week 2 of 5 · The Bell"
- Gold pill at bottom: "Free · No login"
- Same whispered italic sub-copy as Week 1

---

## LINKEDIN TEXT POST — Week 2

```
Most people decide on salary. Then spend 6 months regretting it.

I built a calculator that scores your job offer like a financial model.

Here's what it weighs:

1. The numbers (salary, commute cost, work style)
2. The opportunity (growth ceiling, learning curve)
3. The reality (manager, culture, red flags)

Then it gives you:
→ A score out of 100
→ A verdict: Strong Yes / Lean Yes / Lean No / Strong No
→ 3 questions to ask before you sign
→ The one question that should actually decide it

The golden artifact — the prompt that built the scoring logic:
"You are a career advisor. Score this job offer 0–100. Weigh: salary (30%), growth potential (25%), manager quality (25%), learning opportunities (20%). Return a verdict and THE single real question that should decide this. Be direct. No hedging."

That framing took 20 minutes to get right. The code took 90 minutes.

3 things the tool taught me about job offers:
→ People over-weight salary by about 40%
→ The manager question is the one everyone forgets
→ "Red flags noticed" is the field that changes the score the most

This is Week 2 of 5. Each week: one problem, one tool, full build posted.

Free. No login. Link in bio.

(Save this for when you get an offer and the gut feeling doesn't match the number)
```

---
---

# WEEK 3 — Weekly Work Summary Generator
**Tool URL:** http://localhost:5003

---

## CAROUSEL — 5 Slides

### S1 — THE HOOK
**Headline:** My manager update used to take 45 minutes. Now it's 45 seconds.

**Sub-copy:** Same notes. Three outputs. Manager email, LinkedIn post, CV bullet — all from Friday's rough notes.

**Design:**
- Navy background
- "45 min → 45 sec" in MASSIVE gold type (this is the hero element — make it 60–72px)
- Below: white sub-copy, 16px
- Bottom: Bell branding
- This is pure Matt Gray — one striking number, nothing else

---

### S2 — THE PROBLEM
**Headline:** You did good work. You can't explain it at 5pm on Friday.

**Sub-copy:** A week of real achievements, buried in rough notes. Manager wants bullet points in 10 minutes.

**Design:**
- Cream background
- "Your notes" card on LEFT: messy bullet fragments in grey italic ("- fixed tableau thingy", "- report to cfo done", "- found discrepancy 12k?")
- Arrow pointing right →
- RIGHT side: big question mark OR a blank "Manager Update" email template
- This visual shows the gap the tool closes

---

### S3 — THE BUILD
**Headline:** Paste your rough notes. Get 3 polished versions.

**Sub-copy:** The tool reads your week and writes it in three voices: professional, personal, archival.

**Design:**
- SCREENSHOT of the app showing the 3 tabs: Manager Update · LinkedIn Post · Portfolio Note
- Annotate with "same input" label at top (arrow pointing to notes textarea)
- Three arrows pointing to the 3 tabs
- Very visual — shows the one-to-many output concept
- Light cream frame around screenshot

---

### S4 — THE PROOF
**Headline:** Input: "- fixed the Tableau thing, found 12k AR discrepancy"

**Sub-copy:** Output: a 5-bullet email, a LinkedIn hook, and a STAR bullet ready for your CV.

**Design:**
- Three side-by-side output previews:
  - LEFT: Manager email (cream box) — "Subject: Weekly Update — Key Findings"
  - CENTRE: LinkedIn hook (navy box, white text) — the hook line only
  - RIGHT: Portfolio note (cream box with gold headline) — "Identified £12K accounts receivable discrepancy..."
- Show the same work, three registers — this IS the product demo

---

### S5 — THE GIFT
**Headline:** Free. Paste your rough notes Friday afternoon. Copy the polished version.

**Sub-copy:** (Save this for end of week when you need a manager update and have no idea where to start)

**Design:**
- Navy background
- The 3 output type names stacked: MANAGER UPDATE · LINKEDIN POST · PORTFOLIO NOTE — in white, with gold dots between them
- Bell branding bottom
- Whispered italic CTA in small cream text

---

## LINKEDIN TEXT POST — Week 3

```
On Friday afternoon, I write the worst emails.

So I stopped writing them manually.

This week I built a tool that takes my rough Friday notes and turns them into:

1. A polished manager update (subject line + bullet points, results-led)
2. A LinkedIn post (hook-first, ready to paste)
3. A CV portfolio bullet (STAR format, metric-led)

One input. Three outputs. 45 seconds.

The prompt that generates the manager email:
"You are a professional communications coach. Turn these rough notes into a 3–5 bullet manager update. Each bullet: what was done, result or status, what's next. Formal, concise. Use numbers where possible."

The same prompt gets a different persona for the LinkedIn version — hook-first, question at the end.
Same notes. Different voice. Different purpose.

3 things I learned building this:
→ The "manager voice" and "LinkedIn voice" are almost opposite registers
→ Giving the AI your role + industry makes the output 10× more specific
→ The portfolio STAR format is the format most people forget — but it's the one that builds your CV as you go

This is Week 3 of 5. Building one tool a week. Posting the build each time.

Free. No login. Paste your notes. Copy what you need.

(Save this for the next time you have a Friday afternoon manager update and zero energy to write it)
```

---
---

# WEEK 4 — CV Optimizer
**Tool URL:** http://localhost:5004

---

## CAROUSEL — 5 Slides

### S1 — THE HOOK
**Headline:** Your CV probably has 3 lines a recruiter would cut on sight.

**Sub-copy:** I built a tool that tells you exactly which ones — and rewrites them.

**Design:**
- Navy background
- "3 lines" in large gold type, then rest of headline in white
- Alternatively: show 3 red X marks over blurred text (representing the lines to cut)
- Sub-copy in cream, 16px below
- No photos — pure type impact

---

### S2 — THE PROBLEM
**Headline:** "Make it more results-focused" is not feedback.

**Sub-copy:** You need to know which line is weak, why it's weak, and what it should say instead.

**Design:**
- Cream background
- LEFT card: a sticky note with generic feedback — "Quantify your achievements" "Be more specific" "Add metrics" — these are useless
- Arrow pointing RIGHT →
- RIGHT card: a specific rewrite example with BEFORE (grey) / AFTER (navy bold) — no labels needed, the visual contrast tells the story
- Headline above in navy

---

### S3 — THE BUILD
**Headline:** Paste your CV. Paste the job description. Get a full audit.

**Sub-copy:** Match score. Missing keywords. Line-by-line rewrites. Lines to cut. One positioning statement to add at the top.

**Design:**
- SCREENSHOT of the two-column form (CV on left, JD on right)
- Annotate with labels: "Your CV" and "The JD" with gold arrows
- Below the screenshot: list the 5 outputs in gold pill badges
- This slide is a "feature tour" — show the inputs and hint at the outputs

---

### S4 — THE PROOF (Golden Artifact)
**Headline:** Before: "Managed monthly reports." After: "Delivered KPI reports across 17 countries achieving 99% accuracy."

**Sub-copy:** Same job. Same person. Different line. Different shortlist.

**Design:**
- Split card (most important slide):
  - TOP: Cream box, "BEFORE" in red uppercase, the original weak line in grey italic
  - BOTTOM: Navy box, "AFTER" in gold uppercase, the rewritten line in bold white
- Below the card: Match Score circle showing e.g. "60 → 82" before/after
- No clutter — just the before/after contrast

---

### S5 — THE GIFT
**Headline:** Free. No CV consultant. No generic feedback.

**Sub-copy:** Paste your CV and the job description. Get the exact line to add at the top, the 5 missing keywords, and the lines that are hurting you.

**Design:**
- Navy background
- Gold match score circle in center (showing a number like 78)
- Verdict pill below: "Good Match" in gold
- White sub-copy text below
- "Week 4 of 5 · The Bell" at bottom
- Bell branding

---

## LINKEDIN TEXT POST — Week 4

```
Recruiters spend 7 seconds on your CV.

Most generic feedback makes it worse, not better.

"Be more specific" is not feedback. This is feedback:

"Line 3: 'Managed monthly reports' — too vague, no metric, no scope. Rewrite: 'Delivered KPI reports across 17 countries achieving 99% accuracy, reducing reporting cycle by 2 days.'"

That's what I built this week: a CV optimizer that gives you that level of specificity.

Here's what it returns:
1. Match score vs the job description (0–100)
2. Exact keywords you're missing
3. Line-by-line rewrites — original, why it's weak, the better version
4. Lines to cut entirely
5. A positioning statement to add at the very top, written for the specific role

The golden artifact — the prompt behind the audit:
"You are a senior finance recruiter. Review this CV against this JD. Give me: the exact weak lines and why, the rewrite, the missing keywords, and the one-line summary to add at the top. Be specific. Not generic. Tell me which line, not which concept."

3 things the tool taught me:
→ Most CVs fail on the first bullet, not the last one
→ The positioning statement is the most underused CV section
→ The "lines to cut" list is always longer than people expect

This is Week 4 of 5.

Free. No login. Paste your CV and the JD.

(Save this for the next time you're applying and wondering why you're not getting interviews)
```

---
---

# WEEK 5 — The Bell Newsletter Build Diary
**This is the meta-project — how The Bell itself was built.**

---

## CAROUSEL — 5 Slides

### S1 — THE HOOK
**Headline:** I built a newsletter that runs itself. Here's what I used.

**Sub-copy:** Zero Substack. Zero Beehiiv. Just Python, GitHub, and 5 weeks of building in public.

**Design:**
- Navy background
- Headline in white, bold, 36px, centered
- Below: a very minimal horizontal "stack" diagram showing 3 boxes in gold outline: "Python script" → "GitHub Actions" → "Your inbox"
- Sub-copy in cream below
- This is the system teaser — the diagram doesn't need to be detailed, just show the architecture exists

---

### S2 — THE PROBLEM
**Headline:** Every newsletter tool owns your audience.

**Sub-copy:** Substack takes a cut. Beehiiv charges per subscriber. I wanted to own everything — the list, the code, the content.

**Design:**
- Cream background
- Simple comparison table (2 columns):
  - Column 1: "Platform tools" — bullet list: "You pay per subscriber / They own the deliverability / You lose data if you leave"
  - Column 2: "What I built" — bullet list: "Free to run / I own the code / Portable to any email provider"
- Column 2 has gold left border accent
- Headline in navy above the table

---

### S3 — THE BUILD
**Headline:** The stack: Python generates it. GitHub runs it. Mailchimp sends it.

**Sub-copy:** Four tools. No subscription cost. Full control.

**Design:**
- A horizontal pipeline diagram (hand-built in Canva):
  - Box 1: "Groq AI" (research brief generation) → gold arrow →
  - Box 2: "Python script" (HTML builder) → gold arrow →
  - Box 3: "GitHub Actions" (scheduler) → gold arrow →
  - Box 4: "Mailchimp API" (delivery) → gold arrow →
  - Box 5: "Subscribers" (inbox, represented by an envelope icon)
- Cream background, navy boxes, gold arrows
- This is the diagram slide — spend time making this clean in Canva

---

### S4 — THE PROOF
**Headline:** Week 2 is live. Every component built and pushed to Git.

**Sub-copy:** This carousel? Also automated. The research brief that informed it? Also automated.

**Design:**
- SCREENSHOT of one of these (choose the most visual):
  - Option A: The LinkedIn Research Brief HTML page open in browser (port 8083)
  - Option B: VS Code showing the `tools/` folder structure with all the scripts visible
  - Option C: A GitHub Actions run (green checkmark, run log visible)
- Add a gold annotation: "This runs automatically" with an arrow
- Light frame, Bell branding

---

### S5 — THE GIFT
**Headline:** The full build is documented. Free to follow.

**Sub-copy:** Each week I post one build. The code, the prompts, the mistakes — all of it. (Save this if you want to build something that runs itself)

**Design:**
- Navy background
- "The Bell" wordmark in gold, centered and large (make this the hero element of the whole series)
- Below: "Build in Public · 5 weeks · Finance + AI"
- White sub-copy whisper CTA in italic
- This is the brand close — the final slide is the identity card

---

## LINKEDIN TEXT POST — Week 5

```
I work full time. I post every week. I don't write on Sundays.

Here's the system:

A Python script scrapes Hacker News every Monday.
It finds the 5 most relevant stories in finance and AI.
It generates a research brief in my brand design.
I read it for 15 minutes. I write the post.

That's it. 15 minutes of original thought. Everything else runs itself.

The stack:
→ Groq API (llama-3.3-70b) — research + summarisation
→ Python (Flask + HTML generation) — builds the brief and tools
→ GitHub Actions — schedules the scripts
→ Mailchimp API — sends the newsletter

Total cost: £0/month. No subscription tools. I own everything.

The honest limitation:
The hardest part isn't the code — it's the consistency. The system runs itself. The thinking still has to come from you.

3 things I learned building this in public:
→ Building for yourself is faster than building for a client — you ship when it works, not when it's perfect
→ The tools you build become your portfolio. Every project this month is a real demo.
→ The line between "newsletter person" and "builder" is just 5 weekends

This is Week 5 of 5. The build is done.

The Bell launches properly next week.

(Save this if you want to build something that doesn't require you to show up every time it runs)
```

---

---

# POSTING SEQUENCE

Post 1 week apart. This is the order:

| Week | Post date | Carousel | Text post | Visual anchor |
|---|---|---|---|---|
| 1 | Week 1 Monday | Excel Formula carousel | Same day | App screenshot on S3/S4 |
| 2 | Week 2 Monday | Job Calculator carousel | Same day | Results screenshot on S4 |
| 3 | Week 3 Monday | Summary Generator carousel | Same day | 3-tab output on S4 |
| 4 | Week 4 Monday | CV Optimizer carousel | Same day | Before/after on S4 |
| 5 | Week 5 Monday | Bell Build Diary carousel | Same day | Tools folder screenshot on S4 |

**Before posting each one:** Deploy the tool to a public URL (Netlify, Railway, or Render) so the CTA works. Free tier is fine. This turns "free tool" from a claim into a reality.

---

# DESIGN CHECKLIST FOR CANVA

For every carousel:
- [ ] S1: Navy bg, white headline, gold accent — one number or claim only
- [ ] S2: Cream bg — the problem diagram or the "before" state
- [ ] S3: App screenshot, light cream frame, gold annotation on key feature
- [ ] S4: The proof — verbatim input → output, or before/after split
- [ ] S5: Navy bg, whispered italic CTA, Bell branding visible
- [ ] Every slide: Bell logo or "The Bell" text bottom right
- [ ] Every carousel: "Week X of 5" in bottom left (builds series identity)
- [ ] Font: Use a clean sans-serif (Inter, DM Sans, or Canva's default)
- [ ] No more than 2 font sizes per slide (headline + body)
- [ ] No stock photos — screenshots and diagrams only (Ruben Hassid rule)
