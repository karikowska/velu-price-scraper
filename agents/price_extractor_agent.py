from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import re

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def extract_price_info(product_name: str, url: str, html_snippet: str) -> dict:
    messages = [
        SystemMessage(content=(
            "You are an assistant that extracts product prices from provided HTML snippets. "
            "You are NOT expected to access URLs or browse the web. "
            "Just analyze the HTML text passed in and extract the price and currency if possible."
            "Make sure to convert the price to GBP according to today's exchange rate."
        )),
        HumanMessage(content=(
            f"Product: {product_name}\n"
            f"URL: {url}\n"
            f"HTML snippet:\n{html_snippet}\n\n"
            "From this HTML, what is the price and currency?"
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
