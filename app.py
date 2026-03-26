import streamlit as st
import pandas as pd
from engine.scoring import calculate_business_health
from engine.recommendations import generate_recommendations
from engine.explain import generate_explanation
from engine.simulator import simulate_scenario

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
            padding:12px;
            border-radius:12px;
            background-color:{color};
            color:white;
            text-align:center;
            font-weight:bold;">
            {label}<br>{value}
        </div>
        """,
        unsafe_allow_html=True
    )


def recommendation_card(text):
    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:10px;
            background-color:#f5f5f5;
            border-left:5px solid #4CAF50;
            margin-bottom:8px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def explanation_box(text):
    st.markdown(
        f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background-color:#eef2f7;
            border-left:5px solid #2b6cb0;
            line-height:1.6;">
            {text}
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
        "revenue": revenue,
        "expenses": expenses,
        "cash_flow": cash_flow,
        "debt": debt
    }

    df_summary = create_summary_df(input_data)
    st.dataframe(df_summary, use_container_width=True)

# -------------------------------
# RESULTS + INSIGHTS
# -------------------------------
with col2:
    st.subheader("📈 Results")

    if analyze_btn:
        profit = calculate_profit(revenue, expenses)
        profit_margin = calculate_profit_margin(profit, revenue)

        st.metric("💰 Profit", f"{profit:,.2f}")
        st.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

        st.markdown("### 🧠 Business Health Analysis")

        results = calculate_business_health(input_data)

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

        # -------------------------------
        # RECOMMENDATIONS
        # -------------------------------
        st.markdown("### 📌 Recommendations")
        recommendations = generate_recommendations(input_data, results)

        for rec in recommendations:
            recommendation_card(f"✔ {rec}")

        # -------------------------------
        # EXPLANATION
        # -------------------------------
        st.markdown("### 🧾 Explanation")
        explanation = generate_explanation(input_data, results)
        explanation_box(explanation)

        # -------------------------------
        # SCENARIO SIMULATOR
        # -------------------------------
        st.markdown("### 🔮 Scenario Simulator")

        sim_col1, sim_col2 = st.columns(2)

        with sim_col1:
            rev_delta = st.number_input("Change in Revenue", value=0.0)
            exp_delta = st.number_input("Change in Expenses", value=0.0)

        with sim_col2:
            cash_delta = st.number_input("Change in Cash Flow", value=0.0)
            debt_delta = st.number_input("Change in Debt", value=0.0)

        simulate_btn = st.button("Run Simulation")

        if simulate_btn:
            changes = {
                "revenue_delta": rev_delta,
                "expenses_delta": exp_delta,
                "cash_flow_delta": cash_delta,
                "debt_delta": debt_delta
            }

            sim_result = simulate_scenario(input_data, changes)
            new_scores = sim_result["new_scores"]

            st.markdown("#### 🔁 Simulation Results")

            before = results["health_score"]
            after = new_scores["health_score"]
            diff = after - before

            # Highlight improvement/decline
            if diff > 0:
                st.success(f"Health Score Improved by +{diff}")
            elif diff < 0:
                st.error(f"Health Score Dropped by {diff}")
            else:
                st.info("No change in Health Score")

            # Comparison
            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**Before**")
                colored_metric("Health Score", before)

            with c2:
                st.markdown("**After**")
                colored_metric("Health Score", after)

            st.markdown("#### 📊 New Component Scores")

            c3, c4 = st.columns(2)

            with c3:
                colored_metric("Profitability", new_scores["profitability_score"])
                colored_metric("Cash Flow", new_scores["cash_score"])

            with c4:
                colored_metric("Debt", new_scores["debt_score"])
                colored_metric("Growth", new_scores["growth_score"])

        st.success("Analysis complete ✅")

    else:
        st.info("Click 'Analyze Business' to see results.")
