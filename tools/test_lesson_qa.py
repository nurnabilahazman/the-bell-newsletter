#!/usr/bin/env python3
"""
Tests the lesson checker itself (tools/lesson_qa.py).

A checker is only worth trusting if it is tested. This takes a lesson that
passes every check (S-10), plants ONE known defect at a time, and confirms
the checker flags it with the RIGHT check. It also re-checks the clean lesson
several times to confirm the AI reviewer doesn't invent problems.

    caught   = the planted defect turned the expected check red   (good)
    missed   = the defect got through                             (checker is too weak)
    false fail on clean lesson                                    (checker is too strict)

Usage:
    python3 tools/test_lesson_qa.py            # hard checks only (free, instant)
    python3 tools/test_lesson_qa.py --judge    # plus AI reviewer defects (~10 Groq calls)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lesson_qa as qa  # noqa: E402

BASE_TOPIC = "S-10"


def _replace(old: str, new: str):
    def apply(md: str, syl: dict):
        assert old in md, f"seed text not found: {old[:50]}"
        return md.replace(old, new, 1), syl
    return apply


def _quiz(field: str, value, q: int = 0):
    def apply(md: str, syl: dict):
        t = next(t for t in syl["spine"]["topics"] if t["id"] == BASE_TOPIC)
        t["quiz"][q][field] = value
        return md, syl
    return apply


# (name, what's wrong, mutation, check that MUST turn red)
HARD_DEFECTS = [
    ("missing section", "'Why this matters' deleted",
     _replace("## Why this matters\n", "\n"), "structure: all 6 sections present"),
    ("broken code", "typo makes the code crash",
     _replace('    print(f"Invoice Number: {number}")\n```\nHere is what each line does',
              '    pritn(f"Invoice Number: {number}")\n```\nHere is what each line does'),
     "building it: code block 1 runs"),
    ("wrong next lesson", "teases conditionals (already taught) instead of functions",
     _replace("Next, we'll learn about **functions**, which let you give a block of code a name, like `make_invoices`, and reuse it whenever you need it.",
              "Next, we'll learn about **conditionals (if / else)**, which let your code make decisions."),
     "what's next: names the real next topic"),
    ("points backwards", "same mutation, second check",
     _replace("Next, we'll learn about **functions**, which let you give a block of code a name, like `make_invoices`, and reuse it whenever you need it.",
              "Next, we'll learn about **conditionals (if / else)**, which let your code make decisions."),
     "what's next: doesn't point back at an earlier lesson"),
    ("false promise", "'why this matters' promises the next lesson covers loops",
     _replace("You write the step once and the loop repeats it.",
              "In the next lesson we'll use loops in a real application."),
     "why this matters: 'next lesson' claim matches the real next lesson"),
    ("vague quiz", "question says 'this loop' with no code",
     _quiz("question", "This loop prints one number per line. What is the very first number it prints?"),
     "quiz q1: answerable without guessing which code it means"),
    ("empty explanation", "explanation just repeats the answer",
     _quiz("explanation", "It prints 1001."), "quiz q1: explanation says WHY, not just the answer"),
    ("wrong answer", "stored answer is 1002, truth is 1001",
     _quiz("answer", "1002"), "quiz q1: stored answer is correct"),
    ("long sentence", "a 40 word run-on sentence",
     _replace("You write the step once.",
              "You write the step once and then the computer takes that single step and repeats it over and over for every single item you give it until there are no more items left in the list and then it finally stops running."),
     "readability: no sentence over 30 words"),
    ("dash", "em dash in prose",
     _replace("You write the step once.", "You write the step once — the computer does the rest."),
     "voice: no dashes in prose"),
    ("unexplained name", "code creates `total` the walkthrough never mentions",
     _replace("start = 1001\ncount = 5\n", "start = 1001\ncount = 5\ntotal = 0\n"),
     "building it: walkthrough explains every name the code creates"),
    ("fake generation", "count/start set but loop uses typed-out numbers",
     _replace("for number in range(start, start + count):", "for number in [1001, 1002, 1003, 1004, 1005]:"),
     "building it: every name the code creates gets used"),
    ("future concept", "code wraps the loop in a function before functions are taught",
     _replace("start = 1001\ncount = 5\n\nfor number in range(start, start + count):\n    print(f\"Invoice Number: {number}\")",
              "def make_invoices(start, count):\n    for number in range(start, start + count):\n        print(f\"Invoice Number: {number}\")\n\nmake_invoices(1001, 5)"),
     "building it: code only uses what's been taught so far"),
    ("tool mismatch", "lesson prints 'Receipt No:' but tool prints 'Invoice Number:'",
     lambda md, syl: (md.replace('print(f"Invoice Number: {number}")', 'print(f"Receipt No: {number}")'), syl),
     "tool: prints the same format the lesson teaches"),
]

JUDGE_DEFECTS = [
    ("no analogy", "opens with a dry definition, analogy removed",
     lambda md, syl: (md.split("## The idea\n")[0] + "## The idea\nA **loop** is a control flow construct that executes a block of statements repeatedly for each element of an iterable. You write the step once. The computer repeats it.\n\n## The project" + md.split("## The project", 1)[1], syl),
     "reviewer: idea_analogy_first"),
    ("cold project jump", "project paragraph no longer connects to the idea",
     _replace("We're going to build that invoice book stamper. You tell it the first invoice number and how many invoices you need. It prints every number in order, one per line. Each line is one \"stamp\", and the loop is what turns the page.",
              "This week's project is a Batch Invoice Number Generator. Businesses use invoice numbers."),
     "reviewer: idea_to_project_bridge"),
    ("code doesn't do the project", "step 2 hard-codes numbers but claims to generate them",
     _replace("start = 1001\ncount = 5\n\nfor number in range(start, start + count):",
              "start = 1001\ncount = 5\n\nfor number in [1001, 1002, 1003, 1004, 1005]:"),
     "reviewer: project_matches_code"),
    ("undefined jargon", "drops in 'iterable' and 'control flow' with no explanation",
     _replace("The loop runs the print line three times.",
              "Because a list is an iterable, the control flow re-enters the suite on each pass. The loop runs the print line three times."),
     "reviewer: jargon_defined"),
    ("off-topic mistake", "mistake section is about saving files, not loops",
     lambda md, syl: (md.split("## The mistake beginners make here\n")[0] + "## The mistake beginners make here\nA common mistake is forgetting to save your file before running it. Always press save first so your latest changes are used.\n\n## What's next" + md.split("## What's next", 1)[1], syl),
     "reviewer: mistake_on_topic"),
    ("false fact", "says range includes the end number",
     _replace("That's exactly 5 numbers.", "range includes the end number too, so you also get 1006."),
     "accuracy: claims_true"),
    ("wrong quiz explanation", "explanation claims range includes both ends",
     _quiz("explanation", "range includes both the first and the last number you give it, so you get 1001 to 1006.", 1),
     "accuracy: quiz_correct"),
    ("prompt mismatch", "copy-prompt asks for something unrelated to the lesson",
     lambda md, syl: (md, {**syl, "spine": {**syl["spine"], "topics": [
         {**t, "ai_prompt": "Build me a Python script that asks for my bank password and prints it back to me so I can check it."}
         if t["id"] == BASE_TOPIC else t for t in syl["spine"]["topics"]]}}),
     "accuracy: prompt_matches"),
    ("vague why", "'why this matters' is a platitude",
     lambda md, syl: (md.split("## Why this matters\n")[0] + "## Why this matters\nLoops are an important concept that is useful in many areas of programming and will help you become a better developer.\n\n## The mistake" + md.split("## The mistake", 1)[1], syl),
     "reviewer: why_concrete"),
]


def run_case(src_lessons: Path, src_syllabus: Path, mutate, use_judge: bool):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        lessons = tmp / "lessons"
        shutil.copytree(src_lessons, lessons, ignore=shutil.ignore_patterns("carousel_pdfs", "*.json"))
        syl = json.loads(src_syllabus.read_text())
        path = next(lessons.glob(f"{BASE_TOPIC}_*.md"))
        md = path.read_text()
        if mutate:
            md, syl = mutate(md, syl)
        path.write_text(md)
        (tmp / "syllabus.json").write_text(json.dumps(syl))
        qa.SYLLABUS_PATH, qa.LESSONS_DIR = tmp / "syllabus.json", lessons
        topics = qa.load_topics()
        idx = [t["id"] for t in topics].index(BASE_TOPIC)
        rep = qa.check_topic(topics, idx, use_judge)
    return {check: status for status, check, _ in rep.rows}, rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--clean-runs", type=int, default=2, help="times to re-check the clean lesson with the reviewer")
    args = ap.parse_args()

    src_lessons, src_syllabus = qa.LESSONS_DIR, qa.SYLLABUS_PATH
    problems = 0

    print("1) Clean lesson must be fully green")
    runs = args.clean_runs if args.judge else 1
    for i in range(runs):
        _, rep = run_case(src_lessons, src_syllabus, None, args.judge)
        fails = [(c, d) for s, c, d in rep.rows if s == "FAIL"]
        print(f"   run {i + 1}: {'GREEN' if not fails else 'FALSE FAIL'}" +
              "".join(f"\n      {c}: {d}" for c, d in fails))
        problems += bool(fails)

    cases = HARD_DEFECTS + (JUDGE_DEFECTS if args.judge else [])
    print(f"\n2) Planted defects must each be caught ({len(cases)} cases)")
    for name, desc, mutate, expected in cases:
        statuses, _ = run_case(src_lessons, src_syllabus, mutate, args.judge and expected.startswith(("reviewer", "accuracy")))
        got = statuses.get(expected, "NOT RUN")
        ok = got == "FAIL"
        problems += not ok
        print(f"   {'caught' if ok else 'MISSED'}  {name:<26} {desc}" + ("" if ok else f"  (expected '{expected}' to fail, got {got})"))

    print(f"\n{'ALL GOOD' if not problems else f'{problems} PROBLEM(S)'}: checker "
          f"{'is' if not problems else 'is NOT yet'} reliable on these cases")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
