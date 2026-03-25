import streamlit as st
import pandas as pd

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
# INPUT SUMMARY SECTION
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
        profit = calculate_profit(revenue, expenses)
        profit_margin = calculate_profit_margin(profit, revenue)

        st.metric(label="💰 Profit", value=f"{profit:,.2f}")
        st.metric(label="📊 Profit Margin (%)", value=f"{profit_margin:.2f}%")

        st.success("Analysis complete ✅")

    else:
        st.info("Click 'Analyze Business' to see results.")
