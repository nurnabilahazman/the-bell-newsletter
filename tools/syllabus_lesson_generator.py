#!/usr/bin/env python3
"""
Generates a full beginner-accessible lesson + LinkedIn carousel/post for one
coding syllabus topic (config/coding_syllabus.json).

Reads:  config/coding_syllabus.json, config/linkedin_voice_spec.md,
        config/syllabus_progress.json
Saves:  content/syllabus_lessons/{id}_{slug}.md          (full lesson)
        content/syllabus_lessons/{id}_{slug}_carousel.json (LinkedIn carousel,
        same schema as .tmp/linkedin_carousel_content.json so the existing
        linkedin_carousel_generator.py can render it unchanged)
Usage:
    python tools/syllabus_lesson_generator.py                # next pending spine topic
    python tools/syllabus_lesson_generator.py --topic S-01    # a specific topic
    python tools/syllabus_lesson_generator.py --all           # every remaining spine topic
"""

import argparse
import json
import sys
import subprocess
import os
import re
import time
from pathlib import Path

from groq import Groq, RateLimitError
from groq_client import groq_create, MODEL as GROQ_MODEL
from dotenv import load_dotenv

load_dotenv()

SYLLABUS_PATH   = Path("config/coding_syllabus.json")
VOICE_SPEC_PATH = Path("config/linkedin_voice_spec.md")
PROGRESS_PATH   = Path("config/syllabus_progress.json")
OUTPUT_DIR      = Path("content/syllabus_lessons")

MODEL = GROQ_MODEL

ACCESSIBILITY_RULES = """
ACCESSIBILITY BAR — the single most important constraint, non-negotiable:

The reader has NEVER written a line of code. Zero background. The benchmark is:
they must finish this lesson having genuinely understood it, the way a total
beginner understands Ruben Hassid's writing despite having zero technical
background — not skimmed it, not nodded along without following, actually
understood it.

Rules:
- Every technical term gets a one-sentence plain-English definition the FIRST time it
  appears, in the same sentence or the one right after. Never assume a word like
  "function", "API", "variable", or "loop" is already known.
- A concrete, non-code, real-world analogy comes BEFORE any code is shown for a
  new idea. The analogy must be something a non-coder already understands.
- One idea per section. Do not stack two new concepts in the same paragraph.
- When code appears, walk through it line by line in plain English immediately
  after — never show code and assume it's self-explanatory.
- Short sentences. Short paragraphs. No jargon-on-jargon explanations.
- If you cannot explain a concept without another undefined technical term,
  stop and define that term first.
"""


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:50]


def get_spine_topics(syllabus: dict) -> list[dict]:
    return syllabus.get("spine", {}).get("topics", [])


def get_pending_topics(syllabus: dict, progress: dict) -> list[dict]:
    completed_ids = set(progress.get("completed", []))
    return [t for t in get_spine_topics(syllabus) if t["id"] not in completed_ids]


def build_topic_brief(topic: dict) -> str:
    project = topic.get("project", {})
    # The model can't know the course order, so tell it. Without this it
    # guesses "What's next" and has pointed back at a lesson already taught.
    spine = get_spine_topics(load_json(SYLLABUS_PATH))
    ids = [t["id"] for t in spine]
    idx = ids.index(topic["id"]) if topic["id"] in ids else -1
    prev_t = spine[idx - 1]["topic"] if idx > 0 else "none, this is the first lesson"
    next_t = spine[idx + 1]["topic"] if 0 <= idx < len(spine) - 1 else "none, this is the last lesson"
    taught = ", ".join(t["topic"] for t in spine[:max(idx, 0)]) or "nothing yet"
    return f"""TOPIC ID: {topic['id']}
PREVIOUS LESSON: {prev_t}
NEXT LESSON (the "What's next" section must tease exactly this): {next_t}
ALREADY TAUGHT (the reader knows these, build on them, don't re-teach): {taught}
TOPIC: {topic['topic']}
PLAIN ENGLISH SUMMARY (use as the seed idea, expand on it): {topic.get('plain_english_summary', '')}
STATUS: {topic.get('status', '')}
THE PROJECT FOR THIS LESSON: {project.get('title', '')}
PROJECT DESCRIPTION: {project.get('description', '')}"""


def generate_lesson(client: Groq, voice_spec: str, topic: dict) -> str:
    brief = build_topic_brief(topic)

    prompt = f"""You are writing an educational lesson for The Bell, a coding-education
series aimed at total beginners with zero programming background — finance
professionals, career-changers, anyone who has never coded.

{ACCESSIBILITY_RULES}

VOICE — write in this voice (direct, honest, no corporate language, short
sentences, no banned words/structures below):
{voice_spec}

TODAY'S TOPIC:
{brief}

OUTPUT — produce exactly these two sections, in this exact format, no deviation:

LESSON_START
# {{topic title}}

## The idea
[2-4 short paragraphs. Start with a real-world analogy a non-coder already
understands. Only after the analogy, introduce the technical term with its
one-sentence plain-English definition.]

## The project: {{project title}}
[1 short paragraph introducing what we're building and why, in plain English.]

## Building it
[The actual tiny project, as real runnable Python code in a fenced code block,
followed immediately by a line-by-line plain-English walkthrough of what each
part does. Keep the code itself short — under 20 lines.]

## Why this matters
[1-2 sentences. Must name something CONCRETE and specific — a real, live Bell
tool if the topic's linked project status is "built", or a specific moment in
the reader's own life where this exact idea shows up. Never a vague platitude
like "this is important for building digital products." If you cannot think
of something concrete, connect it to the very next lesson instead.]

## The mistake beginners make here
[1 short paragraph — one specific, common mistake at this exact concept, and
how to avoid it.]

## What's next
[1 sentence teasing the NEXT LESSON named in the brief above, in plain English,
no jargon. Never tease a topic from ALREADY TAUGHT.]
LESSON_END

CAROUSEL_START
COVER_TITLE: [4-7 words, punchy, makes someone stop scrolling. No asterisks, no quotes.]
COVER_SUBTITLE: [One line, max 12 words.]

Each slide is ONE short statement (10-15 words), reader-facing ("you" / "your"),
teaching one piece of this concept. Wrap the single most important 2-3 word
phrase per slide in [[double brackets]] — never a phrase that would wrap to a
second line. No dashes anywhere. No filler words.

SLIDE_1_TEXT: [10-15 words, one [[highlight]]]
SLIDE_2_TEXT: [10-15 words, one [[highlight]]]
SLIDE_3_TEXT: [10-15 words, one [[highlight]]]
SLIDE_4_TEXT: [10-15 words, one [[highlight]]]
SLIDE_5_TEXT: [10-15 words, one [[highlight]]]
LAST_SLIDE: [Follow/save CTA, max 12 words.]
CAROUSEL_END

CRITICAL:
- Everything must pass the accessibility bar above. If in doubt, explain more,
  not less.
- NO DASHES ANYWHERE. Not a hyphen used as punctuation, not an em dash, not a
  double dash. Rewrite the sentence instead of reaching for a dash. This
  applies to the lesson text too, not just the carousel.
- Do not invent numbers, subscriber counts, or achievements.
- The carousel teases the idea; the lesson is where the real teaching happens."""

    for attempt in range(5):
        try:
            response = groq_create(client, 
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.4,
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            wait = 20 * (attempt + 1)
            print(f"    rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Repeated rate-limit failures — giving up on this topic.")


def parse_output(raw: str) -> tuple[str, dict]:
    lesson = ""
    if "LESSON_START" in raw and "LESSON_END" in raw:
        lesson = raw.split("LESSON_START", 1)[1].split("LESSON_END", 1)[0].strip()

    carousel = {"cover_title": "", "cover_subtitle": "", "slides": [], "last_slide": ""}

    if "CAROUSEL_START" in raw and "CAROUSEL_END" in raw:
        section = raw.split("CAROUSEL_START", 1)[1].split("CAROUSEL_END", 1)[0]

        def extract(tag: str) -> str:
            for line in section.splitlines():
                stripped = line.strip()
                if stripped.startswith(f"{tag}:"):
                    return stripped.split(":", 1)[1].strip()
            return ""

        carousel["cover_title"]    = extract("COVER_TITLE")
        carousel["cover_subtitle"] = extract("COVER_SUBTITLE")
        carousel["last_slide"]     = extract("LAST_SLIDE")

        slides = []
        for i in range(1, 6):
            text = extract(f"SLIDE_{i}_TEXT")
            if text:
                slides.append({"text": text})
        carousel["slides"] = slides

    return lesson, carousel


BANNED_WORDS = [
    "leverage", "unlock", "game-changer", "seamlessly", "harness", "dive into",
    "excited to share", "thrilled to announce", "in today's world",
    "it's important to", "navigating the landscape", "the power of",
    "delve", "it's worth noting", "transformative", "groundbreaking",
    "as we navigate", "in today's fast-paced", "i'm humbled",
]

DASH_PATTERN = re.compile(r"\s[-—–]\s|—|–")


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and markdown bullet markers before
    dash-checking — a minus sign in real code (e.g. `total - deduction`) and
    a `- list item` bullet are not stylistic dash violations."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"^[ \t]*-\s", "", text, flags=re.MULTILINE)
    return text


def validate_lesson(text: str) -> list[str]:
    """Deterministic post-generation check — don't trust the model to police
    its own formatting rules. Returns a list of problems found, empty if clean."""
    problems = []

    prose_only = strip_code_blocks(text)
    dash_matches = DASH_PATTERN.findall(prose_only)
    if dash_matches:
        problems.append(f"dash found ({len(dash_matches)}x) — voice spec bans all dashes")

    lower = text.lower()
    for word in BANNED_WORDS:
        if word in lower:
            problems.append(f"banned word found: '{word}'")

    required_headers = ["## The idea", "## Building it", "## Why this matters",
                         "## The mistake beginners make here", "## What's next"]
    for header in required_headers:
        if header not in text:
            problems.append(f"missing required section: {header}")

    return problems


def process_topic(client: Groq, voice_spec: str, topic: dict) -> tuple[Path, list[str]]:
    print(f"  Generating {topic['id']}: {topic['topic']}...")

    problems: list[str] = []
    lesson, carousel, raw = "", {}, ""
    for attempt in range(2):
        raw = generate_lesson(client, voice_spec, topic)
        lesson, carousel = parse_output(raw)
        problems = validate_lesson(lesson) if lesson else ["could not parse LESSON_START/LESSON_END"]
        if not problems:
            break
        if attempt == 0:
            print(f"    retrying — validation found: {problems}")

    if problems:
        print(f"    FLAGGED for manual review: {problems}")

    slug = slugify(topic["topic"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lesson_path = OUTPUT_DIR / f"{topic['id']}_{slug}.md"
    with open(lesson_path, "w") as f:
        f.write(lesson if lesson else raw)

    carousel_data = {
        "topic_id":       topic["id"],
        "topic":          topic["topic"],
        "cover_title":    carousel["cover_title"],
        "cover_subtitle": carousel["cover_subtitle"],
        "slides":         carousel["slides"],
        "last_slide":     carousel["last_slide"],
    }
    carousel_path = OUTPUT_DIR / f"{topic['id']}_{slug}_carousel.json"
    with open(carousel_path, "w") as f:
        json.dump(carousel_data, f, indent=2, ensure_ascii=False)

    print(f"    -> {lesson_path.name}, {carousel_path.name}")

    # Hard checks straight away, so a broken lesson is flagged at birth.
    # See workflows/lesson_quality_pipeline.md for the full pipeline.
    qa = subprocess.run([sys.executable, "tools/lesson_qa.py", "--topic", topic["id"]],
                        capture_output=True, text=True)
    print("    " + qa.stdout.strip().replace("\n", "\n    "))
    if qa.returncode != 0:
        problems.append("lesson_qa hard checks failed, see above")
    return lesson_path, problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Generate a specific topic ID, e.g. S-01")
    parser.add_argument("--all", action="store_true", help="Generate every remaining pending spine topic")
    args = parser.parse_args()

    syllabus = load_json(SYLLABUS_PATH)
    voice_spec = load_text(VOICE_SPEC_PATH)
    progress = load_json(PROGRESS_PATH) or {"current_group": "spine", "current_index": 0, "completed": [], "history": []}

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if args.topic:
        topics = [t for t in get_spine_topics(syllabus) if t["id"] == args.topic]
        if not topics:
            print(f"Topic {args.topic} not found in spine.")
            return
        targets = topics
    elif args.all:
        targets = get_pending_topics(syllabus, progress)
    else:
        pending = get_pending_topics(syllabus, progress)
        targets = pending[:1]

    if not targets:
        print("Nothing pending — all spine topics already generated.")
        return

    print(f"Generating {len(targets)} lesson(s)...")
    flagged, failed = [], []
    for i, topic in enumerate(targets):
        try:
            _, problems = process_topic(client, voice_spec, topic)
        except Exception as e:
            print(f"    FAILED {topic['id']}: {e} — skipping, will retry on next run")
            failed.append(topic["id"])
            if i < len(targets) - 1:
                time.sleep(35)
            continue

        if topic["id"] not in progress["completed"]:
            progress["completed"].append(topic["id"])
        progress["history"].append({
            "topic_id": topic["id"],
            "topic": topic["topic"],
            "flagged_for_review": problems,
        })
        if problems:
            flagged.append(topic["id"])

        # Save after EVERY topic, not just at the end — a crash mid-batch
        # (rate limit, network blip) must not lose track of completed work.
        progress["current_index"] = len(progress["completed"])
        with open(PROGRESS_PATH, "w") as f:
            json.dump(progress, f, indent=2)

        if i < len(targets) - 1:
            time.sleep(35)  # ~5500 tokens/call vs 12000 TPM limit needs >27s gap

    print(f"Done. {len(progress['completed'])}/{len(get_spine_topics(syllabus))} spine topics generated.")
    if flagged:
        print(f"Flagged for manual review after retry: {flagged}")
    if failed:
        print(f"Failed (rate limit exhausted) — re-run --all to retry: {failed}")


if __name__ == "__main__":
    main()
