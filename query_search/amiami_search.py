from helpers.scraper import browser_loader

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# !!!IMPORTANT!!! - this doesn't work - AmiAmi uses cloudflare! Needs a fix :)
def get_search_results(query: str, limit=5) -> list:
    items = browser_loader(link=f"https://amiami.com/search/?query={query}",
                        query=query,
                        product_grid_tag=".ais-Hits-item", 
                        grid_item_tag=".ais-Hits-item")

    results = []
    
    for item in items[:limit]:
        stock_tags = item.select_one('.newly-added-items__item__tag-list')
        stock_status = next((
            tag.text.strip()
            for tag in stock_tags
            if tag.get('style') != 'display: none;'
        ), 'Unknown')

        if stock_status == 'Unknown':
            continue
        elif stock_status == 'Order Closed':
            continue
        
        url = "https://www.amiami.com" + item.select_one('a')['href']
        
        title_tag = item.select_one('.newly-added-items__item__name')
        title = title_tag.text.strip() if title_tag else 'N/A'

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url,
        })
        
    
    return results
