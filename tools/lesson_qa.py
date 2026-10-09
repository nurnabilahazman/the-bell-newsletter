#!/usr/bin/env python3
"""
Quality check for syllabus lessons, section by section.

Built to be used red/green: run it on a lesson BEFORE fixing (it should fail
and say exactly why), fix the lesson, run it again until every check passes.

Two layers:

1. Hard checks (free, deterministic, same answer every run)
   - every section exists, in the right order
   - every Python block in "Building it" actually runs
   - "What's next" names the REAL next topic, not a previous one
   - "Why this matters" doesn't promise something the next lesson won't do
   - quiz questions are answerable on their own and explanations teach something
   - typed quiz answers match what the lesson's own code really prints/returns
   - sentences stay short enough for a total beginner
   - the live tool prints the same format the lesson teaches

2. Reviewer checks (--judge, one Groq call per lesson, free tier)
   An AI reviewer reads the lesson as a total beginner and grades each
   section against a fixed rubric (analogy before jargon, smooth hand-off
   from idea to project to code, every term defined, etc). It must quote the
   exact words behind every FAIL, so a fail is always checkable by a human.

Usage:
    python3 tools/lesson_qa.py --topic S-10            # hard checks only
    python3 tools/lesson_qa.py --topic S-10 --judge    # plus reviewer
    python3 tools/lesson_qa.py --all                   # every lesson, hard checks

Exit code 0 = everything passed, 1 = at least one FAIL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYLLABUS_PATH = ROOT / "config/coding_syllabus.json"
LESSONS_DIR = ROOT / "content/syllabus_lessons"
SITE_DIR = ROOT.parent / "Week 1_Excel Formula Generator"

SECTIONS = ["The idea", "The project", "Building it", "Why this matters",
            "The mistake beginners make here", "What's next"]

# Lessons whose code can't run on its own here (same reasons as audit_quiz_answers.py).
NOT_RUNNABLE = {"S-02", "S-16", "S-17", "S-18", "S-19", "S-20", "S-21", "S-22"}

MAX_SENTENCE_WORDS = 30
MAX_AVG_SENTENCE_WORDS = 20
MIN_EXPLANATION_WORDS = 8

# Words that carry no meaning when picking out a topic's keywords.
STOPWORDS = {"the", "a", "an", "and", "or", "of", "to", "how", "what", "why",
             "actually", "is", "basic", "simple", "with", "your", "own", "informal",
             "matters", "&", "/", "it", "basics", "program", "runs", "code"}


# ─── loading ────────────────────────────────────────────────

def load_topics() -> list[dict]:
    data = json.loads(SYLLABUS_PATH.read_text())
    return data["spine"]["topics"]


def lesson_path(topic_id: str) -> Path | None:
    matches = [p for p in LESSONS_DIR.glob(f"{topic_id}_*.md")]
    return matches[0] if matches else None


def split_sections(md: str) -> dict[str, str]:
    """Map section title → body. 'The project: X' is stored as 'The project'."""
    out, current, buf = {}, None, []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if current:
                out[current] = "\n".join(buf).strip()
            title = m.group(1).strip()
            current = "The project" if title.startswith("The project") else title
            buf = []
        elif current:
            buf.append(line)
    if current:
        out[current] = "\n".join(buf).strip()
    return out


def fences(text: str) -> list[tuple[str, str]]:
    """All fenced blocks as (info string, body), read line by line so a
    closing ``` is never mistaken for an opening one."""
    out, info, body, inside = [], "", [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if inside:
                out.append((info, "\n".join(body) + "\n"))
                inside, body = False, []
            else:
                inside, info = True, line.strip()[3:].strip()
            continue
        if inside:
            body.append(line)
    return out


def python_blocks(text: str) -> list[str]:
    """Plain runnable Python blocks (not output, not expect-error)."""
    return [b for info, b in fences(text)
            if (info.split() or [""])[0] in ("python", "") and "expect-error" not in info]


def keywords(title: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]+", title.lower())
    out = set()
    for w in words:
        if w in STOPWORDS or len(w) < 3:
            continue
        out.add(w.rstrip("s"))  # "loops" → "loop", "functions" → "function"
    return out


def prose_only(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def sentences(text: str) -> list[str]:
    text = re.sub(r"^#.*$", "", prose_only(text), flags=re.MULTILINE)  # headings aren't sentences
    text = re.sub(r"`[^`]*`", "X", text)
    text = re.sub(r"[*#]", "", text)
    parts = re.split(r"(?<=[.!?])\s+|\n\s*\n", text)
    return [p.strip() for p in parts if len(p.split()) >= 3]


# ─── hard checks ───────────────────────────────────────────

class Report:
    def __init__(self, topic_id: str):
        self.topic_id = topic_id
        self.rows: list[tuple[str, str, str]] = []  # (status, check, detail)

    def add(self, ok: bool | None, check: str, detail: str = ""):
        status = "SKIP" if ok is None else ("PASS" if ok else "FAIL")
        self.rows.append((status, check, detail))

    @property
    def failed(self) -> int:
        return sum(1 for s, _, _ in self.rows if s == "FAIL")


def run_python_full(code: str) -> tuple[int, str, str]:
    """Run code, return (exit code, stdout, last line of stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "lesson_code.py"
        f.write_text(code)
        try:
            r = subprocess.run([sys.executable, "-I", str(f)], cwd=tmp, capture_output=True,
                               text=True, timeout=10, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return 124, "", "timed out after 10s"
    return r.returncode, r.stdout, (r.stderr.strip().splitlines() or [""])[-1]


def check_shown_outputs(rep: Report, topic: dict, md: str):
    """Every ```output block must be exactly what the Python block just above
    it prints (```output-head / ```output-tail: its first / last lines).
    A ```python expect-error=NameError block must really raise that error,
    and its ```output must match the error message exactly. Checks the whole
    lesson, not just Building it, so fold-outs are covered too."""
    if topic["id"] in NOT_RUNNABLE:
        return
    last = None  # (description, stdout lines, error line or None)
    pending = []  # output shown before any code (e.g. "here's what we'll build"): matched to the next code
    for info, body in fences(md):
        lang = (info.split() or [""])[0]
        if lang in ("python", ""):
            expect = re.search(r"expect-error=(\w+)", info)
            code, out, err = run_python_full(body)
            label = f"block starting {body.strip().splitlines()[0][:40]!r}" if body.strip() else "empty block"
            if expect:
                ok = code != 0 and err.startswith(expect.group(1))
                rep.add(ok, f"code: {label} raises {expect.group(1)} as the lesson says",
                        "" if ok else f"actually: {'no error' if code == 0 else err}")
                last = (label, [], err)
            else:
                rep.add(code == 0, f"code: {label} runs", "" if code == 0 else err)
                last = (label, out.rstrip("\n").split("\n") if out else [], None)
                for shown in pending:
                    ok = shown == last[1]
                    rep.add(ok, f"output: preview shown before the code matches what {label} prints",
                            "" if ok else f"preview {shown[:2]}..., Python prints {last[1][:2]}...")
                pending = []
        elif lang in ("output", "output-head", "output-tail"):
            shown = body.rstrip("\n").split("\n")
            if last is None:
                pending.append(shown)
                continue
            label, real, err = last
            if err is not None:
                ok = shown == [err]
                rep.add(ok, f"output: error shown for {label} is the real one",
                        "" if ok else f"lesson shows {shown}, Python says {err!r}")
                continue
            want = {"output": real, "output-head": real[:len(shown)], "output-tail": real[-len(shown):]}[lang]
            ok = shown == want
            detail = ""
            if not ok:
                diff = next((k for k in range(max(len(shown), len(want))) if k >= len(shown) or k >= len(want) or shown[k] != want[k]), 0)
                detail = (f"line {diff + 1}: lesson shows {shown[diff] if diff < len(shown) else '(nothing)'!r}, "
                          f"Python prints {want[diff] if diff < len(want) else '(nothing)'!r}")
            rep.add(ok, f"output: {lang} after {label} matches what Python really prints", detail)


def run_python(code: str) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "lesson_code.py"
        f.write_text(code)
        try:
            r = subprocess.run([sys.executable, "-I", str(f)], cwd=tmp, capture_output=True,
                               text=True, timeout=10, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return False, "timed out after 10s"
    if r.returncode != 0:
        return False, (r.stderr.strip().splitlines() or ["unknown error"])[-1]
    return True, r.stdout


def check_structure(rep: Report, sec: dict[str, str]):
    missing = [s for s in SECTIONS if s not in sec]
    rep.add(not missing, "structure: all 6 sections present",
            f"missing: {', '.join(missing)}" if missing else "")
    order = [s for s in sec if s in SECTIONS]
    rep.add(order == [s for s in SECTIONS if s in sec], "structure: sections in teaching order",
            "" if order == [s for s in SECTIONS if s in sec] else f"found order: {order}")
    empty = [s for s in SECTIONS if s in sec and len(prose_only(sec[s]).split()) < 8]
    rep.add(not empty, "structure: no empty sections", f"too short: {empty}" if empty else "")


def check_code(rep: Report, topic: dict, sec: dict[str, str]) -> list[str]:
    building = sec.get("Building it", "")
    if topic["id"] in NOT_RUNNABLE:
        has_any = "```" in building
        rep.add(has_any, "building it: has a code block", "" if has_any else "no code block found")
        rep.add(None, "building it: code runs", "not Python, or not runnable on its own here")
        return []
    blocks = python_blocks(building)
    if not blocks:
        rep.add(False, "building it: has a Python code block", "no ```python block found")
        return []
    outputs = []
    for i, code in enumerate(blocks, 1):
        ok, out = run_python(code)
        rep.add(ok, f"building it: code block {i} runs", "" if ok else out)
        outputs.append(out if ok else "")
    # Every name the code defines should be explained in the walkthrough prose.
    walkthrough = prose_only(sec.get("Building it", ""))
    names = set()
    for code in blocks:
        names |= set(re.findall(r"^\s*([a-z_][a-z0-9_]*)\s*=", code, flags=re.MULTILINE))
        names |= set(re.findall(r"^\s*def\s+([a-z_][a-z0-9_]*)", code, flags=re.MULTILINE))
    # A name that's created but never used is dead weight, or worse, a sign
    # the code only pretends to use its inputs (e.g. count = 5, then a
    # hard-coded list of 5 numbers).
    unused = []
    for code in blocks:
        for n in set(re.findall(r"^\s*([a-z_][a-z0-9_]*)\s*=", code, flags=re.MULTILINE)):
            if len(re.findall(rf"\b{re.escape(n)}\b", code)) < 2:
                unused.append(n)
    rep.add(not unused, "building it: every name the code creates gets used",
            f"created but never used: {sorted(unused)}" if unused else "")
    # A name counts as explained only when the prose mentions it as code, in
    # backticks. Matching plain words let a variable called `total` pass just
    # because the text said "the total printed".
    spans = re.findall(r"`([^`]+)`", walkthrough)
    unexplained = sorted(n for n in names if not any(re.search(rf"\b{re.escape(n)}\b", sp) for sp in spans))
    rep.add(not unexplained, "building it: walkthrough explains every name the code creates",
            f"never mentioned outside the code: {unexplained}" if unexplained else "")
    return outputs


def check_neighbours(rep: Report, topics: list[dict], idx: int, sec: dict[str, str]):
    nxt = topics[idx + 1] if idx + 1 < len(topics) else None
    earlier = topics[:idx]
    whats_next = sec.get("What's next", "").lower()

    if nxt is None:
        rep.add(None, "what's next: names the real next topic", "last lesson in the spine")
    else:
        kw = keywords(nxt["topic"])
        hit = any(k in whats_next for k in kw)
        rep.add(hit, "what's next: names the real next topic",
                "" if hit else f"next lesson is '{nxt['topic']}', section never mentions {sorted(kw)}")

    names_next = nxt is not None and any(k in whats_next for k in keywords(nxt["topic"]))
    backwards = [] if names_next else [t["topic"] for t in earlier[-4:]
                 if keywords(t["topic"]) and all(k in whats_next for k in keywords(t["topic"]))
                 and not (nxt and keywords(nxt["topic"]) & keywords(t["topic"]))]
    rep.add(not backwards, "what's next: doesn't point back at an earlier lesson",
            f"teases a topic already taught: {backwards}" if backwards else "")

    why = sec.get("Why this matters", "").lower()
    if "next lesson" in why and nxt:
        hit = any(k in why for k in keywords(nxt["topic"]))
        rep.add(hit, "why this matters: 'next lesson' claim matches the real next lesson",
                "" if hit else f"promises something about the next lesson, but it's '{nxt['topic']}'")


def check_quiz(rep: Report, topic: dict, outputs: list[str]):
    quiz = topic.get("quiz", [])
    if not quiz:
        rep.add(False, "quiz: has questions", "no quiz")
        return
    all_output = "\n".join(outputs)
    for i, q in enumerate(quiz, 1):
        text = q["question"]
        vague = re.search(r"\bthis (loop|code|function|snippet|list|dictionary)\b|\bthe (code|snippet|loop) above\b", text, re.I)
        has_code = bool(re.search(r"[a-z_]+\(|=|\[|\{|<code>", text))
        ok = not (vague and not has_code)
        rep.add(ok, f"quiz q{i}: answerable without guessing which code it means",
                "" if ok else f"says '{vague.group(0)}' but shows no code: \"{text}\"")
        expl = q.get("explanation", "")
        answer_text = str(q["options"][q["answer"]]) if q.get("type") == "choice" else str(q["answer"])
        teaches = len(expl.split()) >= MIN_EXPLANATION_WORDS and \
            expl.lower().strip(". ") != answer_text.lower().strip(". ")
        rep.add(teaches, f"quiz q{i}: explanation says WHY, not just the answer",
                "" if teaches else f"explanation: \"{expl}\"")
        if q.get("type") == "text" and all_output:
            # If the question quotes a range(...) call, compute the truth directly.
            m = re.search(r"range\((\d+),\s*(\d+)\)", text)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                truth = str(a) if "first" in text.lower() else str(b - a) if "how many" in text.lower() else None
                if truth is not None:
                    rep.add(str(q["answer"]).strip() == truth, f"quiz q{i}: stored answer is correct",
                            "" if str(q["answer"]).strip() == truth else f"stored '{q['answer']}', real answer '{truth}'")


def check_readability(rep: Report, md: str):
    sents = sentences(md)
    long = [s for s in sents if len(s.split()) > MAX_SENTENCE_WORDS]
    rep.add(not long, f"readability: no sentence over {MAX_SENTENCE_WORDS} words",
            "; ".join(f"({len(s.split())} words) \"{s[:90]}...\"" for s in long[:3]))
    avg = sum(len(s.split()) for s in sents) / max(len(sents), 1)
    rep.add(avg <= MAX_AVG_SENTENCE_WORDS, f"readability: average sentence ≤ {MAX_AVG_SENTENCE_WORDS} words",
            f"average is {avg:.1f}")
    dashes = re.findall(r"\s[-—–]\s|—|–", re.sub(r"`[^`]*`", "X", prose_only(md)))  # a minus inside `code` is maths, not a dash
    rep.add(not dashes, "voice: no dashes in prose", f"{len(dashes)} found" if dashes else "")


def check_tool(rep: Report, topic: dict, outputs: list[str]):
    tool = SITE_DIR / "templates/syllabus_tools" / f"{topic['id']}.html"
    if not tool.exists() or not any(outputs):
        return
    html = tool.read_text()
    first_lines = [l for o in outputs for l in o.splitlines() if l.strip()]
    # Only compare labelled output like "Invoice Number: 1001"; raw data
    # (lists, random passwords, timings) isn't a format the tool should copy.
    m = re.match(r"^([A-Z][A-Za-z ]{3,}?)\s*[:#]\s*\S", first_lines[0]) if first_lines else None
    if not m:
        return
    label = m.group(1).strip()
    rep.add(label in html, "tool: prints the same format the lesson teaches",
            "" if label in html else f"lesson prints '{first_lines[0]}', tool never outputs '{label}'")


# Where each piece of syntax is first taught. Code in an earlier lesson that
# uses it leaves the reader staring at something nobody explained.
CONCEPT_FIRST_TAUGHT = [
    (r"^\s*import\s|^\s*from\s+\S+\s+import", "import", "S-13"),
    (r"^\s*if\s|^\s*elif\s|^\s*else\s*:", "if / else", "S-09"),
    (r"^\s*for\s|^\s*while\s", "loops", "S-10"),
    (r"^\s*def\s", "functions (def)", "S-11"),
    (r"^\s*try\s*:", "try / except", "S-14"),
    (r"\bopen\(", "files (open)", "S-15"),
    (r"^\s*class\s", "classes", "S-23"),
    (r"\[[^\]\n]*\bfor\b[^\]\n]*\bin\b[^\]\n]*\]|\{[^}\n]*\bfor\b[^}\n]*\bin\b[^}\n]*\}|\(\S[^)\n]*\bfor\b[^)\n]*\bin\b", "comprehensions", "S-24"),
]


def topic_num(topic_id: str) -> int:
    return int(topic_id.split("-")[1])


def check_untaught(rep: Report, topic: dict, sec: dict[str, str]):
    if not topic["id"].startswith("S-"):
        return
    code = "\n".join(python_blocks(sec.get("Building it", "")))
    early = [f"{name} (taught in {tid})" for pattern, name, tid in CONCEPT_FIRST_TAUGHT
             if topic_num(tid) > topic_num(topic["id"]) and re.search(pattern, code, flags=re.MULTILINE)]
    rep.add(not early, "building it: code only uses what's been taught so far",
            f"uses ideas from later lessons: {', '.join(early)}" if early else "")


def site_context(topic_id: str) -> str:
    """The try-it box and live tool text for this lesson, so the reviewer can
    check they agree with the lesson and are true."""
    parts = []
    tpl = SITE_DIR / "templates/syllabus_lesson.html"
    if tpl.exists():
        m = re.search(r"\{% if topic.id == '" + re.escape(topic_id) + r"' %\}(.*?)\{% endif %\}", tpl.read_text(), re.S)
        if m:
            parts.append("TRY-IT BOX (HTML + JS):\n" + _compact(m.group(1))[:3500])
    tool = SITE_DIR / "templates/syllabus_tools" / f"{topic_id}.html"
    if tool.exists():
        parts.append("LIVE TOOL (HTML + JS):\n" + _compact(tool.read_text())[:2000])
    return "\n\n".join(parts) or "(none)"


def _compact(html_text: str) -> str:
    """Drop styling and collapse whitespace: the reviewer needs the words and
    the logic, not the CSS, and the free API tier caps tokens per minute."""
    html_text = re.sub(r"<style.*?</style>", "", html_text, flags=re.S)
    html_text = re.sub(r'\s(class|style)="[^"]*"', "", html_text)
    return re.sub(r"\s+", " ", html_text).strip()


# ─── reviewer (LLM) ────────────────────────────────────────

JUDGE_RUBRIC = """You are reviewing one lesson of a free coding course. The reader is a total
beginner: they work in finance, have never written code, and read this on their phone.
Your job is to find where a beginner would get confused or lost. Be strict.

Grade each check PASS or FAIL. For every FAIL you MUST quote the exact words from the
lesson that cause the problem, and give a one-sentence fix. No quote, no FAIL.

Checks:
1. idea_analogy_first: "The idea" opens with an everyday analogy BEFORE any technical term.
2. idea_analogy_fits: the analogy actually matches how the concept works (not just loosely related).
3. idea_to_project_bridge: "The project" connects back to the analogy or idea, so the reader sees why THIS project uses THIS concept. A cold jump to the project is a FAIL.
4. project_matches_code: go through the final code line by line. It must really do what "The project" says it builds, using the inputs the project describes (e.g. if the project takes a start number and a count, the loop must be driven by those variables). Typed-out values where the project promises they are generated or calculated are a FAIL, even if the printed output looks right. Variables that are set but never used are a FAIL.
5. code_steps_small: each new code block adds at most one new idea, and the reader is told why the next step is needed before seeing it.
6. walkthrough_plain: the walkthrough explains each line in plain words, in the order the lines appear.
7. jargon_defined: every NEW technical term (e.g. iteration, keyword, range) is explained in plain words the first time it appears. Terms from earlier lessons count as known: {already_taught}. List every undefined new term in the quote.
8. why_concrete: "Why this matters" names concrete, real situations a finance worker recognises, and makes no promise about future lessons that isn't backed up.
9. mistake_on_topic: "The mistake beginners make here" is a mistake specific to THIS concept, with what the error looks like and how to avoid it.
10. whats_next_correct: "What's next" teases exactly this next topic: {next_topic}. Anything else is a FAIL.
11. flow: reading top to bottom, each section follows naturally from the one before. Note any spot where the reader would think "wait, why are we doing this now?".

Lesson topic: {topic}
Previous lesson: {prev_topic}
Next lesson: {next_topic}
Project: {project}

Return only JSON:
{{"checks": [{{"id": "idea_analogy_first", "pass": true, "quote": "", "fix": ""}}, ...]}}

LESSON:
{lesson}"""


ACCURACY_RUBRIC = """You are a senior software engineer fact-checking one lesson of a free coding
course before it is published. Beginners will copy what it says, so a wrong claim does
real harm. Check every sentence, every code line, every quiz answer. Assume current
tool versions on a Mac: Python 3.9+, git 2.28+ (default branch "main"), modern browsers.

Grade each check PASS or FAIL. For every FAIL you MUST quote the exact wrong words and
say what is actually true. No quote, no FAIL. Simplifications for beginners are fine;
statements that are false or would mislead someone are not.

Checks:
1. claims_true: every statement about how code, Python, the terminal, git, GitHub, HTML,
   CSS, JavaScript or a library behaves is true. Includes code comments.
2. code_works: following the lesson exactly (including any install or setup steps it
   gives) the code runs and does what the lesson says. Missing install steps a beginner
   needs, or commands that fail on current versions, are a FAIL.
3. safe_practice: nothing teaches a bad or unsafe habit (e.g. printing secrets, random
   instead of secrets for passwords, committing .env, catching every error silently).
4. quiz_correct: every quiz answer is right, unambiguous, and its explanation is true.
5. site_matches: the try-it box and live tool below are technically true and agree with
   the lesson (same code, same behaviour, same claims). If none, PASS.
6. prompt_matches: the copy-prompt asks for the same thing the lesson teaches, and would
   not lead an AI to produce something that contradicts the lesson.

Return only JSON:
{{"checks": [{{"id": "claims_true", "pass": true, "quote": "", "fix": ""}}, ...]}}

LESSON:
{lesson}

QUIZ (answer is an index into options for choice questions):
{quiz}

COPY-PROMPT:
{ai_prompt}

{site}"""


class DailyLimitReached(Exception):
    """The reviewer model has used its free daily allowance."""


TOKENS_PER_MINUTE = 8000  # Groq free tier limit per request (prompt + max_tokens)
# The reviewer runs on its own model. Groq's free tier gives each model its own
# daily token allowance, and the live site and the newsletter use gpt-oss-120b.
# A full review of 25 lessons would otherwise use up the site's allowance for
# the day (it did, on 2026-10-08), so reviewing can never take the tools down.
QA_MODEL = os.getenv("QA_MODEL", "openai/gpt-oss-20b")


def _ask(client, prompt: str, effort: str) -> list[dict]:
    import time
    # gpt-oss is a reasoning model: its thinking counts against max_tokens, so
    # give it all the room the per-minute cap leaves, or the JSON gets cut off.
    est_prompt = len(prompt) // 3
    max_tokens = max(1500, TOKENS_PER_MINUTE - est_prompt - 300)
    for attempt in range(6):
        try:
            resp = client.chat.completions.create(
                model=QA_MODEL, messages=[{"role": "user", "content": prompt}],
                temperature=0, max_tokens=max_tokens, reasoning_effort=effort,
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content).get("checks", [])
        except Exception as e:  # rate limit or truncated JSON: wait out the minute, retry
            msg = str(e)
            if "per day" in msg:
                raise DailyLimitReached(msg) from None
            if "rate_limit" in msg or "429" in msg or "json_validate_failed" in msg:
                time.sleep(65)
                continue
            raise
    raise RuntimeError("reviewer kept hitting the rate limit, try again in a few minutes")


def _record(rep: Report, prefix: str, runs: list[list[dict]]):
    """Each lesson is reviewed more than once, independently. A check only
    FAILs when every review fails it with quoted evidence: real defects fail
    every time, while a one-off misreading by the reviewer doesn't repeat.
    A split verdict is shown as SKIP with the evidence, for a human to look at."""
    ids = []
    for run in runs:
        for c in run:
            if c.get("id") not in ids:
                ids.append(c.get("id"))
    for cid in ids:
        verdicts = [next((c for c in run if c.get("id") == cid), None) for run in runs]
        fails = [c for c in verdicts if c is not None and not c.get("pass") and c.get("quote")]
        first = fails[0] if fails else None
        detail = f"\"{first.get('quote', '')}\" → fix: {first.get('fix', '')}" if first else ""
        if not fails:
            rep.add(True, f"{prefix}: {cid}")
        elif len(fails) == len(runs):
            rep.add(False, f"{prefix}: {cid}", detail)
        else:
            rep.add(None, f"{prefix}: {cid}", f"reviews disagree ({len(fails)} of {len(runs)} failed it), check manually: {detail}")


JUDGE_RUNS = 2  # a FAIL must be confirmed by a second, independent review


def _confirmed_runs(client, prompt: str, effort: str) -> list[list[dict]]:
    """Review once. Only if something failed, review again so the failure has
    to be confirmed. A clean lesson costs one call instead of two."""
    runs = [_ask(client, prompt, effort)]
    if any(not c.get("pass") for c in runs[0]):
        runs += [_ask(client, prompt, effort) for _ in range(JUDGE_RUNS - 1)]
    return runs


def judge(rep: Report, topics: list[dict], idx: int, md: str):
    try:
        from dotenv import load_dotenv
        from groq import Groq
    except ImportError as e:
        rep.add(None, "reviewer", f"missing package: {e}")
        return
    load_dotenv(ROOT / ".env")
    key = os.getenv("GROQ_API_KEY")
    if not key:
        rep.add(None, "reviewer", "GROQ_API_KEY not set in .env")
        return
    t = topics[idx]
    prompt = JUDGE_RUBRIC.format(
        topic=t["topic"],
        prev_topic=topics[idx - 1]["topic"] if idx > 0 else "none (first lesson)",
        next_topic=topics[idx + 1]["topic"] if idx + 1 < len(topics) else "none (last lesson)",
        already_taught=", ".join(x["topic"] for x in topics[:idx]) or "nothing yet",
        project=f"{t.get('project', {}).get('title', '')}: {t.get('project', {}).get('description', '')}",
        lesson=md,
    )
    client = Groq(api_key=key)
    _record(rep, "reviewer", _confirmed_runs(client, prompt, "low"))
    # Accuracy gets its own, deeper pass: a wrong fact is worse than a clunky sentence.
    acc_prompt = ACCURACY_RUBRIC.format(
        lesson=md, quiz=json.dumps(t.get("quiz", []), indent=1),
        ai_prompt=t.get("ai_prompt", "(none)"), site=site_context(t["id"]))
    _record(rep, "accuracy", _confirmed_runs(client, acc_prompt, "medium"))


# ─── main ──────────────────────────────────────────────────

def check_topic(topics: list[dict], idx: int, use_judge: bool) -> Report:
    topic = topics[idx]
    rep = Report(topic["id"])
    path = lesson_path(topic["id"])
    if not path:
        rep.add(False, "lesson file exists", f"no {topic['id']}_*.md in {LESSONS_DIR}")
        return rep
    md = path.read_text()
    sec = split_sections(md)
    check_structure(rep, sec)
    outputs = check_code(rep, topic, sec)
    check_neighbours(rep, topics, idx, sec)
    check_quiz(rep, topic, outputs)
    check_readability(rep, md)
    check_tool(rep, topic, outputs)
    check_untaught(rep, topic, sec)
    check_shown_outputs(rep, topic, md)
    if use_judge:
        judge(rep, topics, idx, md)
    return rep


def print_report(rep: Report, topic: dict, verbose: bool):
    colour = {"PASS": "\033[32m", "FAIL": "\033[31m", "SKIP": "\033[33m"}
    reset = "\033[0m"
    head = "RED" if rep.failed else "GREEN"
    print(f"\n{colour['FAIL' if rep.failed else 'PASS']}{head}{reset}  {topic['id']} {topic['topic']}"
          f"  ({rep.failed} failing)")
    for status, check, detail in rep.rows:
        if status == "PASS" and not verbose:
            continue
        print(f"  {colour[status]}{status}{reset}  {check}" + (f"\n        {detail}" if detail else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--topic", help="e.g. S-10")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--judge", action="store_true", help="add the AI reviewer (1 Groq call per lesson)")
    ap.add_argument("-v", "--verbose", action="store_true", help="also list passing checks")
    ap.add_argument("--syllabus", help="syllabus JSON (default: config/coding_syllabus.json)")
    ap.add_argument("--lessons-dir", help="lesson .md folder (default: content/syllabus_lessons)")
    args = ap.parse_args()

    global SYLLABUS_PATH, LESSONS_DIR
    if args.syllabus:
        SYLLABUS_PATH = Path(args.syllabus).resolve()
    if args.lessons_dir:
        LESSONS_DIR = Path(args.lessons_dir).resolve()

    topics = load_topics()
    ids = [t["id"] for t in topics]
    if args.topic:
        if args.topic not in ids:
            sys.exit(f"Unknown topic {args.topic}. Known: {', '.join(ids)}")
        targets = [ids.index(args.topic)]
    else:
        targets = [i for i, t in enumerate(topics) if lesson_path(t["id"])]

    total_failed = 0
    for i in targets:
        try:
            rep = check_topic(topics, i, args.judge)
        except DailyLimitReached:
            print(f"\nStopped at {topics[i]['id']}: {QA_MODEL} has used its free daily allowance "
                  f"(200,000 tokens per rolling 24 hours). Resume later with --topic {topics[i]['id']}.")
            sys.exit(2)
        print_report(rep, topics[i], args.verbose)
        total_failed += rep.failed
    if len(targets) > 1:
        red = sum(1 for i in targets if check_topic(topics, i, False).failed)
        print(f"\n{len(targets) - red}/{len(targets)} lessons green on hard checks")
    sys.exit(1 if total_failed else 0)


if __name__ == "__main__":
    main()
