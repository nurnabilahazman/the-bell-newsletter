#!/usr/bin/env python3
"""
Assigns a real posting date to every syllabus topic (spine + all 4 tracks),
weekly cadence, in order: Spine (2026) -> Track A -> Track B (2027) ->
Track C -> Track D (2028).

Reads/writes: config/coding_syllabus.json (adds "scheduled_date" to every topic)
Usage:  python tools/syllabus_scheduler.py [--start YYYY-MM-DD]
"""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

SYLLABUS_PATH = Path("config/coding_syllabus.json")


def next_monday(from_date: date) -> date:
    days_ahead = (7 - from_date.weekday()) % 7
    days_ahead = days_ahead if days_ahead != 0 else 7
    return from_date + timedelta(days=days_ahead)


def assign_dates(syllabus: dict, start: date) -> dict:
    current = start
    spine_topics = syllabus.get("spine", {}).get("topics", [])
    for t in spine_topics:
        t["scheduled_date"] = current.isoformat()
        current += timedelta(weeks=1)

    tracks = {t["id"]: t for t in syllabus.get("tracks", [])}
    order = ["A", "B", "C", "D"]
    for track_id in order:
        track = tracks.get(track_id)
        if not track:
            continue
        for t in track.get("topics", []):
            if t.get("status") == "external_reference":
                t["scheduled_date"] = None
                continue
            t["scheduled_date"] = current.isoformat()
            current += timedelta(weeks=1)

    return syllabus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="YYYY-MM-DD, defaults to next Monday")
    args = parser.parse_args()

    start = date.fromisoformat(args.start) if args.start else next_monday(date.today())

    syllabus = json.loads(SYLLABUS_PATH.read_text())
    syllabus = assign_dates(syllabus, start)
    SYLLABUS_PATH.write_text(json.dumps(syllabus, indent=2, ensure_ascii=False))

    spine = syllabus["spine"]["topics"]
    print(f"Spine: {spine[0]['scheduled_date']} -> {spine[-1]['scheduled_date']} ({len(spine)} topics)")
    for track in syllabus.get("tracks", []):
        dated = [t for t in track["topics"] if t.get("scheduled_date")]
        if dated:
            print(f"Track {track['id']} ({track['name']}): {dated[0]['scheduled_date']} -> {dated[-1]['scheduled_date']} ({len(dated)} topics)")


if __name__ == "__main__":
    main()
