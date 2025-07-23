from helpers.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def get_search_results(query: str, limit=5) -> list[dict[str, str]]:
    items = browser_loader(link=f"https://solarisjapan.com/search/?query={query}",
                            query=query,
                            product_grid_tag=".ais-Hits-item", 
                            grid_item_tag=".ais-Hits-item")

    results = []
    
    for item in items[:limit]:
        url = "https://solarisjapan.com/" + item.select_one("a")["href"]
        
        title_tag = item.select_one("h3")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url
        })

    return results
