# Lesson Quality Pipeline

## Objective
No lesson goes live on the-bell.onrender.com unless it is accurate, beginner friendly, and consistent across every place it appears: the lesson page, quiz, try-it box, live tool, copy-prompt, LinkedIn post and carousel. We publish lessons people learn from, so teaching something wrong is the worst failure.

## When to run
- After generating or editing any lesson (`content/syllabus_lessons/S-XX_*.md`)
- After editing a quiz, copy-prompt or project in `config/coding_syllabus.json`
- After editing a try-it box (`templates/syllabus_lesson.html`) or a tool (`templates/syllabus_tools/`) in the website repo
- Every Friday, for next Monday's lesson, before it goes live

## The two repos
| What | Where | Role |
|---|---|---|
| Source of truth | `Newsletter/content/syllabus_lessons/`, `Newsletter/config/coding_syllabus.json`, `Newsletter/content/syllabus_projects/` | Edit here |
| Website | `Week 1_Excel Formula Generator/` (github.com/nurnabilahazman/the-bell, Render auto-deploys on push) | Never edit lesson files here directly; sync them |

## Steps

### 1. Generate (new lessons only)
`python3 tools/syllabus_lesson_generator.py`
The generator now tells the AI the previous lesson, the next lesson, and everything already taught, so "What's next" points at the real next lesson. It runs the hard checks automatically after writing each lesson.

### 2. Hard checks (free, instant, deterministic)
`python3 tools/lesson_qa.py --topic S-XX` (or `--all`)

Per section:
- **Structure:** all 6 sections, in teaching order, none empty
- **Building it:** every code block runs; every variable it creates is used and explained; it only uses syntax already taught (e.g. no `def` before S-11)
- **What's next:** names the real next lesson, never one already taught
- **Why this matters:** any "next lesson" claim matches the real next lesson
- **Quiz:** questions make sense on their own; explanations say why; typed answers match what the code really produces
- **Readability:** no sentence over 30 words, average 20 or less, no dashes
- **Tool:** the live tool prints the same format the lesson teaches

### 3. AI review (costs Groq tokens)
`python3 tools/lesson_qa.py --topic S-XX --judge`

Two reviewers, both on `openai/gpt-oss-20b` (set by `QA_MODEL`):
- **Flow reviewer**, 11 checks: analogy before jargon, idea → project bridge, code really does the project, one new idea per step, line by line walkthrough, every new term defined, concrete "why", on-topic mistake, correct "what's next", overall flow.
- **Accuracy reviewer**, 6 checks: every claim true; code works as written, including setup steps; no unsafe habits; quiz correct; try-it box and tool agree with the lesson; copy-prompt matches.

Every FAIL must quote the exact words. A FAIL is only reported if a second, independent review agrees; a split verdict shows as SKIP ("check manually").

### 4. Verify anything the checker can't run
Not-runnable lessons (terminal, git, pip, HTML/CSS/JS: S-02, S-16 to S-22) must be verified by hand, the way a learner would do it:
- Terminal/git: run the exact commands in a scratch folder (`mktemp -d`)
- pip: fresh `python3 -m venv`, install exactly what the lesson says, run the code
- HTML/CSS/JS: open the exact code in a real browser with Playwright and check what renders

### 5. Sync to the website repo
`python3 tools/sync_lessons_to_site.py` (refuses to copy if hard checks fail; `--dry-run` to preview)

### 6. Test the website locally
In `Week 1_Excel Formula Generator/`:
```bash
PORT=5077 python3 combined_app.py &
python3 tools/audit_site.py --base-url http://localhost:5077     # every page loads, no JS errors, no broken links
python3 tools/smoke_test.py --base-url http://localhost:5077     # AI tools answer, try-its and tools behave
python3 tools/test_lesson_widgets.py --base-url http://localhost:5077  # every lesson's components (244 checks)
python3 tools/test_s10_interactions.py --base-url http://localhost:5077  # S-10 acceptance suite
```
Only push after these pass, in a separate command (never chained onto the tests).

### 7. Push
Commit and push the website repo. Render deploys in about 2 minutes. Then run both tests again against `https://the-bell.onrender.com`.

### 8. LinkedIn post and carousel
If the lesson's code or claims changed, update `content/linkedin_posts/S-XX_*.md` and `content/syllabus_lessons/S-XX_*_carousel.json`, then `python3 tools/syllabus_carousel_renderer.py` to re-render the PDFs. Posts are published by hand, so an already published post must be edited on LinkedIn by hand.

## Interactive components (step-throughs, calculators, previews)
Every lesson can teach with working interactions, not just text. The pieces:

| What | Where |
|---|---|
| Component library: CodeTrace, Substitution, Experiment, Prediction, MistakeLab, RangeExplorer, LivePreview, FileSim, IndexExplorer | site repo `templates/partials/lesson_components.html` |
| A lesson's own setup (which component goes where, with what values) | site repo `templates/lesson_widgets/<id>.html` |
| Recorded real Python runs: step-throughs, comparison outputs, terminal sessions | site repo `tools/build_traces.py` → `data/lesson_traces/<id>.json` |

To add one to a lesson:
1. In the lesson markdown, put `[[widget:some-name]]` where it belongs (inside the existing headings). Use ```` ```output ```` under code to show its exact output, `:::details Title` … `:::` for fold-outs, and ```` ```python expect-error=NameError ```` for code that is meant to fail.
2. If it shows code running or a comparison, add the code to `TRACES`, `RUNS` or `TERMINAL` in `tools/build_traces.py` and run `python3 tools/build_traces.py`. Never hand-type an output or error message: record it.
3. Mount it in `templates/lesson_widgets/<id>.html` (copy a neighbouring lesson's file).
4. Add behaviour checks to `tools/test_lesson_widgets.py`, comparing what the component shows with real Python.
5. Run the pipeline from step 2 above. The checker verifies every ```` ```output ```` block against real Python, character for character.

Rules learned the hard way:
- Never uppercase labels that can contain code or file names (`total_cost`, `expenses.txt`): Python is case-sensitive.
- Long values must wrap or scroll inside their box; the page must never scroll sideways at 390px.
- Anything modelled in JavaScript says so on screen. Use Python's semantics exactly (`len` counts emoji as 1; floats print as `400.0`; `strptime` uses Python's own patterns).
- Printing a set gives a different order on every run, so lesson code prints `sorted(...)` when the output is shown.

## Testing the checker itself
`python3 tools/test_lesson_qa.py` (hard checks) or `--judge` (plus AI review)
Plants 23 known defects into a clean lesson, one at a time, and confirms each is caught by the right check; also confirms the clean lesson passes. Run it after changing `lesson_qa.py`. When a real problem slips through, add it as a new planted defect first (red), then fix the checker (green).

## Groq limits (learned 2026-10-08)
- Free tier: **8,000 tokens per minute** (prompt + max_tokens per request) and **200,000 tokens per rolling 24 hours, per model**.
- `llama-3.3-70b-versatile` was retired; every tool broke at once. The model now lives in one place per repo: `tools/groq_client.py` (newsletter) and `groq_chat()` in `combined_app.py` (website).
- The site and newsletter use `openai/gpt-oss-120b`, falling back to `openai/gpt-oss-20b` when it is out of daily allowance.
- gpt-oss models are reasoning models: their thinking counts as output. Give each call ~1,500 extra `max_tokens` and `reasoning_effort="low"`, or the JSON gets cut off.
- `qwen/qwen3.8-27b` is not a usable fallback: it caps output at 1,000 tokens per minute.
- The lesson reviewer uses `gpt-oss-20b` so it never eats the site's allowance. A full `--all --judge` review is ~13,000 tokens per lesson (~325,000 for 25 lessons), which is more than one day's allowance: review in batches, today's live lesson and next week's first. When the daily allowance runs out the checker stops cleanly and says where to resume.
