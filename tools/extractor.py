from langchain.tools import tool
from helpers.scraper import get_html, get_text_snippets
from llms.price_extractor import extract_price_info

@tool
def extract_price_from_html(url: str) -> dict:
    """Extracts the price from a given URL using HTML scraping and LLM."""
    url = url.strip().strip("'").strip('"')
    html = get_html(url)
    snippet = get_text_snippets(html)

    if not snippet.strip():
        return {"amount": None, "currency": "UNKNOWN", "note": "No content found"}

    inferred_query = "product"
    result = extract_price_info(inferred_query, url, snippet)

    raw_price = result["price"]
    if "¥" in raw_price:
        amount = float(raw_price.replace("¥", "").replace(",", "").strip())
        currency = "JPY"
    elif "$" in raw_price:
        amount = float(raw_price.replace("$", "").replace(",", "").strip())
        currency = "USD"
    else:
        amount = None
        currency = "UNKNOWN"

    return {"amount": amount, "currency": currency}


