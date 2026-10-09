#!/usr/bin/env python3
"""
Generates the interactive HTML/JS block for a syllabus project — the "Open
tool" experience, not the lesson. Reuses the exact CSS classes already
defined in the Week 1 app's syllabus_project.html (label, input, .btn,
.result, .terminal, .term-line, .card-preview, .live-stats) so no new
styling is needed — only vanilla JS, no external libraries/CDNs.

Reads:  config/coding_syllabus.json
Saves:  {WEEK1_APP}/templates/syllabus_tools/{topic_id}.html
Usage:  python tools/syllabus_tool_generator.py --topic S-06
        python tools/syllabus_tool_generator.py --all
"""

import argparse
import json
import os
import re
import time
from pathlib import Path

from groq import Groq, RateLimitError
from groq_client import groq_create, MODEL as GROQ_MODEL
from dotenv import load_dotenv

load_dotenv()

SYLLABUS_PATH = Path("config/coding_syllabus.json")
WEEK1_APP = Path("../Week 1_Excel Formula Generator")
OUTPUT_DIR = WEEK1_APP / "templates" / "syllabus_tools"

MODEL = GROQ_MODEL

# Topics that redirect instead of needing a new build (handled in combined_app.py)
SKIP_IDS = {"S-11", "S-14", "S-22", "S-23", "S-24"}

FEW_SHOT = '''
Reuse these EXACT CSS classes already defined on the page — do not invent new class names, do not add a <style> block:
- label, input[type=text], input[type=number], textarea — form fields
- .btn — the button (dark pill, use onclick="")
- .result / .result.show — hidden-by-default result box, toggle the "show" class via JS
- .result-line, .result-line b — a label/value row inside .result
- .card-preview, .cname, .ctitle, .ccompany — a centered preview card
- .terminal, .term-line, .term-prompt, .term-output — dark terminal-style output block
- .live-stats, .live-warning — small stat row + warning text

EXAMPLE (a calculator-style tool, S-04 Freelance Day-Rate Calculator):
<label>Hourly rate (RM)</label>
<input type="number" id="s04rate" value="50">
<label>Hours worked</label>
<input type="number" id="s04hours" value="8">
<button class="btn" onclick="s04calc()">Calculate &rarr;</button>
<div class="result" id="s04result">
  <div class="result-line"><span>Total</span><b id="s04total"></b></div>
</div>
<script>
function s04calc() {
  const rate = parseFloat(document.getElementById('s04rate').value) || 0;
  const hours = parseFloat(document.getElementById('s04hours').value) || 0;
  document.getElementById('s04total').textContent = 'RM ' + (rate * hours).toFixed(2);
  document.getElementById('s04result').classList.add('show');
}
</script>

EXAMPLE (a step-through reveal tool, S-01 style):
<div class="terminal">
  <div class="term-line" style="color:#82aaff;">print("hello")</div>
</div>
<button class="btn" id="s01btn" onclick="s01reveal()">Reveal &rarr;</button>
<div class="terminal" id="s01out" style="display:none; margin-top:14px;"></div>
<script>
function s01reveal() {
  document.getElementById('s01out').style.display = 'block';
  document.getElementById('s01out').innerHTML = '<div class="term-output">hello</div>';
  document.getElementById('s01btn').disabled = true;
}
</script>
'''


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def get_topic(data: dict, topic_id: str) -> dict:
    for t in data.get("spine", {}).get("topics", []):
        if t["id"] == topic_id:
            return t
    raise ValueError(f"{topic_id} not found in spine")


def build_prompt(topic: dict) -> str:
    project = topic.get("project", {})
    unique_id = topic["id"].lower().replace("-", "")

    return f"""Generate a self-contained interactive HTML+JS block for a coding-education mini-tool. All element IDs and function names MUST be prefixed with "{unique_id}" (e.g. {unique_id}Btn, {unique_id}calc) so multiple tools can coexist on the same site without ID collisions.

TOPIC: {topic['topic']}
CONCEPT: {topic.get('plain_english_summary', '')}
PROJECT TO BUILD: {project.get('title', '')}
DESCRIPTION: {project.get('description', '')}

{FEW_SHOT}

RULES:
- Vanilla JS only, no external libraries, no CDN links, no fetch/API calls.
- No <style> block and no inline <script src>. Inline <script> at the end is fine.
- Every interactive element needs a real working onclick or oninput handler — no dead buttons.
- If the tool is naturally a "predict then reveal" exercise (matches a step-through/terminal concept), use the terminal pattern with a separate reveal step — never show the answer at the same time as the question.
- If the tool needs to remember data between page loads (e.g. an expense log), use localStorage.
- Keep it genuinely usable — a real working version of "{project.get('title','')}", not a mockup.
- Output ONLY the HTML/JS block. No markdown fences, no explanation, no <html>/<body> wrapper tags."""


def generate_tool(client: Groq, topic: dict) -> str:
    prompt = build_prompt(topic)
    for attempt in range(5):
        try:
            response = groq_create(client, 
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3,
            )
            content = response.choices[0].message.content.strip()
            content = re.sub(r"^```(?:html)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
            return content
        except RateLimitError:
            wait = 20 * (attempt + 1)
            print(f"    rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Repeated rate-limit failures.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Generate a specific topic ID, e.g. S-06")
    parser.add_argument("--all", action="store_true", help="Generate every remaining spine tool (S-06 to S-25, minus reuse/link ones)")
    args = parser.parse_args()

    data = load_json(SYLLABUS_PATH)
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if args.topic:
        targets = [args.topic]
    elif args.all:
        targets = [f"S-{i:02d}" for i in range(6, 26) if f"S-{i:02d}" not in SKIP_IDS]
    else:
        print("Pass --topic S-XX or --all")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(targets)} tool(s)...")
    for i, topic_id in enumerate(targets):
        if topic_id in SKIP_IDS:
            print(f"  {topic_id}: skipped (redirect, no build needed)")
            continue
        topic = get_topic(data, topic_id)
        print(f"  Generating {topic_id}: {topic['topic']} -> {topic.get('project', {}).get('title', '')}...")
        try:
            html = generate_tool(client, topic)
        except Exception as e:
            print(f"    FAILED {topic_id}: {e} — skipping, re-run to retry")
            if i < len(targets) - 1:
                time.sleep(35)
            continue

        out_path = OUTPUT_DIR / f"{topic_id}.html"
        out_path.write_text(html)
        print(f"    -> {out_path}")

        if i < len(targets) - 1:
            time.sleep(35)  # stay under Groq's rate limit

    print("Done.")


if __name__ == "__main__":
    main()
