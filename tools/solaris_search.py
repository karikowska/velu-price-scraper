import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"


def get_search_results(query: str, limit=5) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(f"https://solarisjapan.com/search/?query={query}")
        page.wait_for_selector(".ais-Hits-item")
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

        items = soup.select(".ais-Hits-item")
        results = []
        
        for item in items[:limit]:
            url = "https://solarisjapan.com/" + item.select_one("a")["href"]
            
            title_tag = item.select_one("h3")
            title = title_tag.get_text(strip=True) if title_tag else None
            
            # price_tags = item.select_one('.product__labels-wrapper.tw-w-full')
            # price = None
            # print(price_tags)
            # for price_tag in price_tags.select('div'):
            #     class_name = price_tag.get("class", [])
            #     print(class_name)
            #     if 'product-label--sold-out' not in class_name:
            #         if 'product-label--brand-new' in class_name:
            #             price = price_tag.select_one('span.money')
            #             if price_tag:
            #                 price = price_tag.text.strip()
            #         elif 'product-label--pre-owned' in class_name:
            #             price = price_tag.select_one('span.money')
            #             if price_tag:
            #                 price = price_tag.text.strip()
            #         else:
            #             price = "£20"

            if not (title and url):
                continue

            results.append({
                "title": title,
                "url": url
            })

        return results
