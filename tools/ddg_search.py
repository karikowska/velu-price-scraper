import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_real_url(ddg_url):
    if "uddg=" in ddg_url:
        parsed = urlparse(ddg_url)
        qs = parse_qs(parsed.query)
        if "uddg" in qs:
            return unquote(qs["uddg"][0])
    return ddg_url


def search_duckduckgo(site: str, query: str, limit=5) -> list:
    search_query = f"site:{site} {query}"
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(search_query)}"

    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.select("a.result__a"):
        title = a.get_text(strip=True)
        raw_url = a.get("href")
        final_url = extract_real_url(raw_url)

        # 🚫 Skip bad URLs
        if "duckduckgo.com" in final_url or not final_url.startswith("http"):
            continue

        results.append({
            "title": title,
            "url": final_url
        })

        if len(results) >= limit:
            break

    return results

