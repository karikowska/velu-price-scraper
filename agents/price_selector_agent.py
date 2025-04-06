# UNUSED FOR NOW!!!
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import json

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def pick_best_listing(query: str, listings: list) -> dict:
    message = [
        SystemMessage(content="You're an expert shopper comparing listings. Choose the best match."),
        HumanMessage(content=(
            f"I'm searching for: {query}\n\n"
            f"Here are the listings:\n{json.dumps(listings, indent=2)}\n\n"
            "Pick the best one (cheapest and most relevant) and return its title, price, and URL."
        ))
    ]
    response = llm.invoke(message)
    return {"raw": response.content}
