import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FAKE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# !!!IMPORTANT!!! - this doesn't work - AmiAmi uses cloudflare! Needs a fix :)
def get_search_results(query: str, limit=5) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent=FAKE_UA)
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(f"https://www.amiami.com/eng/search/list/?s_keywords={(query)}")
        page.wait_for_selector(".new-items__inner")
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        items = soup.select(".newly-added-items__item")
        if not items:
            print("No matching HTML blocks. The site may have changed layout.")
            return []

        results = []
        for item in items[:limit]:
            stock_tags = item.select_one('.newly-added-items__item__tag-list')
            stock_status = next((
                tag.text.strip()
                for tag in stock_tags
                if tag.get('style') != 'display: none;'
            ), 'Unknown')

            if stock_status == 'Unknown':
                continue
            elif stock_status == 'Order Closed':
                continue
            
            url = "https://www.amiami.com" + item.select_one('a')['href']
            
            title_tag = item.select_one('.newly-added-items__item__name')
            title = title_tag.text.strip() if title_tag else 'N/A'

            if not (title and url):
                continue

            results.append({
                "title": title,
                "url": url,
            })
            
        
        return results
