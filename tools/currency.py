from langchain.tools import tool

@tool
def convert_currency(input: str) -> str:
    """
    Converts a string like "53.54, USD, JPY" to a float in JPY.
    """
    try:
        clean_input = input.strip().strip('"').strip("'")
        amount_str, from_cur, to_cur = [s.strip() for s in clean_input.split(",")]

        amount = float(amount_str)
        rates = {
            ("USD", "JPY"): 150,
            ("EUR", "JPY"): 160,
            ("GBP", "JPY"): 180,
            ("JPY", "JPY"): 1,
        }
        rate = rates.get((from_cur.upper(), to_cur.upper()))
        if not rate:
            return "Unsupported currency conversion"
        return str(round(amount * rate))
    except Exception as e:
        return f"Error: {e}"
