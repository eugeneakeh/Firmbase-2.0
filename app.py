import streamlit as st
import pandas as pd
from engine.scoring import calculate_business_health

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Firmbase AI",
    layout="wide"
)

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def calculate_profit(revenue, expenses):
    return revenue - expenses


def calculate_profit_margin(profit, revenue):
    if revenue == 0:
        return 0
    return (profit / revenue) * 100


def create_summary_df(data: dict):
    return pd.DataFrame(list(data.items()), columns=["Metric", "Value"])


def get_score_color(score):
    if score >= 80:
        return "green"
    elif score >= 50:
        return "orange"
    else:
        return "red"


def colored_metric(label, value):
    color = get_score_color(value)
    st.markdown(
        f"""
        <div style="
            padding:10px;
            border-radius:10px;
            background-color:{color};
            color:white;
            text-align:center;
            font-weight:bold;">
            {label}<br>{value}
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------
# UI - TITLE
# -------------------------------
st.title("📊 Firmbase AI - Business Health Dashboard")
st.markdown("---")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("📥 Business Inputs")

revenue = st.sidebar.number_input("Revenue", min_value=0.0, value=0.0)
expenses = st.sidebar.number_input("Expenses", min_value=0.0, value=0.0)
cash_flow = st.sidebar.number_input("Cash Flow", value=0.0)
inventory = st.sidebar.number_input("Inventory Value", min_value=0.0, value=0.0)
staff_cost = st.sidebar.number_input("Staff Cost", min_value=0.0, value=0.0)
debt = st.sidebar.number_input("Loans / Debt", min_value=0.0, value=0.0)

analyze_btn = st.sidebar.button("🚀 Analyze Business")

# -------------------------------
# MAIN LAYOUT
# -------------------------------
col1, col2 = st.columns(2)

# -------------------------------
# INPUT SUMMARY
# -------------------------------
with col1:
    st.subheader("📋 Input Summary")

    input_data = {
        "Revenue": revenue,
        "Expenses": expenses,
        "Cash Flow": cash_flow,
        "Inventory": inventory,
        "Staff Cost": staff_cost,
        "Debt": debt,
    }

    df_summary = create_summary_df(input_data)
    st.dataframe(df_summary, use_container_width=True)

# -------------------------------
# RESULTS SECTION
# -------------------------------
with col2:
    st.subheader("📈 Results")

    if analyze_btn:
        # Basic calculations
        profit = calculate_profit(revenue, expenses)
        profit_margin = calculate_profit_margin(profit, revenue)

        st.metric("💰 Profit", f"{profit:,.2f}")
        st.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

        st.markdown("### 🧠 Business Health Analysis")

        # Prepare data for engine
        engine_input = {
            "revenue": revenue,
            "expenses": expenses,
            "cash_flow": cash_flow,
            "debt": debt
        }

        results = calculate_business_health(engine_input)

        # BIG Health Score
        st.markdown("#### ⭐ Overall Health Score")
        colored_metric("Health Score", results["health_score"])

        st.markdown("#### 📊 Component Scores")

        c1, c2 = st.columns(2)

        with c1:
            colored_metric("Profitability", results["profitability_score"])
            colored_metric("Cash Flow", results["cash_score"])

        with c2:
            colored_metric("Debt", results["debt_score"])
            colored_metric("Growth", results["growth_score"])

        st.success("Analysis complete ✅")

    else:
        st.info("Click 'Analyze Business' to see results.")
