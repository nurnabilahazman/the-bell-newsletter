#!/usr/bin/env python3
"""
Renders every generated syllabus carousel JSON (content/syllabus_lessons/*_carousel.json)
into a PDF, reusing the existing linkedin_carousel_generator.py unchanged — it only
reads .tmp/linkedin_carousel_content.json, so this script feeds each lesson's carousel
through that same fixed input path one at a time and moves the result out before the
next overwrites it.

Reads:  content/syllabus_lessons/*_carousel.json
Saves:  content/syllabus_lessons/carousel_pdfs/{topic_id}.pdf
Usage:  python tools/syllabus_carousel_renderer.py
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LESSONS_DIR    = Path("content/syllabus_lessons")
PDF_DIR         = LESSONS_DIR / "carousel_pdfs"
TMP_INPUT       = Path(".tmp/linkedin_carousel_content.json")
TMP_OUTPUT      = Path(".tmp/linkedin_carousel.pdf")
RENDERER_SCRIPT = Path("tools/linkedin_carousel_generator.py")


def topic_number(topic_id: str) -> int:
    match = re.search(r"\d+", topic_id)
    return int(match.group()) if match else 1


def render_one(carousel_path: Path) -> bool:
    data = json.loads(carousel_path.read_text())
    topic_id = data.get("topic_id", carousel_path.stem)

    render_input = {
        "week":           topic_number(topic_id),
        "cover_title":    data.get("cover_title", ""),
        "cover_subtitle": data.get("cover_subtitle", ""),
        "slides":         data.get("slides", []),
        "last_slide":     data.get("last_slide", ""),
    }
    if not render_input["cover_title"] or not render_input["slides"]:
        print(f"  SKIP {topic_id} — missing cover_title or slides, needs manual review")
        return False

    TMP_INPUT.parent.mkdir(exist_ok=True)
    TMP_INPUT.write_text(json.dumps(render_input, indent=2))

    result = subprocess.run(
        [sys.executable, str(RENDERER_SCRIPT)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  FAILED {topic_id}: {result.stderr[-500:]}")
        return False

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    dest = PDF_DIR / f"{topic_id}.pdf"
    shutil.move(str(TMP_OUTPUT), str(dest))
    print(f"  -> {dest}")
    return True


def main():
    carousel_files = sorted(LESSONS_DIR.glob("*_carousel.json"))
    if not carousel_files:
        print("No carousel JSON files found in content/syllabus_lessons/.")
        return

    print(f"Rendering {len(carousel_files)} carousels...")
    ok, failed = 0, []
    for path in carousel_files:
        if render_one(path):
            ok += 1
        else:
            failed.append(path.stem)

    print(f"Done. {ok}/{len(carousel_files)} rendered.")
    if failed:
        print(f"Failed/skipped: {failed}")


if __name__ == "__main__":
    main()
