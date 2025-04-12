from langchain.tools import tool
from helpers.scraper import get_html, get_text_snippets
from llms.price_extractor import extract_price_info

@tool
def extract_price_from_html(url: str) -> str:
    """
    Extracts a price (as a string) from the given product URL using LLM-based snippet parsing.
    """
    print(f"[🔍] Extracting price from: {url}")
    
    html = get_html(url)
    snippet = get_text_snippets(html)

    if not snippet.strip():
        print("No content found in snippet.")
        return "NO_PRICE_FOUND"

    fake_query = "product"
    result = extract_price_info(fake_query, url, snippet)

    print(f"[💸] Extracted: {result['price']} | Raw: {result['raw_response']}")
    return result["price"]

