import json
import yaml
from pathlib import Path
from datetime import datetime
import sys

from tools.scraper import get_html, get_text_snippets
from agents.price_extractor_agent import extract_price_info
from tools.amiami_search import get_search_results as amiami_search
from tools.amazon_search import get_search_results as amazon_search
from tools.google_search import search_google as google_search
from agents.price_selector_agent import pick_best_listing
from tools.ddg_search import search_duckduckgo

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

openai_api_key = os.environ.get("OPENAI_API_KEY")

def scrape(query, site):
    links = search_duckduckgo(site, query)

    if not links:
        print("❌ No DuckDuckGo results found.")
        return

    for link in links[:3]:
        print(f"\n🔎 Scraping: {link['title']}\n{link['url']}")
        html = get_html(link["url"])
        snippet = get_text_snippets(html)
        if not snippet.strip():
            print("⚠️ No price-like content found in HTML snippet.")
            print("Here's the raw snippet preview:\n", snippet[:500])
            continue

        result = extract_price_info(query, link["url"], snippet)
        print(f"💷 Price: {result['price']} | Raw: {result['raw_response']}")


def main():
    if len(sys.argv) == 2 and sys.argv[1].endswith((".yaml", ".yml")):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            items = yaml.safe_load(f)
        for item in items:
            query = item.get("product")
            site = item.get("site")
            if query and site:
                scrape(query, site)
            else:
                print(f"⚠️ Skipping invalid entry: {item}")
    elif len(sys.argv) >= 3:
        query = sys.argv[1].lower()
        site = sys.argv[2].lower()
        scrape(query, site)
    else:
        print("Usage:")
        print("  python main.py '<product_query>' '<site>'")
        print("  python main.py products.yaml")
        print("Supported sites: solaris")

if __name__ == "__main__":
    main()
