#!/usr/bin/env python3
"""
Generates LinkedIn post text and carousel slide content for The Bell.
Reads:  config/curriculum.json, config/saas_progress.json,
        config/linkedin_voice_spec.md, config/linkedin_content_log.json
Saves:  .tmp/linkedin_post.md, .tmp/linkedin_carousel_content.json
Usage:  python tools/linkedin_post_generator.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

from groq import Groq
from groq_client import groq_create, MODEL as GROQ_MODEL
from dotenv import load_dotenv

load_dotenv()

CURRICULUM_PATH   = Path("config/curriculum.json")
SAAS_PATH         = Path("config/saas_progress.json")
VOICE_SPEC_PATH   = Path("config/linkedin_voice_spec.md")
CONTENT_LOG_PATH  = Path("config/linkedin_content_log.json")
POST_OUTPUT       = Path(".tmp/linkedin_post.md")
CAROUSEL_OUTPUT   = Path(".tmp/linkedin_carousel_content.json")

MODEL = GROQ_MODEL

# Rotate through these post types every week
POST_TYPES = [
    "building_from_zero",   # Honest weekly update — what happened, what broke, what worked
    "system_reveal",        # Show one specific part of the automation system
    "lesson_learned",       # One specific lesson with before/after
    "tool_tip",             # One Claude/AI technique with exact prompt to copy
]

POST_TYPE_INSTRUCTIONS = {
    "building_from_zero": """
POST TYPE: Building in public — but reader-first, not writer-first.

The hook must address the READER's situation, not Nabilah's. Open with something the reader recognises about themselves — a fear, a behaviour, an assumption they have.

Then use Nabilah's real story as PROOF that it's possible, not as the subject.

Required structure:
1. Hook: "You [specific thing most people do/feel/assume]." or "[Surprising specific fact]."
2. The real situation from Nabilah — as evidence, not narration
3. Exact action the reader can take today (prompt to type into Claude, step to take, etc.)
4. CTA: "Save this." or "Follow — [specific one-liner reason]."

The reader should think: "This is exactly my situation and now I know what to do."
Do NOT make the post about Nabilah's feelings or journey. Make it about what the reader can do.
""",
    "system_reveal": """
POST TYPE: Reveal a system — but give the reader a copy.

Do not narrate how Nabilah built it. Show the reader how THEY can have it.

Required structure:
1. Hook: "Nobody showed you this." / "Most people don't know you can [specific thing]." / "You don't need [assumption]."
2. Name the system in plain English — what it does in one sentence
3. The exact steps or the exact prompt the reader can use TODAY
4. One specific real number (RM cost, hours saved, time taken)
5. CTA: "Save this." — direct, no softening

Format: short paragraphs. If showing steps, use → not bullet points.
""",
    "lesson_learned": """
POST TYPE: Lesson — but told as a warning to the reader, not a confession by the writer.

The post should make the reader feel: "This is about to happen to me if I don't read this."

Required structure:
1. Hook: Name the mistake as if it's currently happening to the reader. "You're [doing the wrong thing]." or "This will [cost you something] if you ignore it."
2. What actually happened (Nabilah's story — 2-3 lines, no dramatisation)
3. The exact thing that would have prevented it
4. What the reader should do RIGHT NOW to avoid the same outcome
5. CTA: "Save this." — so they can refer back

The before/after must be specific enough that a beginner can see themselves in it.
""",
    "tool_tip": """
POST TYPE: Prompt/technique to copy — the "save this" post.

This is pure reader value. The reader should save it immediately.

Required structure:
1. Hook: "You're using Claude wrong." / "Stop [thing everyone does]. Do this instead." / "Most people use AI like [wrong thing]. There's a better way."
2. What the wrong approach is (1-2 lines — make them feel called out)
3. The exact prompt to type, formatted clearly on its own lines
4. What changes when you use this (specific — time saved, quality difference, specific result)
5. CTA: "Save this." — nothing else needed

The prompt must be in the post, formatted so it can be copied directly. This is non-negotiable.
""",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()


def get_post_type(log: dict) -> str:
    idx = log.get("post_type_index", 0) % len(POST_TYPES)
    return POST_TYPES[idx]


def build_context(log: dict) -> str:
    linkedin_week = log.get("current_week", 1)

    return f"""LINKEDIN WEEK: {linkedin_week}
DATE: {datetime.now().strftime('%B %d, %Y')}

WHO NABILAH IS:
- Malaysian woman, no CS degree, no technical background
- Building automated digital products using Claude and Python
- Started building a fully automated newsletter (The Bell) that runs every Monday with zero manual work
- The newsletter broke and was silently failing for 5 weeks — she found out and is fixing it in public
- This is LinkedIn week {linkedin_week} of documenting the real journey from zero

WHAT SHE HAS ACTUALLY BUILT SO FAR:
- A Python pipeline that scrapes news, generates a newsletter using AI, formats it as HTML and emails it automatically every Monday
- A children's activities section, productivity section, and language learning section — all auto-generated
- The pipeline runs on GitHub Actions (free server) — her MacBook does not need to be on
- Cost: roughly RM2.30/week in API costs
- It broke silently — no error email, no alert — for 5 weeks before she caught it
- She is now also adding a LinkedIn post + carousel that auto-generates alongside the newsletter

HONEST FACTS:
- She has no subscribers yet — just starting to post publicly
- She is not an expert — she is learning while building
- The value to the reader is watching someone with zero background actually do it

DO NOT mention YouTube, invoices, web scrapers, or anything not listed above.
DO NOT invent subscriber numbers, revenue, or achievements that are not listed above."""


def generate_content(client: Groq, voice_spec: str, context: str, post_type: str) -> str:
    instruction = POST_TYPE_INSTRUCTIONS.get(post_type, POST_TYPE_INSTRUCTIONS["building_from_zero"])

    prompt = f"""You are writing LinkedIn content for Nabilah — a Malaysian creator building automated systems with Claude. Zero technical background. Documenting the real journey from scratch, week by week.

VOICE AND WRITING RULES — follow every rule exactly:
{voice_spec}

CONTEXT:
{context}

{instruction}

APPROVED SAMPLE POST (study the rhythm, structure, and reader-pull — write like this):

---
I sleep. It works.

Every Monday at 1am, a newsletter goes out to my subscribers.

I don't write it. I don't format it. I don't send it.

I set it up once. Now it runs by itself.

This does not require a team, a technical background, or expensive software.

I described what I wanted to an AI in plain sentences. It built the system. I tested it. It worked.

One weekend to build. Less than a Grab order a week to run.

If you want to start — type this into Claude:

"I want [what you want to happen automatically]. No technical background. What is the simplest version? Ask me questions before you start."

That is the entry point.

Save this.
---

Notice: short punchy sentences. The writer's story creates FOMO. Removes the barrier the reader imagines. Gives an exact thing to copy. Ends "Save this." Write with this exact energy.

OUTPUT — use this exact format, no deviation:

POST_START
[LinkedIn post. 150-250 words. First sentence is the hook — no setup, no greeting, starts mid-thought or with a specific real detail. Paragraphs are 1-2 sentences. Blank line between every paragraph. Specific numbers where they exist. Honest where numbers are small or zero. Ends with one CTA: follow, save, or repost. No banned words. No banned structures from the voice spec.]
POST_END

CAROUSEL_START
COVER_TITLE: [A punchy 4-7 word statement that makes someone stop scrolling. Real and specific. Example: "My Newsletter Broke For 5 Weeks". No asterisks, no quotes.]
COVER_SUBTITLE: [One line, max 12 words. Completes the cover story.]

Each slide is ONE short statement (10-15 words). Frame slides from the READER's perspective — what THEY can do, learn, or know. Not what Nabilah did.

Wrap the single most powerful 2-3 word phrase in [[double brackets]] — it gets a yellow highlight box. CRITICAL: the [[highlighted]] phrase must be 2-3 words ONLY so it fits on one line. Never highlight a long phrase that would wrap.

SLIDE SENTENCE RULES — non-negotiable:
- No dashes of any kind (no hyphen, no em dash, no double dash). They sound robotic.
- Write like a real person talking. Simple, direct, conversational.
- No filler words like "literally", "actually", "basically".
- Each sentence must be complete and natural on its own.
- Every slide MUST have exactly one [[highlight]]. No exceptions.
- The [[highlight]] must be a real specific term: a tool name, a cost, a time, a number. Never vague phrases like "No Code", "AI Help", "my system".
- This system uses Python and Claude AI — do not call it "No Code". It is AI-assisted automation.

GOOD highlights: [[RM2.30]], [[GitHub Actions]], [[Claude AI]], [[one weekend]], [[52 times]]
BAD highlights: [[No Code]], [[AI Help]], [[my system]], [[this tool]]

BAD: "Your newsletter can run on [[GitHub Actions]] -- for free."
GOOD: "[[GitHub Actions]] runs your newsletter every Monday at no cost."

SLIDE_1_TEXT: [Reader-focused, 10-15 words, one [[specific highlight]]. Natural sentence, no dashes.]
SLIDE_2_TEXT: [Reader-focused, 10-15 words, one [[specific highlight]]. Natural sentence, no dashes.]
SLIDE_3_TEXT: [Reader-focused, 10-15 words, one [[specific highlight]]. Natural sentence, no dashes.]
SLIDE_4_TEXT: [Reader-focused, 10-15 words, one [[specific highlight]]. Natural sentence, no dashes.]
SLIDE_5_TEXT: [Reader-focused, 10-15 words, one [[specific highlight]]. Natural sentence, no dashes.]
LAST_SLIDE: [Follow CTA — max 12 words. Direct. "Follow — [specific reason they get value from following]."]
CAROUSEL_END

CRITICAL RULES:
- Post caption and carousel cover different content. Caption = hook + story. Carousel = system/steps/detail.
- Zero word repetition between the post opening line and carousel cover title.
- Carousel slides are scannable — short, specific, one idea each.
- Do not invent subscriber counts, revenue, or metrics that don't exist yet.
- Everything is beginner-accessible. If a technical term appears, explain it in the same sentence."""

    response = groq_create(client, 
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    return response.choices[0].message.content


def parse_output(raw: str) -> tuple[str, dict]:
    post = ""
    if "POST_START" in raw and "POST_END" in raw:
        post = raw.split("POST_START", 1)[1].split("POST_END", 1)[0].strip()

    carousel = {
        "cover_title":    "",
        "cover_subtitle": "",
        "slides":         [],
        "last_slide":     "",
    }

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
        for i in range(1, 9):
            text = extract(f"SLIDE_{i}_TEXT")
            if text:
                slides.append({"text": text})
        carousel["slides"] = slides

    return post, carousel


def update_log(log: dict, post_type: str) -> dict:
    week = log.get("current_week", 1)
    log["post_type_index"] = (log.get("post_type_index", 0) + 1) % len(POST_TYPES)
    log["current_week"]    = week + 1
    history = log.get("history", [])
    history.append({
        "week":      week,
        "post_type": post_type,
        "date":      datetime.now().strftime("%Y-%m-%d"),
    })
    log["history"] = history[-24:]
    return log


def main():
    voice_spec = load_text(VOICE_SPEC_PATH)
    log        = load_json(CONTENT_LOG_PATH)

    if not log:
        log = {"current_week": 1, "post_type_index": 0, "history": []}

    post_type     = get_post_type(log)
    linkedin_week = log.get("current_week", 1)
    context       = build_context(log)

    print(f"LinkedIn Week {linkedin_week} — Post type: {post_type}")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    print("Generating post and carousel content...")
    raw = generate_content(client, voice_spec, context, post_type)

    post, carousel = parse_output(raw)

    if not post:
        print("WARNING: Could not parse post from output. Check raw output below.")
        print(raw[:500])

    # Save post
    POST_OUTPUT.parent.mkdir(exist_ok=True)
    with open(POST_OUTPUT, "w") as f:
        f.write(f"# LinkedIn Post — Week {linkedin_week}\n")
        f.write(f"# Type: {post_type}\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(post)
        f.write("\n")
    print(f"  ✓ Post → {POST_OUTPUT} ({len(post.split())} words)")

    # Save carousel JSON
    carousel_data = {
        "week":           linkedin_week,
        "post_type":      post_type,
        "cover_title":    carousel["cover_title"],
        "cover_subtitle": carousel["cover_subtitle"],
        "slides":         carousel["slides"],
        "last_slide":     carousel["last_slide"],
    }
    with open(CAROUSEL_OUTPUT, "w") as f:
        json.dump(carousel_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Carousel content → {CAROUSEL_OUTPUT} ({len(carousel['slides'])} slides)")

    # Update log
    updated_log = update_log(log, post_type)
    with open(CONTENT_LOG_PATH, "w") as f:
        json.dump(updated_log, f, indent=2)
    print(f"  ✓ Content log updated — next type: {POST_TYPES[updated_log['post_type_index'] % len(POST_TYPES)]}")


if __name__ == "__main__":
    main()
