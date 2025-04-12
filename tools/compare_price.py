from langchain.tools import tool

@tool
def compare_prices(price: int, budget: int) -> str:
    """
    Compares a price to a budget.
    Returns 'UNDER BUDGET' if price over budget, otherwise 'OVER BUDGET'.
    """
    if price <= budget:
        return "UNDER BUDGET"
    else:
        return "OVER BUDGET"
