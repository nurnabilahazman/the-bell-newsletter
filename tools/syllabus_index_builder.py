#!/usr/bin/env python3
"""
Builds a single readable index of every generated syllabus lesson —
what's done, what's flagged for manual review, what's still pending.

Reads:  config/coding_syllabus.json, config/syllabus_progress.json,
        content/syllabus_lessons/*.md
Saves:  content/syllabus_lessons/INDEX.md
Usage:  python tools/syllabus_index_builder.py
"""

import json
from pathlib import Path

SYLLABUS_PATH = Path("config/coding_syllabus.json")
PROGRESS_PATH = Path("config/syllabus_progress.json")
LESSONS_DIR   = Path("content/syllabus_lessons")
INDEX_PATH    = LESSONS_DIR / "INDEX.md"


def main():
    syllabus = json.loads(SYLLABUS_PATH.read_text())
    progress = json.loads(PROGRESS_PATH.read_text()) if PROGRESS_PATH.exists() else {"completed": [], "history": []}

    spine_topics = syllabus.get("spine", {}).get("topics", [])
    completed = set(progress.get("completed", []))
    flagged_map = {h["topic_id"]: h.get("flagged_for_review", []) for h in progress.get("history", [])}

    lines = ["# The Bell — Zero to Expert: 2026 Spine Lesson Index", ""]
    lines.append(f"Generated {sum(1 for t in spine_topics if t['id'] in completed)}/{len(spine_topics)} spine lessons.")
    lines.append("")
    lines.append("| ID | Topic | Project | Lesson | Carousel | Flags |")
    lines.append("|---|---|---|---|---|---|")

    for t in spine_topics:
        tid = t["id"]
        project_title = t.get("project", {}).get("title", "")
        done = tid in completed
        md_files = list(LESSONS_DIR.glob(f"{tid}_*.md"))
        carousel_files = list(LESSONS_DIR.glob(f"{tid}_*_carousel.json"))
        pdf_file = LESSONS_DIR / "carousel_pdfs" / f"{tid}.pdf"

        lesson_link = f"[{md_files[0].name}]({md_files[0].name})" if md_files else "—"
        carousel_status = "PDF ready" if pdf_file.exists() else ("JSON only" if carousel_files else "—")
        flags = flagged_map.get(tid, [])
        flag_str = "; ".join(flags) if flags else ("clean" if done else "—")

        lines.append(f"| {tid} | {t['topic']} | {project_title} | {lesson_link} | {carousel_status} | {flag_str} |")

    flagged_ids = [tid for tid, f in flagged_map.items() if f]
    if flagged_ids:
        lines.append("")
        lines.append(f"## Needs manual review ({len(flagged_ids)})")
        for tid in flagged_ids:
            lines.append(f"- **{tid}**: {'; '.join(flagged_map[tid])}")

    pending = [t for t in spine_topics if t["id"] not in completed]
    if pending:
        lines.append("")
        lines.append(f"## Still pending ({len(pending)})")
        for t in pending:
            lines.append(f"- {t['id']}: {t['topic']}")

    INDEX_PATH.write_text("\n".join(lines))
    print(f"Index written to {INDEX_PATH}")


if __name__ == "__main__":
    main()
