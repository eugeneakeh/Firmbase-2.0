# engine/recommendations.py

def generate_recommendations(data: dict, scores: dict):
    """
    Generate actionable business recommendations
    based on financial data and scoring output.
    """

    revenue = data.get("revenue", 0)
    expenses = data.get("expenses", 0)
    cash_flow = data.get("cash_flow", 0)
    debt = data.get("debt", 0)

    health_score = scores.get("health_score", 0)

    recommendations = []

    # -------------------------------
    # CORE METRICS
    # -------------------------------
    profit = revenue - expenses
    debt_ratio = debt / revenue if revenue > 0 else 0

    # -------------------------------
    # PROFITABILITY RULES
    # -------------------------------
    if profit < 0:
        recommendations.append(
            "Reduce expenses immediately — your business is operating at a loss."
        )
        recommendations.append(
            "Review pricing strategy or increase revenue streams to restore profitability."
        )

    elif profit > 0 and profit / revenue < 0.1:
        recommendations.append(
            "Your profit margin is low — consider reducing operational costs or increasing prices."
        )

    # -------------------------------
    # CASH FLOW RULES
    # -------------------------------
    if cash_flow < 0:
        recommendations.append(
            "Improve cash flow management — delay non-essential spending and accelerate receivables."
        )
        recommendations.append(
            "Ensure customers pay faster and reduce unnecessary inventory buildup."
        )

    elif cash_flow > 0 and cash_flow / revenue < 0.05:
        recommendations.append(
            "Cash flow is weak — monitor inflows and outflows more closely."
        )

    # -------------------------------
    # DEBT RULES
    # -------------------------------
    if debt_ratio > 0.6:
        recommendations.append(
            "Debt level is high — avoid taking additional loans and focus on repayment."
        )

    elif debt_ratio > 0.3:
        recommendations.append(
            "Manage debt carefully — ensure repayments do not strain your cash flow."
        )

    # -------------------------------
    # HEALTH SCORE RULES
    # -------------------------------
    if health_score < 50:
        recommendations.append(
            "Business is at risk — consider restructuring operations and cutting unnecessary costs."
        )
        recommendations.append(
            "Focus on stabilizing revenue and improving cash flow before expansion."
        )

    elif 50 <= health_score < 80:
        recommendations.append(
            "Business is moderately stable — optimize operations and improve efficiency."
        )

    elif health_score >= 80:
        recommendations.append(
            "Business is strong — consider expansion, hiring, or reinvesting profits."
        )

    # -------------------------------
    # GENERAL SMART SUGGESTIONS
    # -------------------------------
    if revenue == 0:
        recommendations.append(
            "No revenue detected — prioritize customer acquisition and sales generation."
        )

    if expenses > revenue:
        recommendations.append(
            "Expenses exceed revenue — conduct a cost audit to identify waste."
        )

    # -------------------------------
    # ENSURE MINIMUM OUTPUT (3–5)
    # -------------------------------
    if len(recommendations) < 3:
        recommendations.append(
            "Monitor your financial metrics regularly to maintain business health."
        )
        recommendations.append(
            "Track key performance indicators and adjust strategy as needed."
        )

    return recommendations
