#!/usr/bin/env python3
"""
Researches 3 product ideas (one per theme) using Tavily.
Saves results to .tmp/product_research.json.
Usage: python tools/research_products.py
"""

import json
import os
from pathlib import Path

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

THEMES_PATH = Path("config/product_themes.json")
OUTPUT_PATH = Path(".tmp/product_research.json")


def research_theme(client: TavilyClient, theme: dict) -> dict:
    results = []
    for query in theme["search_queries"][:2]:  # 2 searches per theme = 6 API calls total
        response = client.search(query=query, search_depth="basic", max_results=3)
        for r in response.get("results", []):
            results.append({
                "title":   r.get("title", ""),
                "content": r.get("content", "")[:600],
                "url":     r.get("url", "")
            })
    return {
        "theme_id":    theme["id"],
        "theme_name":  theme["name"],
        "description": theme["description"],
        "format":      theme["format"],
        "price_range": theme["price_range"],
        "research":    results
    }


def main():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("ERROR: TAVILY_API_KEY not set in .env")
        raise SystemExit(1)

    if not THEMES_PATH.exists():
        print(f"ERROR: {THEMES_PATH} not found")
        raise SystemExit(1)

    with open(THEMES_PATH) as f:
        themes_data = json.load(f)

    client = TavilyClient(api_key=api_key)
    all_research = []

    print(f"Researching {len(themes_data['themes'])} product themes...")
    for theme in themes_data["themes"]:
        print(f"  → {theme['name']}...")
        result = research_theme(client, theme)
        all_research.append(result)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump({"themes": all_research}, f, indent=2)

    print(f"Research saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
