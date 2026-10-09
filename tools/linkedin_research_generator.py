#!/usr/bin/env python3
"""
Generate a LinkedIn research brief (HTML) for the upcoming carousel week.

Reads:
  config/linkedin_content_log.json     → which week to generate for
  config/linkedin_topic_schedule.json  → carousel topics and slides
  .tmp/linkedin_raw_research.json      → scraped Reddit + RSS data

Calls: Groq API (model set in tools/groq_client.py) to curate insights and generate hook variations

Saves: .tmp/linkedin_research_brief.html

Usage:
  python tools/linkedin_research_generator.py          # uses current_week from log
  python tools/linkedin_research_generator.py --week 3 # specific week
"""

import json
import os
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

from groq import Groq
from groq_client import groq_create, MODEL as GROQ_MODEL
from dotenv import load_dotenv

load_dotenv()

CONTENT_LOG = Path("config/linkedin_content_log.json")
TOPIC_SCHEDULE = Path("config/linkedin_topic_schedule.json")
RAW_RESEARCH = Path(".tmp/linkedin_raw_research.json")
OUTPUT_PATH = Path(".tmp/linkedin_research_brief.html")

CREAM = "#F5F0E8"
NAVY = "#1A1A2E"
GOLD = "#C9A84C"
MUTED = "#777777"
NAVY_LIGHT = "#2a2a4a"

# ── Research playbooks per category ────────────────────────────────────────────

PLAYBOOKS = {
    "BEFORE_AFTER": {
        "label": "Before / After",
        "what_to_find": [
            "A stat showing how much time finance/accounting professionals waste on this task industry-wide",
            "A McKinsey, Microsoft Work Trend Index, or ACCA report on the broader problem (use the RSS stat bank below)",
            "A Reddit post where someone complains about doing exactly this task manually",
            "A specific result number for the 'after' state: hours saved, minutes, percentage reduction",
        ],
        "s1_formula": "The best S1 for Before/After is a surprising industry stat that makes the reader think 'wait, that's me.' Use a specific percentage or time figure with a source name. Avoid vague openers like 'Many people struggle with...'",
        "s4_guidance": "S4 must have a concrete result: '42 hours → 2 minutes', '3 weeks → 5 minutes', 'zero errors since'. Vague claims like 'much faster' do not land.",
        "s5_guidance": "S5 gives ONE specific thing to do TODAY. Not 'try automation' — 'Open Power Automate. It is already in your Microsoft account.' The more specific, the better.",
        "checklist": [
            "S1 stat is verifiable and has a source name (McKinsey, Microsoft, etc.)",
            "S4 has a specific time/number for BOTH the before AND the after",
            "S5 tells reader exactly what to open/click/type — not abstract advice",
            "The 'before' state in S2 is something the audience has personally experienced",
            "The tool in S3 is named specifically — not 'AI' or 'automation'",
        ],
    },
    "TOOL_SPOTLIGHTS": {
        "label": "Tool Spotlight",
        "what_to_find": [
            "A recent adoption stat for this tool or its category (check RSS feeds below)",
            "A Reddit post showing real-world use or misuse of this tool in professional contexts",
            "A specific use case with a measurable result (not 'saves time' — 'cuts research from 1 hour to 5 minutes')",
            "What makes this tool different from or better than the obvious alternative",
        ],
        "s1_formula": "For Tool Spotlights, S1 reveals a surprising gap: the tool is underused ('64% with Copilot access never open it'), or it does something people don't know about, or it saves dramatically more time than expected. Avoid 'X is a great tool for...'",
        "s4_guidance": "S4 must show a real outcome from a real task. Name the task, name the result. 'Three minutes: full slide deck. Layout, content, structure.' Not 'I saved a lot of time.'",
        "s5_guidance": "S5 must give one immediate action: 'Open [tool] now. Type [specific first step].' Make it completable in 5 minutes. Link to the free tier or explain it is already installed.",
        "checklist": [
            "S1 reveals something surprising or counterintuitive about this tool",
            "S3 explains exactly HOW to use it — not just that it exists",
            "S4 has a specific task + specific result (not 'it saves time')",
            "S5 gives the reader exactly where to start (URL, menu item, shortcut)",
            "Work tools (Copilot, Power Automate) are framed as already installed and free",
        ],
    },
    "EXACT_PROMPTS": {
        "label": "Exact Prompts",
        "what_to_find": [
            "What people are asking Claude/ChatGPT in your community right now — those questions ARE prompts to share",
            "Pain points around the task this prompt solves (Reddit is gold for this)",
            "A stat about how much time the task takes without AI (gives S1 its hook)",
            "What bad/vague prompts look like vs specific ones (useful for S3 contrast)",
        ],
        "s1_formula": "For Prompt carousels, S1 frames the problem the prompt solves. Either a time stat ('Writing management summaries used to take most of a morning') or a relatable frustration ('The blank page is the most expensive part of any writing task'). Do NOT start with the prompt itself.",
        "s4_guidance": "S4 should show the specific result when the prompt is used: time saved, quality of output. Or it can show the actual prompt in its full form if not shown in S3.",
        "s5_guidance": "S5 should be a direct CTA that includes the actual action: 'Try this on the next report you receive' or 'Save this. Use it every Monday.' Tell them to actually USE it, not just save it.",
        "checklist": [
            "The actual prompt is shown in slides (verbatim, not paraphrased)",
            "S1 makes the reader feel the pain before the fix is revealed",
            "The prompt includes: role, context, output format, and constraints",
            "S5 tells the reader to try it — not just save it",
            "The result claim in S4 is specific ('3 minutes', '30 words', 'ready to send')",
        ],
    },
    "SYSTEM_BUILDS": {
        "label": "System Build",
        "what_to_find": [
            "Reddit posts about people struggling to build similar automations (validates the problem)",
            "Stats on how much time the equivalent manual task takes industry-wide",
            "The specific tools in the stack and why each was chosen over alternatives",
            "What breaks in this type of system and how to build a failure alert",
        ],
        "s1_formula": "For System Builds, S1 hooks with the running system, not the building of it: 'Every Monday at 1am a newsletter sends. I am asleep.' or 'One task. Manual: 4 hours. Automated: happens while I sleep.' The contrast lands harder than describing the build process.",
        "s4_guidance": "S4 should show the system in its 'final running state': what it does without intervention, how often it fires, how long it has been running without issues.",
        "s5_guidance": "S5 should give the reusable framework: Trigger → Script → Output. This is the mental model readers can apply to their own context. Give it to them explicitly.",
        "checklist": [
            "S1 opens with the system already running — not with 'I decided to build...'",
            "Each tool in the stack is named specifically (not 'an AI' — which AI?)",
            "S4 shows the system running on its own (no manual step needed after setup)",
            "S5 gives a principle the reader can apply to their own repeating task",
            "Build time and running time are mentioned ('built once, runs every week')",
        ],
    },
    "HONEST_TAKES": {
        "label": "Honest Take",
        "what_to_find": [
            "Conflicting opinions about AI in finance/accounting communities — find both sides",
            "Studies that contradict popular assumptions about AI productivity",
            "Real examples of AI failing in professional contexts (Reddit is rich for this)",
            "The perspective most LinkedIn creators in this space are NOT sharing",
        ],
        "s1_formula": "For Honest Takes, S1 states a specific countable claim: 'Three things AI consistently gets wrong.' or 'AI made one specific skill weaker.' Avoid generic opinion openers. The more specific the claim, the stronger the scroll-stop.",
        "s4_guidance": "S4 should be the most personal, specific slide — a real example from your own work with a real number or outcome. This is what makes the take credible rather than theoretical.",
        "s5_guidance": "S5 must land with a clear decision principle: 'Use AI for execution. Keep the judgment. The two are not interchangeable.' No hedging. Be direct. The reader should leave with a heuristic they can act on.",
        "checklist": [
            "S1 makes a specific, countable claim — not a vague opinion",
            "The 'honest' angle is something most creators in this space wouldn't say publicly",
            "S4 is personal and specific — your real experience, not industry claims",
            "S5 gives a clear heuristic the reader can apply immediately",
            "No hedging language ('it depends', 'results may vary') — take a position",
        ],
    },
    "BEGINNER_GUIDES": {
        "label": "Beginner Guide",
        "what_to_find": [
            "The most common 'where do I start?' questions in r/ChatGPT, r/nocode, r/learnprogramming",
            "What beginners wish someone had told them when they first started",
            "The smallest first step that actually works (not 'learn Python first')",
            "Common beginner mistakes that cause people to give up early",
        ],
        "s1_formula": "For Beginner Guides, S1 is welcoming and concrete: 'First time opening Claude. Exact starting point.' or 'Three tools. Not 30. These cover almost everything.' The tone is: I will make this easy for you, right now, with zero prerequisites.",
        "s4_guidance": "S4 shows what the result looks like after following the guide. It should be achievable in under 30 minutes. Name the specific outcome: 'First automation done. Two tools connected. Runs every time the trigger fires.'",
        "s5_guidance": "S5 sets the smallest possible bar: 'Do this once today. Once tomorrow. The habit builds faster than expected.' Never overwhelm the beginner. One action per slide, one slide at a time.",
        "checklist": [
            "S1 removes any anxiety or barrier to getting started",
            "Each step is ONE thing, not three things described as one",
            "The tools mentioned have free tiers or are already installed",
            "S5 is completable in under 5 minutes by someone brand new",
            "No jargon without an immediate plain-English explanation on the same slide",
        ],
    },
}

RESEARCH_HINTS = {
    "BEFORE_AFTER": "Watch for: posts complaining about manual work, productivity stats, time-tracking data. Key sources: McKinsey, Microsoft Work Trend Index, ACCA reports.",
    "TOOL_SPOTLIGHTS": "Watch for: tool update announcements, adoption surveys, Reddit threads from people discovering the tool. Key sources: official tool blogs, ProductHunt, r/ChatGPT.",
    "EXACT_PROMPTS": "Watch for: questions people ask AI (those questions ARE your prompt topics). Key sources: r/ChatGPT top posts, r/PromptEngineering weekly threads.",
    "SYSTEM_BUILDS": "Watch for: 'I built X' posts, automation failure stories. Key sources: r/automation, r/n8n, GitHub trending Python repos.",
    "HONEST_TAKES": "Watch for: AI criticism, failure case studies, contrarian perspectives. Key sources: Hacker News, r/Futurology, academic preprints on AI limitations.",
    "BEGINNER_GUIDES": "Watch for: 'where do I start?' questions, beginner frustration threads. Key sources: r/ChatGPT sorted by new, r/nocode weekly help threads.",
}


# ── AI insight generation ──────────────────────────────────────────────────────

def generate_insights(carousel: dict, raw_research: dict) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    slides_text = "\n".join(f"S{i+1}: {s}" for i, s in enumerate(carousel["slides"]))

    reddit_posts = raw_research.get("reddit", {}).get("posts", [])
    top_posts = sorted(reddit_posts, key=lambda x: x.get("score", 0), reverse=True)[:25]
    reddit_text = "\n".join(
        f"[r/{p['subreddit']}] {p['title']} ({p['score']} upvotes)"
        + (f"\n  → {p['preview'][:200]}" if p.get("preview") else "")
        for p in top_posts
    )

    rss_articles = raw_research.get("rss", {}).get("articles", [])
    rss_text = "\n".join(
        f"[{a['source']}] {a['title']}\n  → {a['summary'][:350]}"
        for a in rss_articles[:18]
    )

    prompt = f"""You are a LinkedIn content strategist for Nabilah Azman, a Finance Analyst at Warner Music (ACCA qualified) who posts about AI and automation for finance professionals. Her brand is The Bell. Content is direct, first-person, stat-led, never corporate.

CAROUSEL TO PREPARE:
Week {carousel["num"]} of 52
Title: "{carousel["title"]}"
Category: {carousel["category"]}

CURRENT SLIDE SENTENCES:
{slides_text}

REDDIT DISCUSSIONS (AI/productivity communities, this week):
{reddit_text}

RECENT ARTICLES FROM RESEARCH FEEDS:
{rss_text}

Return a JSON object with exactly this structure. No extra text, no markdown fences:

{{
  "best_s1_stat": {{
    "stat": "The exact compelling stat or fact to use as the opening hook for S1",
    "source": "Source name (e.g. McKinsey, Microsoft Work Trend Index, Forrester, etc.)",
    "year": "Year if known, otherwise write 'recent'",
    "why": "One sentence explaining why this works as the S1 for this specific carousel",
    "from_scraped_data": true
  }},
  "hook_variations": [
    {{"type": "stat_led", "hook": "Stat-based S1 under 140 chars", "why": "Why this angle works for this audience"}},
    {{"type": "story_led", "hook": "Personal story S1 under 140 chars", "why": "Why this angle works"}},
    {{"type": "provocative", "hook": "Bold or contrarian S1 under 140 chars", "why": "Why this angle works"}}
  ],
  "audience_insights": {{
    "top_pain_points": ["pain point 1 from Reddit", "pain point 2", "pain point 3"],
    "audience_language": ["exact phrase from Reddit to borrow", "another phrase", "third phrase"],
    "most_relevant_reddit_post": {{
      "title": "Post title",
      "subreddit": "subreddit name",
      "why": "Why this validates the carousel topic"
    }}
  }},
  "research_summary": "2-3 sentences on what this research reveals about why this topic resonates right now with finance and accounting professionals.",
  "recommended_s1": "The single best S1 sentence based on the research (under 140 chars)"
}}"""

    try:
        response = groq_create(client, 
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.65,
        )
        content = response.choices[0].message.content.strip()
        if "```" in content:
            content = re.sub(r"```(?:json)?", "", content).replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"  WARNING: AI generation failed ({e}). Using placeholder insights.")
        return {
            "best_s1_stat": {
                "stat": carousel["slides"][0],
                "source": "Current slide text",
                "year": "—",
                "why": "AI generation failed — review manually.",
                "from_scraped_data": False,
            },
            "hook_variations": [
                {"type": "stat_led", "hook": carousel["slides"][0], "why": "Current S1 text"},
                {"type": "story_led", "hook": "I used to spend hours on this. Then I built a system.", "why": "Generic story hook"},
                {"type": "provocative", "hook": "Most finance professionals are solving this the wrong way.", "why": "Contrarian opener"},
            ],
            "audience_insights": {
                "top_pain_points": ["Manual repetitive tasks", "Time pressure on reporting", "Tool adoption barriers"],
                "audience_language": ["I just accepted it", "nobody showed me", "every single week"],
                "most_relevant_reddit_post": {"title": "—", "subreddit": "—", "why": "AI generation failed"},
            },
            "research_summary": "Research generation failed. Review the Reddit posts and RSS articles below manually to find S1 material.",
            "recommended_s1": carousel["slides"][0],
        }


# ── HTML rendering ─────────────────────────────────────────────────────────────

SLIDE_ROLE = {
    0: ("S1 — HOOK", "Opening stat or observation that stops the scroll."),
    1: ("S2 — PROBLEM", "Establish the before state. Make it specific and relatable."),
    2: ("S3 — MECHANISM", "Explain HOW the fix works. Name the tool specifically."),
    3: ("S4 — RESULT", "Show the concrete outcome. Numbers always beat adjectives."),
    4: ("S5 — ACTION", "Give the reader ONE specific thing to do today."),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_html(carousel: dict, insights: dict, raw_research: dict, week_num: int, next_4: list) -> str:  # noqa: C901
    cat = carousel["category"]
    playbook = PLAYBOOKS.get(cat, PLAYBOOKS["BEFORE_AFTER"])
    scraped_at = raw_research.get("scraped_at", "unknown")
    reddit_total = raw_research.get("reddit", {}).get("total", 0)
    rss_total = raw_research.get("rss", {}).get("total", 0)
    generated_at = datetime.now(timezone.utc).strftime("%d %b %Y")

    # ── Slides section ─────────────────────────────────────────────────────────
    slides_html = ""
    for i, slide_text in enumerate(carousel["slides"]):
        label, hint = SLIDE_ROLE.get(i, (f"S{i+1}", ""))
        s1_class = " s1" if i == 0 else ""
        slides_html += f"""
        <div class="slide-card{s1_class}">
          <div class="slide-label">{esc(label)}</div>
          <p class="slide-text">{esc(slide_text)}</p>
          <p class="slide-hint">{esc(hint)}</p>
        </div>"""

    # ── What to find ───────────────────────────────────────────────────────────
    wtf_items = "".join(f"<li>{esc(item)}</li>" for item in playbook["what_to_find"])

    # ── Checklist ──────────────────────────────────────────────────────────────
    checklist_html = "".join(
        f'<div class="check-item"><span class="check-box">☐</span>{esc(item)}</div>'
        for item in playbook["checklist"]
    )

    # ── Hook lab ───────────────────────────────────────────────────────────────
    hook_types = {"stat_led": "STAT-LED", "story_led": "STORY-LED", "provocative": "PROVOCATIVE"}
    hook_colors = {"stat_led": GOLD, "story_led": "#4a9eff", "provocative": "#e85c5c"}
    hooks_html = ""
    for hv in insights.get("hook_variations", []):
        htype = hv.get("type", "stat_led")
        color = hook_colors.get(htype, GOLD)
        hooks_html += f"""
        <div class="hook-card">
          <div class="hook-type" style="color:{color}">{hook_types.get(htype, htype.upper())}</div>
          <p class="hook-text">"{esc(hv.get('hook', ''))}"</p>
          <p class="hook-why">{esc(hv.get('why', ''))}</p>
        </div>"""

    # ── Audience insights ─────────────────────────────────────────────────────
    pain_points = insights.get("audience_insights", {}).get("top_pain_points", [])
    pain_html = "".join(f"<li>{esc(p)}</li>" for p in pain_points)

    lang_phrases = insights.get("audience_insights", {}).get("audience_language", [])
    lang_html = "".join(f'<span class="phrase">"{esc(p)}"</span>' for p in lang_phrases)

    best_post = insights.get("audience_insights", {}).get("most_relevant_reddit_post", {})

    # ── Reddit top posts ───────────────────────────────────────────────────────
    reddit_posts = raw_research.get("reddit", {}).get("posts", [])
    top_reddit = sorted(reddit_posts, key=lambda x: x.get("score", 0), reverse=True)[:12]
    reddit_html = ""
    for p in top_reddit:
        reddit_html += f"""
        <div class="post-card">
          <a href="{esc(p['url'])}" target="_blank" class="post-link">{esc(p['title'][:120])}</a>
          <div class="post-meta">r/{esc(p['subreddit'])} &middot; {p['score']:,} upvotes &middot; {p['num_comments']} comments</div>
          {f'<p class="post-preview">{esc(p["preview"][:200])}</p>' if p.get("preview") else ''}
        </div>"""

    # ── RSS articles ───────────────────────────────────────────────────────────
    rss_articles = raw_research.get("rss", {}).get("articles", [])
    rss_html = ""
    for a in rss_articles[:10]:
        rss_html += f"""
        <div class="post-card">
          <a href="{esc(a['url'])}" target="_blank" class="post-link">{esc(a['title'][:120])}</a>
          <div class="post-meta">{esc(a['source'])} &middot; {esc(a.get('published', '')[:16])}</div>
          <p class="post-preview">{esc(a['summary'][:280])}</p>
        </div>"""

    # ── Next 4 weeks ───────────────────────────────────────────────────────────
    next_html = ""
    for c in next_4:
        hint = RESEARCH_HINTS.get(c["category"], "Watch for relevant discussions in your communities.")
        next_html += f"""
        <div class="upcoming-card">
          <div class="upcoming-num">Week {c['num']}</div>
          <div class="upcoming-cat">{PLAYBOOKS.get(c['category'], {}).get('label', c['category'])}</div>
          <p class="upcoming-title">{esc(c['title'])}</p>
          <p class="upcoming-hint"><strong>Start looking for:</strong> {esc(hint)}</p>
        </div>"""

    # ── Recommended S1 ─────────────────────────────────────────────────────────
    stat = insights.get("best_s1_stat", {})
    rec_s1 = insights.get("recommended_s1", carousel["slides"][0])

    # ── Next 4 weeks (moved here for use in template) ──────────────────────────
    # already built in next_html above

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Week {week_num} — The Bell Research Brief</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: {CREAM};
    color: {NAVY};
    font-size: 17px;
    line-height: 1.47;
    letter-spacing: -0.02em;
    -webkit-font-smoothing: antialiased;
  }}

  .inner {{
    max-width: 900px;
    margin: 0 auto;
    padding: 0 48px;
  }}

  /* ── Tiles ── */
  .tile        {{ width: 100%; padding: 88px 0; }}
  .tile-cream  {{ background: {CREAM}; }}
  .tile-navy   {{ background: {NAVY}; color: #fff; }}
  .tile-white  {{ background: #ffffff; }}

  .tile-header {{
    background:
      linear-gradient(160deg, rgba(26,26,46,0.97) 0%, rgba(26,26,46,0.82) 100%),
      url('https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1600&q=80&fit=crop') center/cover no-repeat;
    color: #fff;
    padding: 112px 0 88px;
  }}

  .photo-band {{
    background:
      linear-gradient(rgba(26,26,46,0.78), rgba(26,26,46,0.78)),
      url('https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=1600&q=80&fit=crop') center/cover no-repeat;
    padding: 64px 0;
    text-align: center;
  }}
  .photo-band-quote {{
    font-size: 26px;
    font-weight: 300;
    color: #ffffff;
    line-height: 1.5;
    letter-spacing: -0.01em;
    max-width: 640px;
    margin: 0 auto;
  }}
  .photo-band-attr {{
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    margin-top: 16px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }}

  /* ── Eyebrow + section head ── */
  .eyebrow {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 12px;
  }}
  .section-head {{
    font-size: 40px;
    font-weight: 600;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
  }}
  .section-sub {{
    font-size: 17px;
    font-weight: 400;
    line-height: 1.47;
    letter-spacing: -0.02em;
    margin-bottom: 48px;
    opacity: 0.6;
  }}
  .tile-navy .section-head {{ color: #ffffff; }}
  .tile-navy .section-sub  {{ color: rgba(255,255,255,0.6); }}

  /* ── Header ── */
  .header-brand {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 24px;
  }}
  .header-pill {{
    display: inline-block;
    background: {GOLD};
    color: {NAVY};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 18px;
    border-radius: 9999px;
    margin-bottom: 28px;
  }}
  .header-title {{
    font-size: 56px;
    font-weight: 600;
    line-height: 1.07;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 24px;
    max-width: 760px;
  }}
  .header-sub {{
    font-size: 21px;
    font-weight: 300;
    color: rgba(255,255,255,0.65);
    letter-spacing: -0.01em;
    margin-bottom: 32px;
    max-width: 560px;
    line-height: 1.4;
  }}
  .header-meta {{
    font-size: 13px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.02em;
  }}
  .header-dot {{ color: rgba(255,255,255,0.2); margin: 0 8px; }}

  /* ── Cards ── */
  .card-dark {{
    background: rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 28px;
  }}
  .card-dark .eyebrow {{ margin-bottom: 16px; }}
  .card-dark ul {{ padding-left: 20px; }}
  .card-dark li {{
    color: rgba(255,255,255,0.85);
    font-size: 15px;
    line-height: 1.65;
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }}
  .card-dark p {{
    color: rgba(255,255,255,0.85);
    font-size: 15px;
    line-height: 1.65;
    letter-spacing: -0.01em;
  }}

  .two-col    {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .two-col-sm {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px; }}

  .guidance-box {{
    background: rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 24px 28px;
    border-left: 3px solid {GOLD};
  }}
  .guidance-box .g-label {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 10px;
  }}
  .guidance-box p {{
    font-size: 14px;
    color: rgba(255,255,255,0.85);
    line-height: 1.65;
    letter-spacing: -0.01em;
  }}

  /* ── Slides ── */
  .slides-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }}
  .slide-card {{
    background: #ffffff;
    border: 1px solid rgba(26,26,46,0.1);
    border-radius: 18px;
    padding: 20px 16px;
  }}
  .slide-card.s1 {{
    border-top: 3px solid {GOLD};
    background: #fffef8;
  }}
  .slide-label {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {MUTED};
    margin-bottom: 10px;
  }}
  .slide-card.s1 .slide-label {{ color: {GOLD}; }}
  .slide-text {{
    font-size: 13px;
    font-weight: 600;
    color: {NAVY};
    line-height: 1.5;
    letter-spacing: -0.01em;
    margin-bottom: 10px;
  }}
  .slide-hint {{
    font-size: 11px;
    color: {MUTED};
    line-height: 1.5;
    font-style: italic;
  }}

  /* ── Recommended S1 — the only shadow in the system ── */
  .rec-s1-wrap {{
    background: {GOLD};
    border-radius: 18px;
    padding: 52px 56px;
    box-shadow: 0 12px 64px rgba(26,26,46,0.18);
    margin-bottom: 48px;
    position: relative;
    overflow: hidden;
  }}
  .rec-s1-deco {{
    position: absolute;
    top: -20px;
    right: 40px;
    font-size: 200px;
    font-weight: 700;
    color: rgba(26,26,46,0.06);
    line-height: 1;
    pointer-events: none;
    font-family: Georgia, serif;
  }}
  .rec-s1-label {{
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(26,26,46,0.5);
    margin-bottom: 20px;
  }}
  .rec-s1-text {{
    font-size: 40px;
    font-weight: 600;
    line-height: 1.12;
    letter-spacing: -0.02em;
    color: {NAVY};
    margin-bottom: 24px;
    max-width: 680px;
    position: relative;
  }}
  .rec-s1-source {{
    font-size: 14px;
    color: rgba(26,26,46,0.55);
    letter-spacing: -0.01em;
    padding-top: 20px;
    border-top: 1px solid rgba(26,26,46,0.15);
  }}
  .rec-s1-why {{
    font-size: 15px;
    color: {NAVY};
    opacity: 0.7;
    margin-top: 10px;
    font-style: italic;
    line-height: 1.5;
    letter-spacing: -0.01em;
  }}

  h3 {{
    font-size: 21px;
    font-weight: 600;
    line-height: 1.19;
    letter-spacing: -0.01em;
    color: {NAVY};
    margin-bottom: 16px;
    margin-top: 0;
  }}
  .tile-navy h3 {{ color: #ffffff; }}

  /* ── Hooks ── */
  .hooks-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
  .hook-card {{
    background: #ffffff;
    border: 1px solid rgba(26,26,46,0.1);
    border-radius: 18px;
    padding: 28px 24px;
  }}
  .hook-type {{
    display: block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 14px;
  }}
  .hook-text {{
    font-size: 16px;
    font-weight: 600;
    color: {NAVY};
    line-height: 1.4;
    letter-spacing: -0.01em;
    margin-bottom: 12px;
    font-style: italic;
  }}
  .hook-why {{
    font-size: 13px;
    color: {MUTED};
    line-height: 1.5;
    letter-spacing: -0.01em;
  }}

  /* ── Audience ── */
  .pain-list {{ padding-left: 20px; }}
  .pain-list li {{
    font-size: 15px;
    color: rgba(255,255,255,0.85);
    line-height: 1.65;
    margin-bottom: 12px;
    letter-spacing: -0.01em;
  }}
  .phrase-bank {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }}
  .phrase {{
    background: rgba(255,255,255,0.1);
    color: #ffffff;
    padding: 7px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-style: italic;
    letter-spacing: -0.01em;
  }}
  .best-post-card {{
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 32px;
  }}
  .best-post-card .bp-label {{
    display: block;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 10px;
  }}
  .best-post-card .bp-title {{
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.01em;
  }}
  .best-post-card .bp-why {{
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    margin-top: 6px;
    letter-spacing: -0.01em;
  }}

  /* ── Post cards ── */
  .post-list {{ display: flex; flex-direction: column; gap: 12px; }}
  .post-card {{
    background: #ffffff;
    border: 1px solid rgba(26,26,46,0.1);
    border-radius: 18px;
    padding: 22px 26px;
  }}
  .post-link {{
    font-size: 15px;
    font-weight: 600;
    color: {NAVY};
    text-decoration: none;
    letter-spacing: -0.01em;
    display: block;
    margin-bottom: 6px;
    line-height: 1.4;
  }}
  .post-link:hover {{ color: {GOLD}; }}
  .post-meta {{
    font-size: 12px;
    color: {MUTED};
    letter-spacing: -0.01em;
    margin-bottom: 8px;
  }}
  .post-preview {{
    font-size: 14px;
    color: {MUTED};
    line-height: 1.55;
    font-style: italic;
    letter-spacing: -0.01em;
  }}

  .section-gap {{ margin-top: 64px; }}

  /* ── Checklist ── */
  .check-list {{ display: flex; flex-direction: column; gap: 12px; }}
  .check-item {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    background: rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 18px 24px;
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    line-height: 1.55;
    letter-spacing: -0.01em;
  }}
  .check-box {{
    font-size: 20px;
    color: {GOLD};
    flex-shrink: 0;
    line-height: 1.2;
  }}

  /* ── Upcoming ── */
  .upcoming-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
  .upcoming-card {{
    background: #ffffff;
    border: 1px solid rgba(26,26,46,0.1);
    border-radius: 18px;
    padding: 22px 20px;
  }}
  .upcoming-num {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: {GOLD};
    margin-bottom: 4px;
  }}
  .upcoming-cat {{
    font-size: 10px;
    color: {MUTED};
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
  }}
  .upcoming-title {{
    font-size: 13px;
    font-weight: 600;
    color: {NAVY};
    line-height: 1.4;
    letter-spacing: -0.01em;
    margin-bottom: 10px;
  }}
  .upcoming-hint {{
    font-size: 11.5px;
    color: {MUTED};
    line-height: 1.5;
    letter-spacing: -0.01em;
  }}
  .upcoming-hint strong {{ color: {NAVY}; font-weight: 600; }}

  /* ── Mobile ── */
  @media (max-width: 640px) {{
    .inner        {{ padding: 0 20px; }}
    .tile         {{ padding: 56px 0; }}
    .tile-header  {{ padding: 64px 0 52px; }}
    .photo-band   {{ padding: 44px 0; }}

    .header-title     {{ font-size: 30px; }}
    .header-sub       {{ font-size: 17px; }}
    .photo-band-quote {{ font-size: 18px; }}
    .section-head     {{ font-size: 26px; }}

    .slides-grid   {{ grid-template-columns: 1fr; gap: 10px; }}
    .two-col       {{ grid-template-columns: 1fr; }}
    .two-col-sm    {{ grid-template-columns: 1fr; }}
    .hooks-grid    {{ grid-template-columns: 1fr; }}
    .upcoming-grid {{ grid-template-columns: 1fr 1fr; gap: 10px; }}

    .rec-s1-wrap  {{ padding: 32px 24px; }}
    .rec-s1-text  {{ font-size: 24px; }}
    .rec-s1-deco  {{ font-size: 120px; right: 16px; }}

    .card-dark   {{ padding: 20px 18px; }}
    .check-item  {{ padding: 14px 18px; font-size: 14px; }}
    .post-card   {{ padding: 16px 18px; }}
    .hook-card   {{ padding: 20px 18px; }}
    .upcoming-card {{ padding: 16px 14px; }}

    .guidance-box {{ padding: 18px 20px; }}
    .phrase {{ font-size: 12px; padding: 5px 12px; }}
    .section-gap {{ margin-top: 44px; }}
  }}
</style>
</head>
<body>

<!-- HEADER — photo background -->
<div class="tile-header">
  <div class="inner">
    <span class="header-brand">The Bell &middot; LinkedIn Research Brief</span>
    <span class="header-pill">{esc(playbook["label"])}</span>
    <h1 class="header-title">{esc(carousel["title"])}</h1>
    <p class="header-sub">Your weekly content research brief &mdash; everything you need before you write a single slide.</p>
    <p class="header-meta">
      Week {week_num} of 52
      <span class="header-dot">&middot;</span>
      {generated_at}
      <span class="header-dot">&middot;</span>
      {reddit_total} Reddit posts
      <span class="header-dot">&middot;</span>
      {rss_total} articles
    </p>
  </div>
</div>

<!-- SECTION 1 — Carousel slides — Cream -->
<div class="tile tile-cream">
  <div class="inner">
    <span class="eyebrow">This Week&rsquo;s Carousel</span>
    <h2 class="section-head">Five slides. One story.</h2>
    <p class="section-sub">Your S1 hook is the only slide that matters until someone swipes. Make it a status grenade.</p>
    <div class="slides-grid">
      {slides_html}
    </div>
  </div>
</div>

<!-- PHOTO BAND — quote break -->
<div class="photo-band">
  <div class="inner">
    <p class="photo-band-quote">&ldquo;The goal is not to post more. It is to post things people save.&rdquo;</p>
    <p class="photo-band-attr">The Bell &middot; Build in Public</p>
  </div>
</div>

<!-- SECTION 2 — Research Playbook — Navy -->
<div class="tile tile-navy">
  <div class="inner">
    <span class="eyebrow">Research Playbook</span>
    <h2 class="section-head">What to look for this week.</h2>
    <p class="section-sub">Category: {esc(playbook["label"])}. These are the four things that make an S1 land.</p>
    <div class="two-col">
      <div class="card-dark">
        <span class="eyebrow">What to look for</span>
        <ul>{wtf_items}</ul>
      </div>
      <div class="card-dark">
        <span class="eyebrow">S1 Formula</span>
        <p>{esc(playbook["s1_formula"])}</p>
      </div>
    </div>
    <div class="two-col-sm">
      <div class="guidance-box">
        <span class="g-label">S4 needs</span>
        <p>{esc(playbook["s4_guidance"])}</p>
      </div>
      <div class="guidance-box">
        <span class="g-label">S5 needs</span>
        <p>{esc(playbook["s5_guidance"])}</p>
      </div>
    </div>
  </div>
</div>

<!-- SECTION 3 — Recommended S1 + Hook Lab — White -->
<div class="tile tile-white">
  <div class="inner">
    <span class="eyebrow">AI-Curated Opening Hook</span>
    <h2 class="section-head">Your recommended S1.</h2>
    <p class="section-sub">Generated from this week&rsquo;s research. Use it as-is or remix one of the three angles below.</p>
    <div class="rec-s1-wrap">
      <div class="rec-s1-deco">&ldquo;</div>
      <span class="rec-s1-label">&#9733; Recommended S1 &mdash; curated from scraped research</span>
      <p class="rec-s1-text">{esc(rec_s1)}</p>
      <p class="rec-s1-source">
        Based on: {esc(stat.get("stat", "—"))}
        <br>Source: {esc(stat.get("source", "—"))} ({esc(str(stat.get("year", "—")))})
      </p>
      <p class="rec-s1-why">{esc(stat.get("why", ""))}</p>
    </div>
    <h3>Three hook angles &mdash; choose one or remix:</h3>
    <div class="hooks-grid">
      {hooks_html}
    </div>
  </div>
</div>

<!-- SECTION 4 — Audience Intel — Navy -->
<div class="tile tile-navy">
  <div class="inner">
    <span class="eyebrow">Audience Intel</span>
    <h2 class="section-head">What your audience is saying.</h2>
    <p class="section-sub">Real language from real communities. Use these exact phrases in your slides &mdash; not your own corporate words.</p>
    <div class="two-col">
      <div>
        <h3>Top pain points this week</h3>
        <ul class="pain-list">{pain_html}</ul>
      </div>
      <div>
        <h3>Language to borrow</h3>
        <div class="phrase-bank">{lang_html}</div>
      </div>
    </div>
    {'<div class="best-post-card"><span class="bp-label">&#9733; Most relevant post</span><div class="bp-title">' + esc(best_post.get("title","—")) + '</div><div class="bp-why">r/' + esc(best_post.get("subreddit","—")) + ' &nbsp;&middot;&nbsp; ' + esc(best_post.get("why","")) + '</div></div>' if best_post.get("title") else ''}
  </div>
</div>

<!-- SECTION 5 — Reddit + RSS — Cream -->
<div class="tile tile-cream">
  <div class="inner">
    <span class="eyebrow">Community Research</span>
    <h2 class="section-head">Reddit &mdash; top posts this week.</h2>
    <p class="section-sub">Click through the highest-scoring posts. The comments are where the real S1 material hides.</p>
    <div class="post-list">
      {reddit_html}
    </div>

    <div class="section-gap">
      <span class="eyebrow">Stat Bank</span>
      <h2 class="section-head">Recent articles.</h2>
      <p class="section-sub">Verify any stat before citing it. Paywalled sources may have different numbers in the abstract.</p>
      <div class="post-list">
        {rss_html}
      </div>
    </div>
  </div>
</div>

<!-- SECTION 6 — Checklist — Navy -->
<div class="tile tile-navy">
  <div class="inner">
    <span class="eyebrow">Pre-Publish Checklist</span>
    <h2 class="section-head">Before you design a single slide.</h2>
    <p class="section-sub">Category: {esc(playbook["label"])}. Every item must be true before you open Canva.</p>
    <div class="check-list">
      {checklist_html}
    </div>
  </div>
</div>

<!-- SECTION 7 — Next 4 weeks — Cream -->
<div class="tile tile-cream">
  <div class="inner">
    <span class="eyebrow">Forward Planning</span>
    <h2 class="section-head">Next 4 weeks &mdash; start looking now.</h2>
    <p class="section-sub">The best S1 stats are found a week early. Bookmark discussions as you find them.</p>
    <div class="upcoming-grid">
      {next_html}
    </div>
  </div>
</div>

</body>
</html>"""


# ── Main ───────────────────────────────────────────────────────────────────────

def main(week_num: int = None):
    # Determine which week to generate for
    if week_num is None:
        log = json.loads(CONTENT_LOG.read_text())
        week_num = log.get("current_week", 1)
        print(f"Using current_week from log: {week_num}")

    # Validate research data exists
    if not RAW_RESEARCH.exists():
        print(f"ERROR: Research data not found at {RAW_RESEARCH}")
        print("Run first: python tools/scrape_linkedin_research.py")
        raise SystemExit(1)

    # Load research freshness
    raw_research = json.loads(RAW_RESEARCH.read_text())
    scraped_at = raw_research.get("scraped_at", "")
    if scraped_at:
        try:
            age_hours = (datetime.now(timezone.utc) - datetime.fromisoformat(scraped_at.rstrip("Z")).replace(tzinfo=timezone.utc)).total_seconds() / 3600
            if age_hours > 168:
                print(f"WARNING: Research data is {age_hours:.0f}h old. Consider re-scraping.")
        except Exception:
            pass

    # Load carousel data
    schedule = json.loads(TOPIC_SCHEDULE.read_text())
    all_carousels = schedule["carousels"]
    carousel = next((c for c in all_carousels if c["num"] == week_num), None)
    if not carousel:
        print(f"ERROR: Week {week_num} not found in topic schedule (1–{len(all_carousels)})")
        raise SystemExit(1)

    print(f"Generating research brief for Week {week_num}: {carousel['title']}")
    print(f"  Category: {carousel['category']}")

    # Generate AI insights
    print("  Calling Groq for insights...")
    insights = generate_insights(carousel, raw_research)

    # Next 4 weeks
    next_4 = [c for c in all_carousels if c["num"] > week_num][:4]

    # Build and save HTML
    html = build_html(carousel, insights, raw_research, week_num, next_4)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html)

    print(f"  → Saved: {OUTPUT_PATH}")
    print(f"  Open:    open {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LinkedIn research brief")
    parser.add_argument("--week", type=int, default=None, help="Week number (default: current_week)")
    args = parser.parse_args()
    main(args.week)
