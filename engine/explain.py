# engine/explain.py

def generate_explanation(data: dict, scores: dict):
    """
    Generate a human-like explanation of business performance.
    """

    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    cash_flow = data.get("cash_flow", 0)
    debt = data.get("debt", 0)

    health_score = scores.get("health_score", 0)

    # -------------------------------
    # CORE METRICS
    # -------------------------------
    profit = revenue - expenses
    debt_ratio = debt / revenue if revenue > 0 else 0

    explanation_parts = []

    # -------------------------------
    # PROFIT ANALYSIS
    # -------------------------------
    if profit > 0:
        explanation_parts.append(
            "Your business is currently profitable, meaning your revenue exceeds your expenses."
        )
    elif profit == 0:
        explanation_parts.append(
            "Your business is breaking even, with revenue matching expenses."
        )
    else:
        explanation_parts.append(
            "Your business is operating at a loss, as expenses exceed revenue."
        )

    # -------------------------------
    # CASH FLOW ANALYSIS
    # -------------------------------
    if cash_flow > 0:
        explanation_parts.append(
            "Cash flow is positive, which means your business is generating enough cash to sustain operations."
        )
    elif cash_flow == 0:
        explanation_parts.append(
            "Cash flow is neutral, indicating tight cash management with little buffer."
        )
    else:
        explanation_parts.append(
            "Cash flow is negative, which may lead to liquidity issues if not addressed."
        )

    # -------------------------------
    # DEBT ANALYSIS
    # -------------------------------
    if debt_ratio < 0.3:
        explanation_parts.append(
            "Debt levels are relatively low and manageable."
        )
    elif debt_ratio < 0.6:
        explanation_parts.append(
            "Debt is at a moderate level and should be managed carefully."
        )
    else:
        explanation_parts.append(
            "Debt levels are high relative to revenue, which increases financial risk."
        )

    # -------------------------------
    # HEALTH SCORE INTERPRETATION
    # -------------------------------
    if health_score >= 80:
        explanation_parts.append(
            f"Overall, your business is in strong condition with a health score of {health_score}, indicating stability and good growth potential."
        )
    elif health_score >= 50:
        explanation_parts.append(
            f"Your business is moderately stable with a health score of {health_score}, but there are areas that need improvement."
        )
    else:
        explanation_parts.append(
            f"Your business is currently at risk with a health score of {health_score}, and immediate attention is needed to improve performance."
        )

    # -------------------------------
    # COMBINE INTO PARAGRAPH
    # -------------------------------
    explanation = " ".join(explanation_parts)

    return explanation
