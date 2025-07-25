"""Helper functions for scraping."""
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re

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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(link)
        try:
            page.wait_for_selector(product_grid_tag, timeout=20_000)
        except PlaywrightTimeoutError:
            print(f"Timeout: '{product_grid_tag}' not found on the page after 10 seconds. The item cannot be found on the store's page. It may not exist as a listing or the page may be broken or unable to be loaded.")
            browser.close()
            return []
        
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
    """Obtain text snippets from HTML that look like prices using regex."""
    
    soup = BeautifulSoup(html, "html.parser")
    snippets = set()

    price_pattern = re.compile(r"(?i)([\$£€¥]?\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s?(USD|GBP|EUR|JPY)?)")

    for tag in soup.find_all(["div", "span", "p", "li"]):
        text = tag.get_text(separator=" ", strip=True)
        if price_pattern.search(text):
            cleaned = re.sub(r"\s+", " ", text).strip()
            if len(cleaned) > 5:
                snippets.add(cleaned)
            if len(snippets) >= limit:
                break

    return "\n".join(sorted(snippets))
