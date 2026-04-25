#!/usr/bin/env python3
"""
Scrapes finance RSS feeds and saves articles to .tmp/rss_content.json.
Usage: python tools/scrape_rss.py [--limit N]
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path

import feedparser
from dotenv import load_dotenv

load_dotenv()

ARTICLES_PER_FEED = 5
OUTPUT_PATH = Path(".tmp/rss_content.json")


def parse_feed(url: str, limit: int) -> list[dict]:
    feed = feedparser.parse(url)
    source_name = feed.feed.get("title", url)
    articles = []

    for entry in feed.entries[:limit]:
        summary = entry.get("summary", "")
        # Strip basic HTML tags from summary
        import re
        summary = re.sub(r"<[^>]+>", "", summary).strip()

        articles.append({
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", ""),
            "summary": summary[:500],
            "published": entry.get("published", ""),
            "source": source_name,
        })

    return articles


def main(limit: int = ARTICLES_PER_FEED):
    feeds_env = os.getenv("RSS_FEEDS", "")
    if not feeds_env:
        print("ERROR: RSS_FEEDS not set in .env")
        raise SystemExit(1)

    feed_urls = [url.strip() for url in feeds_env.split(",") if url.strip()]
    print(f"Scraping {len(feed_urls)} RSS feeds (up to {limit} articles each)...")

    all_articles = []
    for url in feed_urls:
        try:
            articles = parse_feed(url, limit)
            print(f"  {len(articles)} articles from: {url}")
            all_articles.extend(articles)
        except Exception as e:
            print(f"  WARNING: Failed to parse {url}: {e}")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({
            "scraped_at": datetime.utcnow().isoformat(),
            "total": len(all_articles),
            "articles": all_articles,
        }, f, indent=2)

    print(f"\nSaved {len(all_articles)} articles to {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=ARTICLES_PER_FEED,
                        help="Max articles per feed")
    args = parser.parse_args()
    main(args.limit)
