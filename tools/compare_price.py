from langchain.tools import tool

import ast

@tool
def compare_prices(input: str) -> str:
    """
    Expects input like "[4210, 5000]".
    Returns whether price is under or over budget.
    """
    try:
        price_budget = ast.literal_eval(input)
        price, budget = price_budget
        return "UNDER BUDGET" if price <= budget else "OVER BUDGET"
    except Exception as e:
        return f"ERROR: {str(e)}"
