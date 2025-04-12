from query_search.amiami_search import get_search_results as amiami_search
from query_search.solaris_search import get_search_results as solaris_search
from query_search.ninningame_search import get_search_results as ninningame_search
from query_search.animota_search import get_search_results as animota_search
from query_search.goodsmileeurope_search import get_search_results as goodsmileeurope_search
from query_search.japan_figure_search import get_search_results as japanfigure_search
import yaml

def shop_check(query: str, site: str):
    if site == 'anim':
        links = animota_search(query)
    elif site == 'sol':
        links = solaris_search(query)
    elif site == 'aa':
        links = amiami_search(query)
    elif site == 'nng':
        links = ninningame_search(query)
    elif site == 'jf':
        links = japanfigure_search(query)
    elif site == 'gsce':
        links = goodsmileeurope_search(query)
        
    return links


def prepare_agent_for_product(product: dict, all_tools: list, config: dict) -> tuple[list, str]:
    name = product["name"]
    budget = product["max_price"]
    site_names = product.get("sites") or config.get("allowed_sites", [])

    selected_tools = [
        tool for tool in all_tools
        if tool.name in site_names or tool.name == "extract_price_from_html"
    ]

    # Generate prompt
    prompt = f"""
        You are a price-checking assistant. Your task is to search for '{name}' using the available tools,
        compare prices, and notify the user only if a deal is found under ¥{budget}.

        Steps:
        1. Use ONLY these search tools: {', '.join(site_names)}.
        2. For each result URL returned by these tools, call extract_price_from_html(url).
        3. Collect all prices and URLs.
        4. Collect all listings where compare_prices(price, budget) returns 'UNDER BUDGET'.
        5. From those, select the listing with the lowest price.
        6. If there are listings under budget:
            - Pick the one with the lowest price
            - Return: "Found {{name}} at ¥{{price}} from {{site}}: {{url}}"
            
        Example:  
            If extract_price_from_html(url) returned 14200, and the site is AmiAmi, return:  
            "Found {{name}} at ¥14200 from AmiAmi: https://amiami.com/product/FIGURE-123"

        7. If no listings are under budget:
            - Pick the cheapest one overall
            - Return: "{{name}} is not available under ¥{{budget}}, but the cheapest available is ¥{{price}} from {{site}}: {{url}}"
            
        Example:
            If your price results are:
            - AmiAmi: ¥5100
            - Solaris: ¥5300
            - Ninningame: ¥4800

            And the budget is ¥4500, return:
            "{{name}} is not available under ¥4500, but the cheapest available is ¥4800 from Ninningame: {{url}}"
            
        8. If no listings are found on any website:
            - Return: "{{name}} is not available under ¥{{budget}}."

        Important:
        - Always extract and store (site, url, price) triples
        - Do not invent prices or sites
        - Reuse the real values returned by extract_price_from_html(url)

        Return your result as the final answer. Do not call any tool to report it. Never use brackets like <url> or <price> — always use real values from tool results.
        Important: NEVER guess whether a price is under or over budget. Always use compare_prices(price, budget) to make this decision. Keep a running list of all (site, url, price) triples you extract.
        Only compare listings that are under budget."""

    return selected_tools, prompt

# Load wishlist + config
def load_config():
    with open("config/wishlist.yaml", "r") as f:
        return yaml.safe_load(f)