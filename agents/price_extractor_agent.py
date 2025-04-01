from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import re

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def extract_price_info(product_name: str, url: str, html_snippet: str) -> dict:
    messages = [
        SystemMessage(content=(
            "You are an amazingly helpful assistant that extracts product prices from provided HTML snippets."
            "If the currency is in USD ($) or JPY (¥), you have to convert it to GBP (£) using the current exchange rate and output the final price. Please do not show your calculations, just output the final price in GBP."
            "If the product name contains 'plush' or other object name that is not part of the figure name, make it clear that it is NOT a figure."
        )),
        HumanMessage(content=(
            f"Product: {product_name}\n"
            f"URL: {url}\n"
            f"HTML snippet:\n{html_snippet}\n\n"
            "Is this a figure listing, or something else? From this HTML, what is the GBP price?"
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
