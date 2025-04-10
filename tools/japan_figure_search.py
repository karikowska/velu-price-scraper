from tools.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list[dict[str, str]]:
    items = browser_loader(link=f"https://japan-figure.com/en-gb/search?q={query}",
                        query=query,
                        product_grid_tag=".productgrid--items", 
                        grid_item_tag="div.productitem")
    
    results = []
    
    for item in items:
        actions = item.select_one("figure.productitem--image")
        soon_span = actions.select_one("span.productitem__badge")
        if soon_span and "sold out" in soon_span.text.lower():
            continue
        
        url = "https://japan-figure.com" + item.select_one("a")["href"]
        
        title_tag = item.select_one("h2.productitem--title")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url
        })

    return results
