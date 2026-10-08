#!/usr/bin/env python3
"""
Copy lesson content from this repo (the source) to the website repo.

The lessons live in two places: here, where they're generated and checked,
and in the website repo, which is what Render serves. Nothing kept them in
step, so they could drift. This copies the source of truth across and reports
what changed. It refuses to copy anything that fails the hard checks.

Copies:
    content/syllabus_lessons/S-*.md      -> <site>/data/syllabus_lessons/
    content/syllabus_projects/S-*        -> <site>/data/syllabus_projects/
    config/coding_syllabus.json          -> <site>/data/coding_syllabus.json

Usage:
    python3 tools/sync_lessons_to_site.py            # check, then copy
    python3 tools/sync_lessons_to_site.py --dry-run  # show what would change
"""

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT.parent / "Week 1_Excel Formula Generator"

PAIRS = [
    (ROOT / "content/syllabus_lessons", SITE / "data/syllabus_lessons", "S-*.md"),
    (ROOT / "content/syllabus_projects", SITE / "data/syllabus_projects", "S-*"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not SITE.exists():
        sys.exit(f"Website repo not found at {SITE}")

    # Never ship a lesson that fails the hard checks.
    qa = subprocess.run([sys.executable, str(ROOT / "tools/lesson_qa.py"), "--all"],
                        capture_output=True, text=True)
    if qa.returncode != 0:
        print(qa.stdout[-3000:])
        sys.exit("Hard checks failed. Fix the lessons above before syncing.")

    changes = []
    for src_dir, dst_dir, pattern in PAIRS:
        dst_dir.mkdir(parents=True, exist_ok=True)
        src_names = {p.name for p in src_dir.glob(pattern)}
        for src in sorted(src_dir.glob(pattern)):
            dst = dst_dir / src.name
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                changes.append(f"update {dst.relative_to(SITE)}")
                if not args.dry_run:
                    shutil.copy2(src, dst)
        # A project file renamed at the source leaves a stale copy behind.
        for dst in sorted(dst_dir.glob(pattern)):
            if dst.name not in src_names and dst.name.split("_", 1)[0] in {n.split("_", 1)[0] for n in src_names}:
                changes.append(f"remove stale {dst.relative_to(SITE)}")
                if not args.dry_run:
                    dst.unlink()

    src_json, dst_json = ROOT / "config/coding_syllabus.json", SITE / "data/coding_syllabus.json"
    if not filecmp.cmp(src_json, dst_json, shallow=False):
        changes.append("update data/coding_syllabus.json")
        if not args.dry_run:
            shutil.copy2(src_json, dst_json)

    print("\n".join(changes) if changes else "Already in sync.")
    if args.dry_run and changes:
        print("(dry run, nothing copied)")


if __name__ == "__main__":
    main()
