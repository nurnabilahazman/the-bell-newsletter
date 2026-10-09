#!/usr/bin/env python3
"""
Generates the "Try It Yourself" widget spec + 2-question "Check Yourself"
quiz for each spine lesson, matching the pattern piloted on S-01.

Reads:  config/coding_syllabus.json, content/syllabus_lessons/{id}_*.md
Writes: config/coding_syllabus.json (adds "try_it" and "quiz" per topic),
        synced to the Week 1 app's copy too.
Usage:  python tools/syllabus_quiz_generator.py --topic S-03
        python tools/syllabus_quiz_generator.py --all
"""

import argparse
import json
import os
import time
from pathlib import Path

from groq import Groq, RateLimitError
from groq_client import groq_create, MODEL as GROQ_MODEL
from dotenv import load_dotenv

load_dotenv()

SYLLABUS_PATH = Path("config/coding_syllabus.json")
WEEK1_SYLLABUS_PATH = Path("../Week 1_Excel Formula Generator/data/coding_syllabus.json")
LESSONS_DIR = Path("content/syllabus_lessons")

MODEL = GROQ_MODEL
DONE_IDS = {"S-01", "S-03"}  # already piloted/verified, skip unless --topic explicitly names it


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def find_lesson_text(topic_id: str) -> str:
    for f in LESSONS_DIR.glob(f"{topic_id}_*.md"):
        return f.read_text()
    return ""


def build_prompt(topic: dict, lesson_text: str) -> str:
    project = topic.get("project", {})
    return f"""You are designing a "Try It Yourself" mini-widget and a 2-question quiz for a
coding lesson aimed at total beginners (zero prior coding knowledge).

TOPIC: {topic['topic']}
CONCEPT: {topic.get('plain_english_summary', '')}
PROJECT: {project.get('title', '')} — {project.get('description', '')}

LESSON CONTENT (for grounding, use its actual code/examples):
{lesson_text[:2500]}

Design two things:

1. TRY_IT — a tiny, single-blank fill-in-the-code widget. Take ONE real line
from the lesson's code and split it into: text before the editable part
(prefix), the default value that goes in the blank (placeholder), and text
after (suffix). The reader edits ONLY the placeholder value and immediately
sees the effect echoed back EXACTLY as typed (the widget just mirrors
whatever they type, character for character, into an output box). This
means: the placeholder must be the BARE value only, with NO quote marks,
NO brackets, and NO trailing punctuation baked into it, because whatever
the reader types is treated as literal display text. If the value being
edited is a string in the real code (e.g. name = "John Doe"), put the
opening quote at the end of the prefix and the closing quote at the start
of the suffix, so the input box only ever contains John Doe with no quotes
around it — for example: prefix: 'name = "', placeholder: 'John Doe',
suffix: '"'. Pick the most illustrative single value to make editable for
this specific concept (a string, a number, a condition, whatever best
demonstrates the idea). Write one short hint (under 20 words) explaining
what changing it teaches.

2. QUIZ — exactly 2 questions testing whether they understood THIS topic,
grounded in the lesson's actual example:
   - Question 1: type "text" — a predict-the-output style question with a
     short, exact-match answer (a single word, number, or short phrase).
   - Question 2: type "choice" — 3 options, exactly one correct (0-indexed
     answer), testing a common misconception about this specific concept.
   Each question needs a one-sentence explanation (under 25 words) shown
   after they answer, regardless of right or wrong.

Respond with ONLY valid JSON, no markdown fences, in this exact shape:
{{
  "try_it": {{"prefix": "...", "suffix": "...", "placeholder": "...", "hint": "..."}},
  "quiz": [
    {{"question": "...", "type": "text", "answer": "...", "explanation": "..."}},
    {{"question": "...", "type": "choice", "options": ["...", "...", "..."], "answer": 0, "explanation": "..."}}
  ]
}}

Rules:
- No dashes of any kind anywhere (no hyphen used as punctuation, no em dash). Rewrite instead.
- If a question references code, wrap it in <code>...</code> HTML tags directly in the question string.
- The quiz "answer" for text questions must be short enough to reasonably type exactly (a word, a number, a short phrase) — never a full sentence.
- Keep every string beginner-friendly: no unexplained jargon."""


def generate(client: Groq, topic: dict, lesson_text: str) -> dict:
    prompt = build_prompt(topic, lesson_text)
    for attempt in range(5):
        try:
            response = groq_create(client, 
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.4,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except RateLimitError:
            wait = 20 * (attempt + 1)
            print(f"    rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Repeated rate-limit failures.")


def sync_to_week1(data: dict):
    WEEK1_SYLLABUS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Generate a specific topic ID, e.g. S-03")
    parser.add_argument("--all", action="store_true", help="Generate for all spine topics except S-01 (already done)")
    args = parser.parse_args()

    data = load_json(SYLLABUS_PATH)
    topics = data["spine"]["topics"]
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if args.topic:
        targets = [args.topic]
    elif args.all:
        targets = [t["id"] for t in topics if t["id"] not in DONE_IDS]
    else:
        print("Pass --topic S-XX or --all")
        return

    print(f"Generating quiz/try_it for {len(targets)} topic(s)...")
    for i, topic_id in enumerate(targets):
        topic = next(t for t in topics if t["id"] == topic_id)
        lesson_text = find_lesson_text(topic_id)
        print(f"  {topic_id}: {topic['topic']}...")
        try:
            result = generate(client, topic, lesson_text)
        except Exception as e:
            print(f"    FAILED {topic_id}: {e} — skipping, re-run to retry")
            if i < len(targets) - 1:
                time.sleep(35)
            continue

        topic["try_it"] = result.get("try_it")
        topic["quiz"] = result.get("quiz")

        SYLLABUS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        sync_to_week1(data)
        print(f"    -> saved")

        if i < len(targets) - 1:
            time.sleep(35)

    print("Done.")


if __name__ == "__main__":
    main()
