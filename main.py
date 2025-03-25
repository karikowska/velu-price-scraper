import json
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

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py '<product_query>' '<site>'")
        print("Supported sites: amiami, ebay, amazon, solaris")
        return
    
    query = sys.argv[1].lower()
    site = sys.argv[2].lower()

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


if __name__ == "__main__":
    main()
