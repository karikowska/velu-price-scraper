import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(f"https://animota.net/search?q={query}")
        page.wait_for_selector(".product-grid")
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

        items = soup.select("li.grid__item")

        results = []
        
        for item in items[:limit]:
            try:
                status = item.select_one("span.badge")
                print(status)
                if status and "sold out" in status.text.lower():
                    continue
            except:
                pass
            
            url = "https://www.animota.net" + item.select_one("a")["href"]
            
            title_tag = item.select_one("a.full-unstyled-link")
            title = title_tag.get_text(strip=True) if title_tag else None

            if not (title and url):
                continue

            results.append({
                "title": title,
                "url": url
            })

        return results
