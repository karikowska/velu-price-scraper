"""Runs agent that uses tools to scrape sites and serve results below budget in wishlist."""
import yaml
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from tools.site_tools import (
    search_amiami,
    search_solaris,
    search_ninningame,
    search_animota,
    search_gsce,
    search_japanfigure
)

from tools.extractor import extract_price_from_html
from tools.compare_price import compare_prices
from tools.currency import convert_currency
from helpers.other_helpers import prepare_agent_for_product

tools = [
    search_amiami,
    search_solaris,
    search_ninningame,
    search_animota,
    search_gsce,
    search_japanfigure,
    extract_price_from_html,
    compare_prices,
    convert_currency,
]

# load wishlist from yaml
def load_wishlist(path="config/wishlist.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
# load llm
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

wishlist = load_wishlist()
def run_langchain_agent():
    for product in wishlist:
        selected_tools, prompt = prepare_agent_for_product(product, all_tools=tools)

        agent = initialize_agent(
            tools=selected_tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True,
        )

        agent.run(prompt)

if __name__ == "__main__":
    run_langchain_agent()