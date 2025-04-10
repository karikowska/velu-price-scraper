from tools.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list[dict[str, str]]:
    items = browser_loader(link=f"https://goodsmileeurope.com/search?type=product&filter.v.availability=1&options%5Bprefix%5D=last&q={query}",
                        query=query,
                        product_grid_tag=".filters-results", 
                        grid_item_tag="div.card.column.quarter")
    
    results = []
    
    for item in items:
        url = "https://goodsmileeurope.com" + item.select_one("a")["href"]
        
        title_tag = item.select_one("div.card__link")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url
        })

    return results