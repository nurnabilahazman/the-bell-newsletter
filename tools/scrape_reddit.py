#!/usr/bin/env python3
"""
Pulls top posts from personal finance subreddits via Reddit's public JSON API.
No auth required. Saves to .tmp/reddit_content.json.
Usage: python tools/scrape_reddit.py [--limit N]
"""

import json
import time
import argparse
from datetime import datetime
from pathlib import Path

import requests

SUBREDDITS = ["personalfinance", "investing", "financialindependence"]
POSTS_PER_SUB = 10
OUTPUT_PATH = Path(".tmp/reddit_content.json")
HEADERS = {"User-Agent": "newsletter-bot/1.0"}


def fetch_top_posts(subreddit: str, limit: int) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit={limit}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()

    posts = []
    for child in data["data"]["children"]:
        post = child["data"]
        # Skip stickied mod posts and link posts with no text
        if post.get("stickied"):
            continue

        selftext = post.get("selftext", "")
        # Trim preview to 400 chars
        preview = selftext[:400].strip() if selftext and selftext != "[removed]" else ""

        posts.append({
            "title": post.get("title", "").strip(),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "subreddit": subreddit,
            "selftext_preview": preview,
        })

    return posts


def main(limit: int = POSTS_PER_SUB):
    print(f"Fetching top posts from {len(SUBREDDITS)} subreddits...")

    all_posts = []
    for sub in SUBREDDITS:
        try:
            posts = fetch_top_posts(sub, limit)
            print(f"  {len(posts)} posts from r/{sub}")
            all_posts.extend(posts)
            time.sleep(1)  # Be polite to Reddit's public API
        except Exception as e:
            print(f"  WARNING: Failed to fetch r/{sub}: {e}")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({
            "scraped_at": datetime.utcnow().isoformat(),
            "total": len(all_posts),
            "posts": all_posts,
        }, f, indent=2)

    print(f"\nSaved {len(all_posts)} posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=POSTS_PER_SUB,
                        help="Max posts per subreddit")
    args = parser.parse_args()
    main(args.limit)
