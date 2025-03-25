import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def build_search_url(query: str) -> str:
    return f"https://solarisjapan.com/search?q={quote_plus(query)}"

def get_search_results(query: str, limit=5) -> list:
    url = build_search_url(query)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select(".product-grid .grid__item")  # cards in the search results

    results = []
    for item in items[:limit]:
        title_tag = item.select_one(".card__heading a")
        price_tag = item.select_one(".price--highlight")
        link = title_tag["href"] if title_tag else None

        if not (title_tag and price_tag and link):
            continue

        title = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        url = "https://solarisjapan.com" + link

        results.append({
            "title": title,
            "price": price,
            "url": url
        })

    return results
