# Homepage & Site Refinement Pipeline

## Objective
Refine the-bell.onrender.com (homepage first, then any shared page) without losing what makes it distinctive, without publishing a claim that isn't true, and without breaking lessons, tools or build guides. Full design brief: `docs/briefs/THE_BELL_HOMEPAGE_MASTER_REFINEMENT_BRIEF.md`.

## When to run
Any request to change the homepage, site design, copy, FAQ, privacy wording, track cards, roadmap, evidence section, tools section, navigation or footer. (Lesson content has its own pipeline: `workflows/lesson_quality_pipeline.md`.)

## Where things are (website repo: `../Week 1_Excel Formula Generator/`)
| Part | File |
|---|---|
| Homepage (all sections, styles, scripts) | `templates/home.html` |
| Homepage route and the data it gets (spotlight, stats, tools list `BELL_TOOLS`) | `combined_app.py` (`@app.route("/")`, `get_syllabus_spotlight()`) |
| Winding 25-node roadmap SVG | `roadmap_svg.py` |
| "This week" date logic | each lesson's `scheduled_date` in `data/coding_syllabus.json` vs today |
| AI tools and their pages | `templates/week1/` … `templates/week10/`, calls in `combined_app.py` (`groq_chat`) |
| Page-load / link / JS-error audit | `tools/audit_site.py` |
| Click-through + 10 AI tools | `tools/smoke_test.py` |
| Homepage checks (CTAs, overflow at all widths, accordion, contrast, roadmap) | `tools/test_homepage.py` |

## Rules (non-negotiable)
1. **Preserve the signature pieces:** navy/cream/gold identity, the bell, the winding 25-node roadmap with four branches, the four track cards with their colours, the weekly spotlight with its inset and timeline, the dark evidence section, the tool cards, the FAQ accordion, the candid personal voice. Vary layouts; never flatten into a generic SaaS grid. No stock photos, blobs, glassmorphism, loud animation.
2. **Never invent or change a fact.** Numbers (89 / 10 / 0, every career metric), employer details, privacy behaviour, AI provider policies, testing claims and release dates are verified against the code, the data, or the founder. Anything unverified is listed as `NEEDS FOUNDER CONFIRMATION` and left as it is, or qualified, never silently edited.
3. **Privacy wording must match the code and the provider's published policy.** Never write "no logging", "never stored", "completely safe", "not used for training" or "end-to-end encrypted" unless confirmed end to end. HTTPS protects data in transit only.
4. **Founder approval** is required for: hero copy, replacing "ZERO TO EXPERT", career metrics and employer names, privacy facts, new FAQ questions, a privacy page. Ask once, in one batch, with options and a recommendation.
5. **Accessibility is part of done:** WCAG AA contrast (4.5:1 body, 3:1 large text), semantic headings, visible keyboard focus, >=44px tap targets, `aria-expanded` on accordions, reduced motion respected, colour never the only signal.
6. **Mobile first:** test 320, 360, 375, 390, 414, 430, 768, 1024, 1440px. No sideways scrolling at any width.
7. **No destructive refactors:** keep every URL, tool, lesson link and integration. Commit before editing.

## Steps

### Phase A: inspect and propose (no edits)
1. Read the brief and `templates/home.html` end to end; list each section with its file and line range.
2. Screenshot the live homepage at 390px and 1440px (before images).
3. Run the privacy audit: what each AI tool sends, to whom (`groq_chat` → Groq), what the site stores (cookies, localStorage, database, files, logs), what gunicorn/Render log, the AI provider's current data policy (search their official docs), whether a privacy page exists.
4. Verify every number and claim on the page against the code/data; list what only the founder can confirm.
5. Write the audit: Keep / Change / Verify / Optional, with file locations and risks.

### Phase B: high-confidence changes
Make the changes that need no founder facts: honest privacy wording (qualified, matching the audit), point-of-use privacy notes on AI tools that take free text, FAQ accordion semantics, CTAs that lead somewhere real, readable future tracks, scannable evidence cards (same numbers, details on demand), roadmap labels and tap targets, mobile type and spacing. Ask the founder the approval questions in one batch, then apply the answers.

### Phase C: optional polish
Rhythm, states, focus/hover details, icon consistency. Only after Phase B screenshots look right.

### Phase D: QA (all must pass before push; push in a separate step)
```bash
cd "../Week 1_Excel Formula Generator"
PORT=5077 python3 combined_app.py &
python3 tools/test_homepage.py --base-url http://localhost:5077   # CTAs, widths, accordion, contrast, roadmap
python3 tools/audit_site.py --base-url http://localhost:5077      # every page, links, JS errors
python3 tools/smoke_test.py --base-url http://localhost:5077 --skip-ai
python3 tools/test_lesson_widgets.py --base-url http://localhost:5077   # lessons unaffected
```
Then before/after screenshots at 390px and 1440px, push, wait for Render, re-run the same tests against `https://the-bell.onrender.com`. Report: files changed, tests run with results, what still needs founder confirmation.

## Learned so far
- The homepage's "this week" lesson comes only from `scheduled_date` in `data/coding_syllabus.json`; Google Sheets and the newsletter pipeline don't affect it.
- Keep the Mac display awake for the whole time you work (`caffeinate -dimsu`).
- The local server (`python3 combined_app.py`, debug off) caches templates and Python modules: **restart it after every edit** before testing or screenshotting, or you test the old page. Check port 5077 isn't held by an old server (`lsof -i :5077`).
- Local Python is 3.9: no `str | None` annotations, no backslashes inside f-string expressions.
- Founder decisions (2026-10-09): eyebrow "THE BELL · LEARN BY BUILDING"; hero copy from the brief; keep employer names (Deloitte, Warner Music, Maybank) and every figure exactly; Tableau card carries "Now evolving onto a new platform to get past Tableau's limits." `tools/test_homepage.py` fails if any of these facts change.
- Text colours that pass AA: gold text on cream/white uses `--gold-text: #7d6219` (5.1:1 on cream; `#8a6d1f` was 4.32, a fail). Muted text `#5f5e66`. Bright gold `#C9A84C` only on navy or as a fill.
- Roadmap tap targets: transparent `r=41` hit circles plus tighter phone padding keep every node >= 44px down to 320px wide. Don't raise r above 41 (rows are 82 apart; circles would overlap).
- Same-colour sections next to each other double their padding; trim one side (FAQ top padding is 8px because the tools section above already gives 80px).
