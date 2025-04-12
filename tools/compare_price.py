from langchain.tools import tool

@tool
def compare_prices(price: int, budget: int) -> str:
    """
    Compares a price to a budget.
    Returns 'UNDER BUDGET' if price <= budget, otherwise 'OVER BUDGET'.
    Example: compare_prices(price=4500, budget=40000)
    """
    if price <= budget:
        return "UNDER BUDGET"
    else:
        return "OVER BUDGET"
