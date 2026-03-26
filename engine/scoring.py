# engine/scoring.py

def clamp_score(value, min_value=0, max_value=100):
    """Ensure score stays within 0–100 range."""
    return max(min_value, min(max_value, int(value)))


# -------------------------------
# PROFITABILITY SCORE (30%)
# -------------------------------
def profitability_score(revenue, expenses):
    if revenue == 0:
        return 0

    profit_margin = (revenue - expenses) / revenue

    if profit_margin >= 0.3:
        score = 100
    elif profit_margin >= 0.2:
        score = 80
    elif profit_margin >= 0.1:
        score = 60
    elif profit_margin > 0:
        score = 40
    else:
        score = 10  # negative profit

    return clamp_score(score)


# -------------------------------
# CASH FLOW SCORE (25%)
# -------------------------------
def cash_flow_score(cash_flow, revenue):
    if revenue == 0:
        return 0

    ratio = cash_flow / revenue

    if ratio >= 0.2:
        score = 100
    elif ratio >= 0.1:
        score = 80
    elif ratio >= 0.05:
        score = 60
    elif ratio > 0:
        score = 40
    else:
        score = 10  # negative cash flow

    return clamp_score(score)


# -------------------------------
# DEBT SCORE (20%)
# -------------------------------
def debt_score(debt, revenue):
    if revenue == 0:
        return 50  # neutral if no revenue

    ratio = debt / revenue

    if ratio <= 0.2:
        score = 100
    elif ratio <= 0.4:
        score = 80
    elif ratio <= 0.6:
        score = 60
    elif ratio <= 1.0:
        score = 40
    else:
        score = 20  # too much debt

    return clamp_score(score)


# -------------------------------
# GROWTH SCORE (25%)
# -------------------------------
def growth_score(revenue, expenses):
    """
    Proxy growth logic:
    If revenue significantly exceeds expenses → growth potential.
    """

    if revenue == 0:
        return 0

    ratio = (revenue - expenses) / revenue

    if ratio >= 0.25:
        score = 100
    elif ratio >= 0.15:
        score = 80
    elif ratio >= 0.05:
        score = 60
    elif ratio > 0:
        score = 40
    else:
        score = 20  # declining business

    return clamp_score(score)


# -------------------------------
# FINAL HEALTH SCORE
# -------------------------------
def calculate_business_health(data: dict):
    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    cash_flow = data.get("cash_flow", 0)
    debt = data.get("debt", 0)

    p_score = profitability_score(revenue, expenses)
    c_score = cash_flow_score(cash_flow, revenue)
    d_score = debt_score(debt, revenue)
    g_score = growth_score(revenue, expenses)

    # Weighted score
    health_score = (
        p_score * 0.30 +
        c_score * 0.25 +
        d_score * 0.20 +
        g_score * 0.25
    )

    return {
        "health_score": clamp_score(health_score),
        "profitability_score": p_score,
        "cash_score": c_score,
        "debt_score": d_score,
        "growth_score": g_score
    }
