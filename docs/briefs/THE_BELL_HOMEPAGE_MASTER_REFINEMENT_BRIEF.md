# THE BELL — HOMEPAGE MASTER REFINEMENT BRIEF
## Claude implementation specification | Mobile-first visual polish, content, trust, and usability

> Saved from the founder's message of 2026-10-09. This is the source brief that
> `workflows/homepage_refinement_pipeline.md` implements. Summary of its binding rules
> is in that workflow; this copy keeps the full detail.

**Purpose:** Refine the EXISTING website, not redesign it. Use the repository as the source of truth. The supplied mobile screenshots show the current intended visual language and content, but cannot establish code architecture, backend behavior, data policies, or whether numeric claims are independently verified.

**Founder intention:** A beautiful, approachable, impressive first visit: clean and minimalist yet visually varied, thoughtfully designed, beginner-friendly, credible, personal, and practical. The founder has iterated on the site extensively. **Preserve its distinctive components.** Do not flatten it into a standard SaaS template. The founder is an accounting/ACCA professional learning and building with AI assistance after work; do not misrepresent them as a software engineering expert or as having hand-written all code.

**Website:** https://the-bell.onrender.com/ ; sample lesson: https://the-bell.onrender.com/syllabus/lesson/S-10/

## 0. Non-negotiable rules
1. Audit before changing. List exact files to edit.
2. Preserve: navy/cream/muted gold identity; the bell symbol; winding 25-node roadmap; four branching tracks; weekly lesson spotlight; project cards; real-world achievement panels; FAQ accordion; personal, slightly candid voice. No stock photos, gradient blobs, glassmorphism, excessive shadows, random icons, loud animations.
3. Don't invent: user counts, usage metrics, savings, retention practices, provider policies, security claims, tests performed, employer endorsement, project completion status, future release guarantees.
4. Verify every existing numeric claim with founder-provided evidence or mark as founder-reported and request confirmation. Do not silently delete or modify numbers.
5. Accessible: contrast, semantic headings, keyboard focus, tap targets, reduced motion, responsive layout, readable mobile type.
6. No destructive refactors: preserve URLs, live tools, lesson navigation, content, integrations. Commit before editing; test after.
7. Vary section compositions within a cohesive system. No one-size-fits-all card grid.
8. Do not publish wording that makes technical or legal promises before checking the code and third-party terms.

## 1. Current homepage (from founder screenshots): keep core architecture and order
Hero (bell, `THE BELL · ZERO TO EXPERT`, `Learn to code. One real lesson a week.`, founder story, stats 89 / 10 / 0); weekly spotlight (THIS WEEK, THE SPINE, Loops, Batch Invoice Number Generator, two CTAs, previous/next chronology); `The whole path` serpentine 25-step roadmap with four dotted branches and legend; four tracks A to D; dark evidence section `NOT THEORY. SHIPPED AT WORK` (Deloitte, Warner Music, Maybank); tools section `Every project, in one place.`; FAQ `Things you might be wondering` (privacy, AI accuracy, why not ChatGPT, AI-built code, founder story).

## 2. Creative direction
Editorial, structured, calm, warm, quietly ambitious, beginner-friendly, premium without looking expensive, human-built. Avoid corporate dashboard, crypto landing page, children's game, template SaaS, AI poster aesthetic. One bold idea per viewport.
Palette (preserve existing tokens; these are references): navy #1B1A31, ivory #F5F0E8, white, muted gold #C8A64A (eyebrows, current node; not body text; darken for contrast on light), beige #F0EAE1, charcoal #3F3E46, slate #77767C (only where contrast passes), Track A blue #4C7FDF, B violet #9565D6, C coral #E66F59, D teal #36B5AE.
Type: max two families; mobile body 16–18px, supporting >=15px, clamp() headings, line height 1.45–1.65, gutters 20–24px, no horizontal scroll; spacing scale 8/12/16/24/32/48/64/80.
Micro-interactions: subtle hover/press/focus; roadmap nodes expose title/date/status on focus/tap (not hover only); restrained accordions honoring reduced motion; future tracks distinguished by label + status text, not low opacity; no false "completed" state.

## 3. Hero
Keep the headline. Problems: long paragraphs compete with the headline on mobile; "ACCA alone wasn't going to be enough" can read as the credential being insufficient; stats/CTA push the first lesson down; "ZERO TO EXPERT" promises expertise (consider `LEARN · BUILD · SHARE`, `FROM FIRST LINE TO REAL PROJECTS` or `THE BELL · LEARN BY BUILDING`, founder approval only).
Preferred support copy (2 short paragraphs max): "I work in finance, not software engineering. I started learning to build with AI and code because I wanted to spend less time on repetitive work." / "Now I'm sharing the lessons and projects I'm learning from, one week at a time."
Alternative (founder choice, not both): "I studied accounting and started learning automation to make repetitive work easier. The Bell is where I share the coding lessons and AI-assisted projects I'm building after work."
Micro-proof: `Free beginner lessons · Real projects · 10 AI tools to explore` (count dynamic). Primary CTA `Start this week's lesson →`, secondary `Explore free tools →`. Stats 89/10/0 only if verified; compact 3-column row on mobile; clarify 89 mapped vs 25 core; never claim all 89 are live.
Mobile: centred bell + eyebrow; two-line headline, gold only on second thought; one concise support block; stacked CTAs, primary dominant; compact metrics; no unnecessary full-screen hero height.

## 4. This week
Keep featured white card + warm inset. Hierarchy: `THIS WEEK · THE SPINE` + accurate date; large title; plain-English one-liner (e.g. Loops: "Make Python repeat a task instead of doing it by hand."); inset `BUILD THIS` / project; primary `Read the lesson →`; secondary `Already know the basics? Try the generator →` (label honestly per what the link is). Timeline: keep vertical gold line; ~3 previous, ~3 upcoming; previous rows obviously clickable; `Coming [date]` only if firm, else `Planned`; optional `View full syllabus`.

## 5. Roadmap: preserve the signature serpentine 5x5 path and branches
Legend: consider `Current`, `Available`, `Planned`. Node numbers + accessible labels; >=44px tap areas; on tap/focus expose `Lesson 10 · Loops · Available`; crisp SVG, no clipping at 320px; preserve branching to A–D without collisions; condensed or accessible list alternative on very narrow screens; explain "25 foundational lessons, then four specialist tracks" above; clarify 89 includes future tracks if true; don't imply scheduled lessons are published.
Suggested text: "Start with 25 foundational lessons. Then choose a direction: build products, work with data and AI, explore systems and security, or understand computer science more deeply."

## 6. Track cards
Keep differentiated accents. Single column or swipe if 2x2 is cramped at 375px (test). A Web & Product (databases, auth, REST APIs, deployment; 10 tools live); B Data & AI (planned 2027); C Systems & Security (planned 2027–2028); D CS Theory (planned 2028). Thin accent line, small consistent icon container, short title, 1–2 line description, status pill. Future cards stay readable (quiet background + PLANNED pill), not faded. Links only to real destinations. Prefer consistent line icons over emoji-only. Reserve the four colours for tracks and their roadmap branches.

## 7. Evidence section
Keep dark navy and large gold outcomes. Card anatomy: verified outcome; one-line context; two-line summary; compact tags; optional `How it worked ↓` disclosure for detail. Claims needing founder verification + careful status wording:
- Deloitte: 42 hours → 2 minutes, 99%+ efficiency, 50+ scanned files, 3,000+ data points, 1,000+ test runs, under 3 months.
- Warner Music Tableau: 9 months → 1 week, 97%+ faster, 25 templates, 50+ testing rounds, 1–2 weeks → under 5 minutes; confirm deployed / tested / discontinued / superseded.
- Warner Music Apps Script: 48+ hours → 3 minutes, 99%+ on Tax KPI already live; other categories in progress; keep completed scope separate from projected savings.
- Maybank: 3 → 6 entities, 15 tables, 0 discrepancies; verify scope.
Check confidentiality / permission for employer names and internal systems; keep the independent / not-affiliated footer. Alternating panels or vertical proof timeline, not four identical walls of text; no fake charts.

## 8. Tools section
Heading option `Built to be used, not just read.` / `Try a free tool, then open its build guide to see how it works.` (or keep current). Each card: precise name, one concrete outcome (<=2 lines), `Open tool →`, `See how it was built →`, optional verified tags only. Honest states (no misleading "Live"). `+7 more` clearly clickable to the full directory. Check all ten tools and guides load.

## 9. FAQ
Keep title and candid tone; add at most 1–2 questions.
9.1 Privacy audit FIRST: storage, cookies, analytics, telemetry, request paths, logs, hosting logs, AI provider and its retention/training policy, third parties, personal data in scope, privacy policy existence. Never write "no logging", "never stored", "completely safe", "not used for training", "end-to-end encrypted" unless confirmed end to end. HTTPS protects transport only.
9.2 Proposed answers (confirm each fact): Q1 data safety (no account; some tools send input to an external AI provider; don't paste passwords, IDs, confidential work; remove identifying details; link privacy page or real contact). Q2 wrong output (starting point not final decision; check important details; report via LinkedIn without private info). Q3 why not ChatGPT (prompts + workflow for specific tasks; build guides show how; check guides actually expose prompts). Q4 AI-built code (used AI extensively; test and fix; not audited enterprise software; no formal-audit or "low risk" claims). Q5 who built this (accountant, own money on courses, after work, AI helped, still learning; optional pull quote "ACCA taught me accounting. It didn't teach me how to stop repeating the same task every week." founder approval). Optional Q6 do I need coding (no). Optional Q7 is it free (only if accurate; no indefinite promise).
9.3 Accordion: collapsed by default; clear chevron; `<button>` with `aria-expanded`/`aria-controls`; keyboard; visible focus; >=44px targets; short paragraphs.

## 10. Point-of-use privacy note
Beside CV, salary, meeting notes and other free-text AI inputs: "Before you paste: Remove confidential details, passwords, ID numbers, and private company information. This tool may send your input to an external AI provider to generate a response." Tool-specific; calm styling (not scary red); link privacy page if it exists; report-issue link that doesn't ask for the sensitive input. Optional Privacy & Data Handling page (plain English; per-tool providers; logging/retention by site, host, providers; analytics/cookies; what not to submit; contact; effective date; no unsupported compliance claims).

## 11. Navigation, footer, microcopy
Clear `Start learning` / `Explore tools` near top; logo links home; sticky quick-nav only if warranted. Footer: `Independent project · Built after work · AI-assisted · Not affiliated with employers mentioned` (accurate), links to Lessons, Tools, How it was built, Privacy, LinkedIn/contact where real. No "Unlock your potential" style phrases; keep plain specific labels.

## 12. Mobile checklist
Widths 320, 360, 375, 390, 414, 430, 768, 1024, 1440. Intentional headline wraps; eyebrow/gold contrast; first CTA visible quickly; stats aligned; spotlight spacing; previous/next obviously tappable; roadmap legible, interactive, not clipped; tracks not cramped (1 column below ~400px if needed); future tracks readable; metrics wrap elegantly with details collapsed; tool card link hierarchy; FAQ wraps, icon doesn't collide; long answers readable; safe-area insets; no layout shift; colour not the only cue; screen reader order, landmarks, headings, alt text, keyboard, focus.

## 13. Performance, search, analytics
Optimise images; defer non-critical JS; no layout shift; good title/meta/social preview; privacy-conscious analytics only if disclosed, never secretly added; analytics must not capture free-text inputs.

## 14. Content consistency audit
Verify 89 mapped (live vs planned); 25 foundational lessons and dates; 10 tools live, routes, uptime, free limits; S-10/S-11 dates; zero cost (no hidden fees/quotas/accounts); founder bio accuracy; professional metrics, rollout status, confidentiality; AI processing, logs, third-party retention, security posture; footer disclaimer and contact. Mark unverified items `NEEDS FOUNDER CONFIRMATION`.

## 15. Sequence
A Inspect & propose (Keep / Change / Verify / Optional, exact files, risks, flagged claims). B High-confidence changes (privacy statements, hero, FAQ accessibility, mobile legibility of tracks and evidence, roadmap labels and links). C Optional polish (rhythm, states, icons, density). D QA (tests, responsive screenshots, keyboard/screen reader, contrast, reduced motion, click every CTA, re-check privacy text, before/after, changelog).

## 16. Acceptance criteria
First-time visitor understands the offer and finds a lesson/tool quickly; still recognisably navy/cream/gold; roadmap and branching tracks preserved; mobile readable and interactive without clipping/overflow; every CTA real and correct; future content distinguished; achievements keep impact without walls of text or misleading status; privacy/AI claims grounded or transparently qualified; voice human and candid; lessons, tools, guides still work; report what changed, what was tested, what needs approval.

## Founder approval points
1. Hero copy (recommended vs personal alternative). 2. Replace `ZERO TO EXPERT`? 3. Privacy/retention/logging facts after audit. 4. Which professional figures and employer details may be published, and deployment status. 5. Optional FAQs 6–7 and a separate privacy page.

*Minimalist does not mean generic. Beginner-friendly does not mean childish. Credible does not mean corporate. Make every section intentional.*
