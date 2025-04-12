from helpers.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list:
    items = browser_loader(link=f"https://animota.net/search?q={query}",
                        query=query,
                        product_grid_tag=".product-grid", 
                        grid_item_tag="li.grid__item")

    results = []
    
    for item in items[:limit]:
        try:
            status = item.select_one("span.badge")
            if status and "sold out" in status.text.lower():
                continue
        except:
            pass
        
        url = "https://www.animota.net" + item.select_one("a")["href"]
        
        title_tag = item.select_one("a.full-unstyled-link")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url
        })

    return results
