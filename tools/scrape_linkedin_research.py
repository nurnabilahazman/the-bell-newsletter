#!/usr/bin/env python3
"""
Scrapes community discussions (Hacker News + optional Reddit OAuth) and research
RSS feeds for LinkedIn carousel content research. Separate from newsletter scraper.

Data sources:
  - Hacker News Algolia API  (free, no auth required)
  - Reddit OAuth API          (optional — add REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET
                               + REDDIT_USERNAME + REDDIT_PASSWORD to .env)
  - Research RSS feeds        (config/linkedin_research_rss.json)

Usage:
  python tools/scrape_linkedin_research.py                  # scrape all
  python tools/scrape_linkedin_research.py --category TOOL_SPOTLIGHTS
  python tools/scrape_linkedin_research.py --days 14        # look back 14 days

Output: .tmp/linkedin_raw_research.json
"""

import json
import os
import re
import time
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()

HN_HEADERS = {"User-Agent": "bell-newsletter/1.0"}
HN_BASE = "https://hn.algolia.com/api/v1/search"
RSS_ARTICLES_PER_FEED = 6
OUTPUT_PATH = Path(".tmp/linkedin_raw_research.json")
RSS_CONFIG_PATH = Path("config/linkedin_research_rss.json")

# HN search queries per carousel category
CATEGORY_HN_QUERIES = {
    "BEFORE_AFTER": [
        "excel automation finance", "manual work automation savings",
        "spreadsheet automation hours saved", "finance reporting automation",
    ],
    "TOOL_SPOTLIGHTS": [
        "Claude AI productivity", "ChatGPT work tool", "AI tool comparison",
        "Microsoft Copilot workplace", "Tableau data visualization",
    ],
    "EXACT_PROMPTS": [
        "ChatGPT prompt engineering", "AI prompt productivity",
        "LLM prompt work", "Claude prompt template",
    ],
    "SYSTEM_BUILDS": [
        "GitHub Actions automation", "Python automation workflow",
        "no-code automation", "workflow automation build",
    ],
    "HONEST_TAKES": [
        "AI productivity honest review", "ChatGPT limitations",
        "AI hype reality", "automation failure lessons",
    ],
    "BEGINNER_GUIDES": [
        "getting started AI tools", "ChatGPT beginner",
        "no-code automation start", "first automation workflow",
    ],
    "ALL": [
        "AI productivity work", "automation finance",
        "ChatGPT workplace", "excel automation",
        "AI tools professional", "prompt engineering",
    ],
}

# Subreddits per category (used when Reddit OAuth credentials are available)
CATEGORY_SUBREDDITS = {
    "BEFORE_AFTER":    ["excel", "accounting", "productivity", "automation", "financialcareers"],
    "TOOL_SPOTLIGHTS": ["ChatGPT", "ClaudeAI", "productivity", "Office365", "tableau", "PowerBI"],
    "EXACT_PROMPTS":   ["ChatGPT", "ClaudeAI", "PromptEngineering", "productivity"],
    "SYSTEM_BUILDS":   ["automation", "n8n", "nocode", "learnpython", "github"],
    "HONEST_TAKES":    ["ChatGPT", "Futurology", "productivity", "artificial"],
    "BEGINNER_GUIDES": ["ChatGPT", "nocode", "learnprogramming", "productivity"],
    "ALL": [
        "ChatGPT", "ClaudeAI", "productivity", "automation",
        "excel", "accounting", "financialcareers",
    ],
}


# ── Hacker News ────────────────────────────────────────────────────────────────

def fetch_hn(query: str, days_back: int = 14, limit: int = 8) -> list[dict]:
    cutoff = int((datetime.utcnow() - timedelta(days=days_back)).timestamp())
    url = f"{HN_BASE}?query={requests.utils.quote(query)}&tags=story&numericFilters=created_at_i>{cutoff}&hitsPerPage={limit}"
    r = requests.get(url, headers=HN_HEADERS, timeout=12)
    r.raise_for_status()
    posts = []
    for hit in r.json().get("hits", []):
        posts.append({
            "title": hit.get("title", "").strip(),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}",
            "score": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "subreddit": "hackernews",
            "query": query,
            "preview": "",
        })
    return posts


# ── Reddit OAuth (optional) ────────────────────────────────────────────────────

def get_reddit_token():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")
    if not all([client_id, client_secret, username, password]):
        return None
    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(client_id, client_secret),
        data={"grant_type": "password", "username": username, "password": password},
        headers={"User-Agent": f"python:bell-newsletter:v1.0 (by /u/{username})"},
        timeout=12,
    )
    return r.json().get("access_token")


def fetch_reddit(subreddit: str, token: str, limit: int = 15) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "python:bell-newsletter:v1.0",
    }
    url = f"https://oauth.reddit.com/r/{subreddit}/top?t=week&limit={limit}"
    r = requests.get(url, headers=headers, timeout=12)
    r.raise_for_status()
    posts = []
    for child in r.json()["data"]["children"]:
        p = child["data"]
        if p.get("stickied"):
            continue
        selftext = p.get("selftext", "")
        preview = selftext[:400].strip() if selftext not in ("", "[removed]", "[deleted]") else ""
        posts.append({
            "title": p.get("title", "").strip(),
            "url": f"https://reddit.com{p.get('permalink', '')}",
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "subreddit": subreddit,
            "preview": preview,
        })
    return posts


# ── RSS ────────────────────────────────────────────────────────────────────────

def fetch_rss(url: str, name: str, limit: int = RSS_ARTICLES_PER_FEED) -> list[dict]:
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:limit]:
        summary = re.sub(r"<[^>]+>", "", entry.get("summary", "")).strip()
        articles.append({
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", ""),
            "summary": summary[:600],
            "published": entry.get("published", ""),
            "source": name,
        })
    return articles


# ── Main ───────────────────────────────────────────────────────────────────────

def main(category: str = "ALL", days_back: int = 14):
    print(f"Scraping LinkedIn research — category: {category} | lookback: {days_back}d")

    # ── Hacker News ────────────────────────────────────────────────────────────
    hn_queries = CATEGORY_HN_QUERIES.get(category, CATEGORY_HN_QUERIES["ALL"])
    print(f"\n[Hacker News] {len(hn_queries)} queries:")
    hn_posts = []
    seen_urls = set()
    for q in hn_queries:
        try:
            posts = fetch_hn(q, days_back=days_back)
            new_posts = [p for p in posts if p["url"] not in seen_urls]
            for p in new_posts:
                seen_urls.add(p["url"])
            print(f"  {len(new_posts):2d} posts  '{q}'")
            hn_posts.extend(new_posts)
            time.sleep(0.4)
        except Exception as e:
            print(f"  WARNING '{q}': {e}")

    # ── Reddit (if credentials available) ─────────────────────────────────────
    reddit_posts = []
    reddit_token = get_reddit_token()
    if reddit_token:
        subreddits = CATEGORY_SUBREDDITS.get(category, CATEGORY_SUBREDDITS["ALL"])
        print(f"\n[Reddit OAuth] {len(subreddits)} subreddits: {subreddits}")
        for sub in subreddits:
            try:
                posts = fetch_reddit(sub, reddit_token)
                print(f"  {len(posts):2d} posts  r/{sub}")
                reddit_posts.extend(posts)
                time.sleep(1)
            except Exception as e:
                print(f"  WARNING r/{sub}: {e}")
    else:
        print(
            "\n[Reddit] No OAuth credentials found — skipping Reddit.\n"
            "  To enable: add REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,\n"
            "  REDDIT_USERNAME, REDDIT_PASSWORD to .env\n"
            "  (Create a 'script' app at reddit.com/prefs/apps)"
        )

    # Merge community posts: Reddit first (higher signal), then HN
    community_posts = sorted(reddit_posts + hn_posts, key=lambda x: x["score"], reverse=True)

    # ── RSS ────────────────────────────────────────────────────────────────────
    rss_feeds = json.loads(RSS_CONFIG_PATH.read_text())
    print(f"\n[RSS] {len(rss_feeds)} feeds")
    rss_articles = []
    for feed in rss_feeds:
        try:
            articles = fetch_rss(feed["url"], feed["name"])
            print(f"  {len(articles):2d} articles  {feed['name']}")
            rss_articles.extend(articles)
            time.sleep(0.5)
        except Exception as e:
            print(f"  WARNING {feed['name']}: {e}")

    # ── Save ───────────────────────────────────────────────────────────────────
    result = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "days_back": days_back,
        "reddit": {
            "total": len(community_posts),
            "sources": ["reddit"] if reddit_token else ["hackernews"],
            "posts": community_posts,
        },
        "rss": {
            "total": len(rss_articles),
            "articles": rss_articles,
        },
    }
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2))
    print(f"\nSaved → {OUTPUT_PATH}")
    print(f"  Community: {len(community_posts)} posts (HN + {'Reddit' if reddit_token else 'no Reddit'})")
    print(f"  RSS:       {len(rss_articles)} articles from {len(rss_feeds)} feeds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape LinkedIn research content")
    parser.add_argument(
        "--category",
        default="ALL",
        choices=list(CATEGORY_HN_QUERIES.keys()),
        help="Carousel category (default: ALL)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Days to look back for HN posts (default: 14)",
    )
    args = parser.parse_args()
    main(category=args.category, days_back=args.days)
