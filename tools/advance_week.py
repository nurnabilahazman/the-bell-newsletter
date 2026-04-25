#!/usr/bin/env python3
"""
Advances current_week by 1 in curriculum.json and saas_progress.json.
Called automatically after a successful newsletter send.
Usage: python tools/advance_week.py
"""

import json
from pathlib import Path

CURRICULUM_PATH = Path("config/curriculum.json")
SAAS_PATH       = Path("config/saas_progress.json")


def advance(path: Path, max_weeks: int, label: str):
    if not path.exists():
        print(f"SKIP: {path} not found")
        return
    with open(path) as f:
        data = json.load(f)
    current = data.get("current_week", 1)
    if current >= max_weeks:
        print(f"{label}: already at week {current}/{max_weeks} — not advancing")
        return
    data["current_week"] = current + 1
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"{label}: week {current} → {current + 1}")


def main():
    curriculum = json.loads(CURRICULUM_PATH.read_text()) if CURRICULUM_PATH.exists() else {}
    saas       = json.loads(SAAS_PATH.read_text())       if SAAS_PATH.exists()       else {}

    max_curriculum = len(curriculum.get("projects", []))
    max_saas       = len(saas.get("milestones", []))

    advance(CURRICULUM_PATH, max_curriculum, "Curriculum")
    advance(SAAS_PATH,       max_saas,       "SaaS")


if __name__ == "__main__":
    main()
