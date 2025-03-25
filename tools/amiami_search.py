import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def build_search_url(query: str) -> str:
    return f"https://www.amiami.com/search/?s_keywords={quote_plus(query)}"

def get_search_results(query: str, limit=5) -> list:
    url = build_search_url(query)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("li.search_item")  # newer AmiAmi layout
    if not items:
        print("⚠️ No matching HTML blocks. The site may have changed layout.")
        return []

    results = []
    for item in items[:limit]:
        title_tag = item.select_one(".product_name")
        price_tag = item.select_one(".price")
        link_tag = item.select_one("a")

        if not (title_tag and price_tag and link_tag):
            continue

        results.append({
            "title": title_tag.get_text(strip=True),
            "price": price_tag.get_text(strip=True),
            "url": link_tag.get("href")
        })

    print(res[:1000])
    
    return results
