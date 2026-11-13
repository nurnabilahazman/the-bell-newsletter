# The Bell: Master Guide for Weekly Lessons and LinkedIn Carousels

**Purpose:** This is the durable working brief for The Bell. Read it at the start of every new lesson, including in a new ChatGPT conversation or Work task. Last updated: 13 November 2026.

## 1. Project purpose and audience
The Bell teaches practical programming to complete beginners, including people without a computer science background. Explain each new concept with everyday situations, then show real, executable code. The learner should be able to understand the lesson without asking what technical jargon means.

- Language: natural, short, clear English. Punchy headings and simple examples. No inflated marketing copy or vague AI-sounding sentences.
- Give the learner the whole core concept in the carousel. The website extends learning with actual interaction.
- All lessons and their real exercises are free; say **FREE PYTHON LESSON** on the opening slide.
- Correctness beats visuals and speed. Never present invented code, output, errors, or fake interactive screenshots as real.

## 2. Existing source of truth and safe editing
Root directory: `/Users/nabilahazman/Documents/coding money project/Section 1_Project of the Week/Newsletter`.

Read `CLAUDE.md` and `workflows/lesson_quality_pipeline.md` before editing a lesson.

- Authoritative lesson content: `content/syllabus_lessons/S-NN_*.md`.
- Official lesson order, quizzes and AI copy-prompts: `config/coding_syllabus.json`.
- Specific interactive components: adjacent website repo `../Week 1_Excel Formula Generator/templates/lesson_widgets/S-NN.html`.
- Shared interactive components: `../Week 1_Excel Formula Generator/templates/partials/lesson_components.html`.
- Lesson-level NOW TRY IT: `../Week 1_Excel Formula Generator/templates/syllabus_lesson.html`.
- Actual deployed website: `https://the-bell.onrender.com`.
- Sync only using `tools/sync_lessons_to_site.py` after local QA, following the site workflow.
- Never change unrelated lessons, site templates or standardized feature names because an S-NN lesson needs better wording. Make an original-file backup before edits. Preserve any pre-existing unrelated git changes.
- Do not publish or say the site is updated until tests and a live check confirm it.
- Do not expose credentials, local private files or real employer data in teaching examples.

## 3. Standard lesson experience (preserve all four)
Each lesson has the same educational sections and their actual functionality:
1. **PREDICT FIRST**: The learner chooses or writes a prediction before seeing the answer. Real outputs, meaningful feedback.
2. **TRY IT YOURSELF**: The learner changes inputs or settings, clicks Run, and sees the actual comparison. Keep the simulator's state and Reset behaviour correct. Label JS demonstrations clearly.
3. **NOW TRY IT**: A second hands-on exercise that makes the learner debug, compare or transfer a concept. Its interactive behaviour must match actual Python.
4. **CHECK YOURSELF**: The real three-question understanding quiz with correct answers, explanations and appropriate feedback.

Also preserve the lesson's existing **Open tool**, **Copy prompt**, and **Preview first** functionality where available.

A lesson may additionally have **WATCH IT RUN** (line-by-line execution viewer). If it exists, show what it actually does and which buttons the reader can press.

These sections are NOT generic labels to display and remove. Keep their identities, interactive functionality, placement in the lesson, and site-wide styling. Improve specific content without forcing changes to other lessons.

## 4. Technical review before content design
- Inspect the actual source file, code, site widgets and answer data.
- Run every Python code example in a clean temporary directory, then again with relevant previous state if the topic uses files.
- Check exact outputs, errors, and choice answers against real behaviour. Never guess.
- Separate a Python limitation from a chosen teaching simplification. State example assumptions.
- Verify that JS simulated interactions accurately explain Python's behaviour.
- If something is wrong, fix the smallest relevant code/content surface first. Keep proven code when it is already correct.
- Run the repository's deterministic QA and site regression tests. Add a focused test for corrected interactive behaviour.

## 5. Carousel design standard (established and approved)
Format: **11 SEPARATE 1080 × 1350 px portrait PNG images**, not one collage and not plain slides assembled into a PDF.

Use the user's earlier The Bell editorial carousel references as the benchmark:
- Warm ivory/cream background with subtle paper warmth, not synthetic plastic gradients.
- Striking black high-contrast editorial serif headline; supporting sans-serif body; monospace for code.
- Neon-yellow accents applied deliberately to a small number of key words, labels, and outcomes.
- Thin curved lines and small dots in the corners; understated outline illustrations and elegant arrows.
- Highly legible code window, realistic and logically explained.
- Tight but balanced content placement; no oversized empty decorative boxes or cartoon-heavy illustrations.
- Footer: bell mark, **THE BELL : NABILAH AZMAN** and **the-bell.onrender.com** (or approved current brand treatment).
- One clear teaching point per slide, with concrete worked examples when needed.
- Consistent visual hierarchy, spelling, typography, code colours and margins across all slides.
- Keep **WATCH IT RUN**, **TRY IT YOURSELF**, **NOW TRY IT**, **CHECK YOURSELF** labels each in one consistent neon-yellow treatment; do not make every letter a different colour.
- Do not invent websites, screenshots or fake interactive controls. Show faithful screenshots/reconstructions from the actual site's features with arrows and short instructions.

## 6. Storyboard process for every lesson
**First read and understand the whole lesson.** Identify the 1-3 pivotal concepts that beginners must actually understand. Decide the visuals around those concepts; don't choose a slide layout first and then squeeze the lesson into it.

Create and verify a complete 11-slide storyboard before generating:
- Slide 1: a genuinely curiosity-creating real-life hook, plus prominent **FREE PYTHON LESSON**.
- Slides 2 onward: real-life example → meaning of concept → actual project → source code and workings → comparisons, common mistakes, work relevance as appropriate.
- Give the central concepts enough separate slides; do not spend all 11 on repeating the same point.
- Near the end, show the ACTUAL applicable website interactive activities with meaningful UI and instructions. Avoid cramming the activities into a generic list.
- Slide 11: an ending summary of THIS lesson and what Slides 1-10 actually taught, using the previously approved reference's recap format. Mention only the correct next lesson title from the official syllabus. Do not start teaching the next lesson in this slide.

This is a teaching framework, not a license to alter an approved slide-by-slide storyboard mid-production. Keep the approved sequence unless the user changes it.

## 7. Production, reviews, and publication
- After storyboard approval, generate full-size images ONE BY ONE if requested, with real editable/verified code text and no clipping.
- Confirm code snippets are exact and explanations match the illustrated outcome.
- Inspect the rendered image for spelling, alignment, overlapping text, tiny code, and visual inconsistencies.
- If the first slide looks generic or “AI-generated,” fix it before producing ten more.
- Keep approved slides untouched when revising another slide.
- The LinkedIn caption should be a natural storytelling post, not a repeat of the carousel. Include the correct deep link to the FREE lesson. Avoid em dashes (use periods, commas, or colons instead).
- Do not post or deploy without the user's instruction and the repository's existing checks. Report exactly what was edited, tested, saved locally, and actually published.

## 8. Current lesson context, as of 13 November 2026
- **S-14**: Handling errors (`try/except`). Project: Cost per Unit Calculator. Prior 11-slide carousel taught declined-card example, error paths and interactions.
- **S-15**: Reading and writing files. Project: Expense Log. Core concepts: `"a"` adds, `"w"` clears/replaces, `"r"` reads; `with open()` closes automatically. Must explain the initial-empty-file assumption and accurate buffered-write semantics. Keep existing Python project code and all standardized interactive features.
- **S-16**: Installing packages and virtual environments. This is the next topic after S-15.

## 9. How to restart from a new chat or Work session
Tell the assistant:
“Use Remote Desktop Commander to open the Newsletter project folder and read docs/THE_BELL_MASTER_GUIDE.md, CLAUDE.md, and workflows/lesson_quality_pipeline.md. Continue the next weekly lesson without changing the approved syllabus, visuals or interactive features. Inspect the real source, test before editing or deploying, and record the final deliverables in the project folder.”

The guide is the durable contract; previous chat context is supplementary, not the only place where decisions live.
