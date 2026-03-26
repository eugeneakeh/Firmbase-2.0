# engine/metrics.py

from utils.helpers import safe_divide, calculate_ratio

def calculate_profit(revenue: float, expenses: float) -> float:
    """
    Calculate net profit.
    """
    return revenue - expenses


def profit_margin(revenue: float, expenses: float) -> float:
    """
    Return profit margin as a ratio (0–1)
    """
    profit = calculate_profit(revenue, expenses)
    return safe_divide(profit, revenue)


def cash_flow_ratio(cash_flow: float, revenue: float) -> float:
    """
    How much of revenue is actual cash flow.
    """
    return safe_divide(cash_flow, revenue)


def debt_ratio(debt: float, revenue: float) -> float:
    """
    Debt compared to revenue
    """
    return safe_divide(debt, revenue)


def burn_rate(expenses: float, revenue: float) -> float:
    """
    Rate at which the business is losing money.
    Returns 0 if profitable.
    """
    if expenses <= revenue:
        return 0
    return expenses - revenue


def runway(cash_flow: float, expenses: float) -> float:
    """
    Estimate months the business can survive with current cash flow.
    """
    if expenses <= 0:
        return float("inf")
    return safe_divide(cash_flow, expenses) * 12  # in months


def calculate_all_metrics(revenue: float, expenses: float, cash_flow: float, debt: float) -> dict:
    """
    Return all key metrics as a dictionary
    """
    metrics = {
        "profit": calculate_profit(revenue, expenses),
        "profit_margin": profit_margin(revenue, expenses),
        "cash_flow_ratio": cash_flow_ratio(cash_flow, revenue),
        "debt_ratio": debt_ratio(debt, revenue),
        "burn_rate": burn_rate(expenses, revenue),
        "runway": runway(cash_flow, expenses)
    }
    return metrics
