"""Uses LLM to extract the price of a product from HTML snippets."""
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import re

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def extract_price_info(product_name: str, url: str, html_snippet: str) -> dict:
    messages = [
        SystemMessage(content=(
            "You are a very helpful assistant that extracts the relevant product's price from HTML."
            "If the currency is not in JPY (¥), you have to convert it to JPY (¥) using the current exchange rate and output the final price."
        )),
        HumanMessage(content=(
            f"Product: {product_name}\n"
            f"URL: {url}\n"
            f"HTML snippet:\n{html_snippet}\n\n"
            "From this HTML, what is the JPY (¥) price?"
        ))
    ]

    response = llm.invoke(messages)
    
    price_match = re.search(r"([\$£€¥]\s?\d+[.,]?\d*)", response.content)
    extracted_price = price_match.group(1).replace(" ", "") if price_match else "N/A"

    return {
        "product": product_name,
        "price": extracted_price,
        "raw_response": response.content
    }
