# utils/helpers.py

def safe_divide(a, b):
    """
    Safely divide two numbers.
    Returns 0 if denominator is 0.
    """
    try:
        return a / b if b != 0 else 0
    except Exception:
        return 0


def format_currency(value):
    """
    Format a number as currency string.
    Example: 12000 -> '12,000.00'
    """
    try:
        return f"{value:,.2f}"
    except Exception:
        return "0.00"


def format_percentage(value):
    """
    Format a number as percentage string.
    Example: 0.255 -> '25.50%'
    """
    try:
        return f"{value * 100:.2f}%"
    except Exception:
        return "0.00%"


def clamp(value, min_val=0, max_val=100):
    """
    Restrict a value within a given range.
    """
    try:
        return max(min_val, min(max_val, value))
    except Exception:
        return min_val


def calculate_ratio(part, whole):
    """
    Calculate ratio safely using safe_divide.
    """
    return safe_divide(part, whole)
