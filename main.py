import sys
import yaml
from pathlib import Path

from tools.scraper import get_html, get_text_snippets
from agents.price_extractor_agent import extract_price_info
from tools.amiami_search import get_search_results as amiami_search
from tools.amazon_search import get_search_results as amazon_search
from tools.solaris_search import get_search_results as solaris_search
from tools.ninningame_search import get_search_results as ninningame_search
from tools.google_search import search_google as google_search
from agents.price_selector_agent import pick_best_listing
from tools.ddg_search import search_duckduckgo

def shop_check(query: str, site: str):
    if site == 'amzn':
        links = amazon_search(query)
    elif site == 'sol':
        links = solaris_search(query)
    elif site == 'ebay':
        links = solaris_search(query)
    elif site == 'aa':
        links = amiami_search(query)
    elif site == 'nng':
        links = ninningame_search(query)
        
    return links


def main() -> str:
    config = False
    if len(sys.argv) == 3:
        query = sys.argv[1].lower()
        site = sys.argv[2].lower()
        
    elif len(sys.argv) == 2:
        path_to_config = Path(sys.argv[1])
        with open(path_to_config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
    else:
        print("Single query usage: python main.py '<product_query>' '<site>'")
        print("Multi-query usage: python main.py 'path/to/config/yaml'")
        print("Supported sites: aa, ebay, amzn, sol, nng")
        return

    if config:
        for config_d in config:
            for query, site_list in config_d.items():
                for site in site_list:
                    links = shop_check(query, site)
    
    else:
        links = shop_check(query, site)
        
    if not links:
        return "❌ No results found."

    for link in links[:3]:
        print(f"\n🔎 Scraping: {link['title']}\n{link['url']}")
        html = get_html(link["url"])
        snippet = get_text_snippets(html)
        if not snippet.strip():
            print("!!! No price-like content found in HTML snippet !!!")
            print("Here's the raw snippet preview:\n", snippet[:500])
            continue

        result = extract_price_info(query, link["url"], snippet)
        return f"💷 Price: {result['price']} | Raw: {result['raw_response']}"
        

if __name__ == "__main__":
    main()
