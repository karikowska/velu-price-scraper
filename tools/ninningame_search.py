from tools.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list[dict[str, str]]:
    """Find relevant items for the query using Nin-Nin Game."""
    items = browser_loader(link=f"https://www.nin-nin-game.com/en/search?controller=search&orderby=date_add&orderway=desc&search_query={query}&submit_search=Search",
                        query=query,
                        product_grid_tag=".product-grid", 
                        grid_item_tag="li.general_block_card")
    
    results = []
    
    for item in items[:limit]:
        actions = item.select_one("div.actions")
        soon_span = actions.select_one("span.soon")
        if soon_span and "soon available" in soon_span.text.lower():
            continue
        
        add_btn = actions.select_one("button.ajax_add_to_cart_button")
        if add_btn and "add to cart" in add_btn.text.lower():
            None
        
        url = item.select_one("a")["href"]
        
        title_tag = item.select_one("a.product-name")
        title = title_tag.get_text(strip=True) if title_tag else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url
        })

    return results
