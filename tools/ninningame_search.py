import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(f"https://www.nin-nin-game.com/en/search?controller=search&orderby=date_add&orderway=desc&search_query={query}&submit_search=Search")
        page.wait_for_selector(".product-grid")
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

        items = soup.select("li.general_block_card")

        results = []
        
        for item in items[:limit]:
            url = item.select_one("a")["href"]
            
            print(url)
            
            actions = item.select_one("div.actions")
            add_btn = actions.select_one("button.ajax_add_to_cart_button")
            if add_btn and "add to cart" in add_btn.text.lower():
                None

            # 2. Check for "Soon available" span (coming soon)
            soon_span = actions.select_one("span.soon")
            if soon_span and "soon available" in soon_span.text.lower():
                continue
            
            title_tag = item.select_one("a.product-name")
            title = title_tag.get_text(strip=True) if title_tag else None
            print(title)

            if not (title and url):
                continue

            results.append({
                "title": title,
                "url": url
            })

        return results
