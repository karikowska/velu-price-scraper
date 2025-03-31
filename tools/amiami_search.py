import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# !!!IMPORTANT!!! - this doesn't work - AmiAmi uses cloudflare!
def build_search_url(query: str) -> str:
    return f"https://www.amiami.com/eng/search/list/?s_keywords={quote_plus(query)}"

def get_search_results(query: str, limit=5) -> list:
    url = build_search_url(query)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    print(soup.prettify()[:1000])
    
    items = soup.select(".newly-added-items__item nomore")
    if not items:
        print("No matching HTML blocks. The site may have changed layout.")
        return []

    results = []
    for item in items[:limit]:
        stock_tags = item.select_one('.newly-added-items__item__tag-list')
        stock_status = next((
            tag.text.strip()
            for tag in stock_tags
            if tag.get('style') != 'display: none;'
        ), 'Unknown')

        if stock_status == 'Unknown' or 'Order Closed':
            continue
        
        url = item.select_one('a')['href']
        
        title_tag = item.select_one('.newly-added-items__item__name')
        title = title_tag.text.strip() if title_tag else 'N/A'

        # price_tag = item.select_one('.newly-added-items__item__price')
        # price = price_tag.text.strip() if price_tag else 'N/A'

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url,
        })
    
    return results
