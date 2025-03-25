import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def build_amazon_url(query: str) -> str:
    return f"https://www.amazon.co.uk/s?k={quote_plus(query)}"

def get_search_results(query: str, limit=5) -> list:
    url = build_amazon_url(query)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("div.s-result-item[data-component-type='s-search-result']")

    results = []
    for item in items[:limit]:
        title_tag = item.select_one("h2 a span")
        price_whole = item.select_one(".a-price .a-price-whole")
        price_fraction = item.select_one(".a-price .a-price-fraction")
        link_tag = item.select_one("h2 a")

        if not (title_tag and price_whole and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        price = price_whole.get_text(strip=True)
        if price_fraction:
            price += "." + price_fraction.get_text(strip=True)

        url = "https://www.amazon.co.uk" + link_tag["href"]

        results.append({
            "title": title,
            "price": "£" + price,
            "url": url
        })

    return results
