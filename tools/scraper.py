import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_html(url: str) -> str:
    """Fetch raw HTML from the given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""

def get_text_snippets(html: str, limit=10) -> str:
    """Extract potentially price-relevant text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    snippets = []

    for tag in soup.find_all(["div", "span", "p", "li"]):
        text = tag.get_text().strip()
        if text and any(symbol in text for symbol in ["$", "£", "€", "¥"]):
            snippets.append(text)

    return "\n".join(snippets[:limit])
