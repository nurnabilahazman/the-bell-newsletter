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
from dotenv import load_dotenv

load_dotenv()

CURRICULUM_PATH   = Path("config/curriculum.json")
SAAS_PATH         = Path("config/saas_progress.json")
VOICE_SPEC_PATH   = Path("config/linkedin_voice_spec.md")
CONTENT_LOG_PATH  = Path("config/linkedin_content_log.json")
POST_OUTPUT       = Path(".tmp/linkedin_post.md")
CAROUSEL_OUTPUT   = Path(".tmp/linkedin_carousel_content.json")

MODEL = "llama-3.3-70b-versatile"

# Rotate through these post types every week
POST_TYPES = [
    "building_from_zero",   # Honest weekly update — what happened, what broke, what worked
    "system_reveal",        # Show one specific part of the automation system
    "lesson_learned",       # One specific lesson with before/after
    "tool_tip",             # One Claude/AI technique with exact prompt to copy
]

POST_TYPE_INSTRUCTIONS = {
    "building_from_zero": """
POST TYPE: Weekly building-in-public update.
The writer is documenting the real journey from zero — no technical background, just starting.
Hook must capture the honest reality of this week: what she tried, what broke, what surprised her.
The reader (someone who wants to start but hasn't) should feel: "this person is just like me AND they're actually doing it."
Specific is everything — a real thing that happened this week, not a general reflection.
Do NOT fake success metrics. If nothing launched, say so. That honesty is the value.
""",
    "system_reveal": """
POST TYPE: Reveal one specific part of the automation system.
Explain what it does in plain English — no jargon.
Specific numbers create credibility: RM cost, hours to build, number of steps.
The reader should understand how one real piece of automation works and feel like they could build it.
The carousel shows the step-by-step breakdown. The post tells the story of why it matters.
""",
    "lesson_learned": """
POST TYPE: One specific lesson from building.
Structure: what I assumed → what actually happened → what I now know.
Must be specific enough that a beginner can apply it to their own project today.
Not motivational — practical and earned from real experience.
The "before" state should match exactly where the target reader is right now.
""",
    "tool_tip": """
POST TYPE: One specific Claude/AI technique with the exact prompt.
The reader should be able to copy the prompt and use it today.
Open with why most people do this wrong or don't know about it.
End with the exact words to type — formatted clearly so it stands out.
This is the "save this" post — make it worth saving.
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


def build_context(curriculum: dict, saas: dict, log: dict) -> str:
    week_num  = curriculum.get("current_week", 1)
    projects  = curriculum.get("projects", [])
    project   = next((p for p in projects if p["week"] == week_num), {})

    saas_week      = saas.get("current_week", 1)
    saas_miles     = saas.get("milestones", [])
    saas_current   = next((m for m in saas_miles if m["week"] == saas_week), {})
    linkedin_week  = log.get("current_week", 1)

    return f"""LINKEDIN WEEK: {linkedin_week}
NEWSLETTER WEEK: {week_num}
SECTION 1 PROJECT THIS WEEK: {project.get('title', 'Building automation tools')}
SKILL BEING LEARNED: {project.get('skill', 'Python + Claude')}
SAAS TASK THIS WEEK: {saas_current.get('task', 'Building the core system')}
DATE: {datetime.now().strftime('%B %d, %Y')}
CREATOR: Nabilah — Malaysian, no technical background, building automation with Claude from scratch.
NEWSLETTER STATUS: Automated newsletter system (currently being fixed after 5-week outage).
HONEST SUBSCRIBER COUNT: Small — just starting. Do not invent large numbers."""


def generate_content(client: Groq, voice_spec: str, context: str, post_type: str) -> str:
    instruction = POST_TYPE_INSTRUCTIONS.get(post_type, POST_TYPE_INSTRUCTIONS["building_from_zero"])

    prompt = f"""You are writing LinkedIn content for Nabilah — a Malaysian creator building automated systems with Claude. Zero technical background. Documenting the real journey from scratch, week by week.

VOICE AND WRITING RULES — follow every rule exactly:
{voice_spec}

CONTEXT:
{context}

{instruction}

OUTPUT — use this exact format, no deviation:

POST_START
[LinkedIn post. 150-250 words. First sentence is the hook — no setup, no greeting, starts mid-thought or with a specific real detail. Paragraphs are 1-2 sentences. Blank line between every paragraph. Specific numbers where they exist. Honest where numbers are small or zero. Ends with one CTA: follow, save, or repost. No banned words. No banned structures from the voice spec.]
POST_END

CAROUSEL_START
COVER_TITLE: [Bold claim or specific thing — max 8 words. Different from the post hook.]
COVER_SUBTITLE: [What the reader gets from this carousel — max 12 words.]
SLIDE_1_TITLE: [Title]
SLIDE_1_BODY: [Max 45 words. Use → for steps. Plain English. Specific.]
SLIDE_2_TITLE: [Title]
SLIDE_2_BODY: [Max 45 words.]
SLIDE_3_TITLE: [Title]
SLIDE_3_BODY: [Max 45 words.]
SLIDE_4_TITLE: [Title]
SLIDE_4_BODY: [Max 45 words.]
SLIDE_5_TITLE: [Title]
SLIDE_5_BODY: [Max 45 words.]
LAST_SLIDE: [CTA — max 20 words. Simple. Direct. E.g. "Follow for weekly posts on building with AI from scratch."]
CAROUSEL_END

CRITICAL RULES:
- Post caption and carousel cover different content. Caption = hook + story. Carousel = system/steps/detail.
- Zero word repetition between the post opening line and carousel cover title.
- Carousel slides are scannable — short, specific, one idea each.
- Do not invent subscriber counts, revenue, or metrics that don't exist yet.
- Everything is beginner-accessible. If a technical term appears, explain it in the same sentence."""

    response = client.chat.completions.create(
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
            title = extract(f"SLIDE_{i}_TITLE")
            body  = extract(f"SLIDE_{i}_BODY")
            if title:
                slides.append({"title": title, "body": body})
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
    curriculum = load_json(CURRICULUM_PATH)
    saas       = load_json(SAAS_PATH)
    voice_spec = load_text(VOICE_SPEC_PATH)
    log        = load_json(CONTENT_LOG_PATH)

    if not log:
        log = {"current_week": 1, "post_type_index": 0, "history": []}

    post_type     = get_post_type(log)
    linkedin_week = log.get("current_week", 1)
    context       = build_context(curriculum, saas, log)

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
