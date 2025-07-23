"""CLI-based price scraper for supported sites."""
import sys
import yaml
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
import os
from helpers.scraper import get_html, get_text_snippets
from llms.price_extractor import extract_price_info
from helpers.transformer_tools import single_embedding_ranker
from helpers.other_helpers import shop_check

def main() -> str:
    """Main driver function of the price scraper."""
    
    config = False
    
    # parse cmd args
    # if 3 args, assume single query mode
    if len(sys.argv) == 3:
        query = sys.argv[1].lower()
        site = sys.argv[2].lower()
        
    # if 2 args, assume batch mode with config file
    elif len(sys.argv) == 2:
        path_to_config = Path(sys.argv[1])
        with open(path_to_config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    
    # help with usage for user if they type in incorrect input
    else:
        print("Single query usage: python main.py '<product_query>' '<site>'")
        print("Multi-query usage: python main.py 'path/to/config/yaml'")
        print("Supported sites: aa, anim, jf, sol, nng, gsce")
        return

    # if using batch mode, load config and perform shop checks with each query
    if config:
        links = []
        for config_d in config:
            query = config_d["name"]
            site_list = config_d["stores"]
            for site in site_list:
                links.append(shop_check(query, site))
                sleep(2)
    
    else:
        links = shop_check(query, site)
        
    if not links:
        return "❌ No results found."
    
    # run links through embedding ranker, which uses a transformer model to rank the links in terms of relevance and throw out anything below threshold
    new_links = []
    if len(links) == 1:
        new_links = single_embedding_ranker(links, query)
    else:
        new_links.append(single_embedding_ranker(links, query))
    
    # test if site_list is being used, which specifies which sites should be scraped - this is a batch mode only feature
    try:
        site_list
    except NameError:
        site_list = 0
        
    for link in new_links[:(len(site_list) if site_list>1 else 3)]:
        if type(link) == list and len(link) > 1:
            link = link[0]
        print(f"\n🔎 Scraping: {link['title']}\n{link['url']}")
        html = get_html(link["url"])
        snippet = get_text_snippets(html)
        if not snippet.strip():
            print("\n!!! No price-like content found in HTML snippet !!!")
            print("Here's the raw snippet preview:\n", snippet[:500])
            continue

        result = extract_price_info(query, link["url"], snippet)
        print(f"💷 Price: {result['price']} | Raw: {result['raw_response']}")
        

if __name__ == "__main__":
    main()
