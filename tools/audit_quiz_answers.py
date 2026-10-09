#!/usr/bin/env python3
"""
Ground-truth audit for syllabus quiz answers.

The old self-consistency test only checks that a quiz's stored "answer"
matches itself when submitted, it never checks that the answer is actually
correct. This script instead treats each lesson's own "Building it" Python
code as the oracle: it actually runs that code with a real interpreter,
then evaluates or executes whatever the quiz question's <code> snippet is,
capturing real stdout and/or the real return value, and compares that to
the stored answer.

Only questions whose wording implies "what does this print / what is the
output / what is the result" are auto-verified. Questions that just
reference a snippet for context (e.g. "what TYPE of structure is X", "how
many items are in X") are skipped, since the snippet there isn't something
that alone defines the expected answer.

For anything this can't safely or meaningfully verify (non-Python code,
missing third-party packages, real randomness, real timing, side effects),
it reports SKIP with a reason instead of guessing.

Usage: python3 tools/audit_quiz_answers.py [--topic S-04]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

SYLLABUS_PATH = Path("config/coding_syllabus.json")
LESSONS_DIR = Path("content/syllabus_lessons")

SKIP_TOPICS = {
    "S-02": "shell commands, not Python",
    "S-12": "quiz answer is conceptual (search type), not a value from running the code",
    "S-13": "uses real randomness, output is different every run by design",
    "S-15": "does real file I/O, answer is conceptual (what 'w' mode does)",
    "S-16": "needs the qrcode package, not installed in this environment",
    "S-17": "needs the git package/a real repo, side-effecting",
    "S-18": "shells out to git via os.system, side-effecting",
    "S-19": "HTML, not Python",
    "S-20": "the code just assembles an HTML string, question is about a value inside it, not runnable in isolation",
    "S-22": "needs a real .env file with a real secret, answer is conceptual (library name)",
    "S-25": "uses datetime.now(), answer changes depending on when you run it",
}

# Only auto-verify questions that are actually asking "what does this
# produce", not questions that merely reference a snippet for context.
OUTPUT_QUESTION_HINTS = (
    "output of",
    "result of",
    "is printed",
    "will this print",
    "will be the output",
    "does this print",
)

PROBE_TEMPLATE = '''
import io, re, contextlib

{code_block}

def __audit_run(snippet):
    def _last_line(text):
        lines = text.rstrip("\\n").splitlines()
        return lines[-1] if lines else ""

    buf = io.StringIO()
    try:
        assign_match = re.match(r"^(\\w+)\\s*=\\s*(?!=)(.+)$", snippet.strip())
        if assign_match:
            varname = assign_match.group(1)
            with contextlib.redirect_stdout(buf):
                exec(snippet)
                result = eval(varname)
            stdout_text = buf.getvalue()
        else:
            try:
                with contextlib.redirect_stdout(buf):
                    result = eval(snippet)
            except SyntaxError:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    exec(snippet)
                result = None
            stdout_text = buf.getvalue()

        if callable(result) and not stdout_text.strip():
            buf2 = io.StringIO()
            with contextlib.redirect_stdout(buf2):
                result = result()
            stdout_text = buf2.getvalue()

        if stdout_text.strip():
            print("__AUDIT_OK__" + _last_line(stdout_text))
        else:
            print("__AUDIT_OK__" + str(result))
    except Exception as e:
        print("__AUDIT_ERR__" + str(e))

__audit_run({snippet!r})
'''


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def extract_code_block(lesson_text: str) -> str | None:
    m = re.search(r"## Building it\n.*?```\w*\n(.*?)```", lesson_text, re.S)
    return m.group(1) if m else None


def find_lesson_text(topic_id: str) -> str | None:
    for f in LESSONS_DIR.glob(f"{topic_id}_*.md"):
        return f.read_text()
    return None


def extract_code_snippets(question_html: str) -> list[str]:
    return [html.unescape(m) for m in re.findall(r"<code>(.*?)</code>", question_html)]


def is_output_question(question_html: str) -> bool:
    q = html.unescape(question_html).lower()
    return any(hint in q for hint in OUTPUT_QUESTION_HINTS)


def run_probe(code_block: str, snippet: str) -> tuple[str | None, str | None]:
    probe = PROBE_TEMPLATE.format(code_block=code_block, snippet=snippet)
    try:
        proc = subprocess.run(
            [sys.executable, "-c", probe], capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        return None, "timed out"
    if proc.returncode != 0:
        return None, (proc.stderr.strip().splitlines()[-1] if proc.stderr else "non-zero exit")
    for line in proc.stdout.splitlines():
        if line.startswith("__AUDIT_OK__"):
            return line[len("__AUDIT_OK__"):], None
        if line.startswith("__AUDIT_ERR__"):
            return None, line[len("__AUDIT_ERR__"):]
    return None, "no probe output captured"


def normalize(s: str) -> str:
    return " ".join(s.strip().split()).lower().rstrip("!.")


def audit_topic(topic: dict) -> list[dict]:
    tid = topic["id"]
    findings = []

    if tid in SKIP_TOPICS:
        findings.append({"status": "SKIP", "reason": SKIP_TOPICS[tid]})
        return findings

    lesson_text = find_lesson_text(tid)
    if not lesson_text:
        findings.append({"status": "SKIP", "reason": "lesson file not found"})
        return findings

    code_block = extract_code_block(lesson_text)
    if not code_block:
        findings.append({"status": "SKIP", "reason": "no 'Building it' code block found"})
        return findings

    quiz = topic.get("quiz", [])
    for i, q in enumerate(quiz, 1):
        if q["type"] != "text":
            findings.append({"status": "SKIP", "q": i, "reason": "choice questions aren't checked by this tool yet"})
            continue

        if not is_output_question(q["question"]):
            findings.append({"status": "SKIP", "q": i, "reason": "question doesn't ask for output/result, likely conceptual"})
            continue

        snippets = extract_code_snippets(q["question"])
        if not snippets:
            findings.append({"status": "SKIP", "q": i, "reason": "no <code> snippet in question"})
            continue

        print_snippets = [s for s in snippets if s.strip().startswith("print(")]
        snippet = print_snippets[0] if print_snippets else max(snippets, key=len)
        result, error = run_probe(code_block, snippet)

        if error:
            findings.append({"status": "SKIP", "q": i, "reason": f"could not run/eval '{snippet}': {error}"})
            continue

        stored = str(q["answer"])
        if normalize(result) == normalize(stored):
            findings.append({"status": "PASS", "q": i, "snippet": snippet, "real": result, "stored": stored})
        else:
            findings.append({"status": "MISMATCH", "q": i, "snippet": snippet, "real": result, "stored": stored})

    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Audit a single topic, e.g. S-04")
    args = parser.parse_args()

    data = load_json(SYLLABUS_PATH)
    topics = data["spine"]["topics"]
    if args.topic:
        topics = [t for t in topics if t["id"] == args.topic]

    total_pass = total_mismatch = total_skip = 0
    mismatches = []

    for topic in topics:
        for r in audit_topic(topic):
            if r["status"] == "PASS":
                total_pass += 1
                print(f"  {topic['id']} Q{r['q']}: PASS  ({r['snippet']} -> {r['real']})")
            elif r["status"] == "MISMATCH":
                total_mismatch += 1
                mismatches.append((topic["id"], r))
                print(f"  {topic['id']} Q{r['q']}: MISMATCH  stored={r['stored']!r} real={r['real']!r}  ({r['snippet']})")
            else:
                total_skip += 1
                q = f" Q{r['q']}" if "q" in r else ""
                print(f"  {topic['id']}{q}: SKIP  ({r['reason']})")

    print(f"\n{'=' * 60}")
    print(f"PASS: {total_pass}   MISMATCH: {total_mismatch}   SKIP: {total_skip}")
    if mismatches:
        print("\nMismatches need fixing:")
        for tid, r in mismatches:
            print(f"  {tid} Q{r['q']}: stored {r['stored']!r} but real Python gives {r['real']!r}")
        sys.exit(1)


if __name__ == "__main__":
    main()
