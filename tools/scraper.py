import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def browser_loader(link: str, query: str, product_grid_tag: str, grid_item_tag: str) -> list[dict[str, str]]:
    """Initialize a browser session using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(link)
        page.wait_for_selector(product_grid_tag)
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

        items = soup.select(grid_item_tag)
        
        return items


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
        if text and any(symbol in text for symbol in ["$", "£", "€", "¥", "USD", "GBP", "EUR", "JPY"]):
            snippets.append(text)

    return "\n".join(snippets[:limit])
