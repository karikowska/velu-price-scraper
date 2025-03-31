import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_google(site: str, query: str, limit=5) -> list:
    search_url = f"https://www.google.com/search?q=site:{site}+{quote_plus(query)}"
    res = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for g in soup.select("div.g")[:limit]:
        a_tag = g.select_one("a")
        if a_tag:
            link = a_tag["href"]
            title = a_tag.get_text()
            links.append({"title": title, "url": link})

    print(links)
    return links
