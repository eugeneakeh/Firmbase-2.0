# risk.py

def calculate_risk_level(data, scores):
    """
    Calculate the risk level of a business based on financial and health metrics.

    Parameters:
        data (dict): Financial data with keys:
            - profit (float)
            - cash_flow (float)
            - debt_ratio (float, 0 to 1)
        scores (dict): Health and performance metrics with keys:
            - health_score (float, 0 to 100)
            - margin (float, 0 to 1)

    Returns:
        dict: {
            "risk_level": "Low" | "Medium" | "High",
            "reasons": [list of strings explaining the risk]
        }
    """
    reasons = []

    profit = data.get("profit", 0)
    cash_flow = data.get("cash_flow", 0)
    debt_ratio = data.get("debt_ratio", 0)
    health_score = scores.get("health_score", 100)
    margin = scores.get("margin", 0.3)  # default moderate margin

    # HIGH risk conditions
    if profit < 0:
        reasons.append(f"Profit is negative ({profit}), indicating potential losses.")
    if cash_flow < 0:
        reasons.append(f"Cash flow is negative ({cash_flow}), signaling liquidity issues.")
    if debt_ratio > 0.6:
        reasons.append(f"Debt ratio is high ({debt_ratio:.2f}), which increases financial leverage risk.")
    if health_score < 50:
        reasons.append(f"Health score is low ({health_score}), suggesting operational or financial weaknesses.")

    # Determine risk level
    if reasons:
        risk_level = "High"
        return {"risk_level": risk_level, "reasons": reasons}

    # MEDIUM risk conditions
    medium_reasons = []
    if 0.4 < debt_ratio <= 0.6:
        medium_reasons.append(f"Debt ratio is moderate ({debt_ratio:.2f}), may increase risk under stress.")
    if 0 < margin < 0.1:
        medium_reasons.append(f"Margins are low ({margin:.2f}), limiting buffer against losses.")
    if 0 <= cash_flow < 10000:  # arbitrary low cash flow threshold
        medium_reasons.append(f"Cash flow is weak ({cash_flow}), may impact short-term operations.")
    
    if medium_reasons:
        risk_level = "Medium"
        return {"risk_level": risk_level, "reasons": medium_reasons}

    # LOW risk conditions
    low_reasons = []
    low_reasons.append(f"Profit is strong ({profit}).")
    low_reasons.append(f"Cash flow is positive ({cash_flow}).")
    low_reasons.append(f"Debt ratio is low ({debt_ratio:.2f}).")
    low_reasons.append(f"Health score is high ({health_score}).")
    
    risk_level = "Low"
    return {"risk_level": risk_level, "reasons": low_reasons}


# Example usage
if __name__ == "__main__":
    data = {"profit": 50000, "cash_flow": 20000, "debt_ratio": 0.3}
    scores = {"health_score": 85, "margin": 0.15}

    result = calculate_risk_level(data, scores)
    print(result)
