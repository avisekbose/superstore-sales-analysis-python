import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")

st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive analysis of Sales and profit performance")

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore Sales/superstore_eda_V1-1724655032.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format = "mixed", errors= "coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format = "mixed", errors= "coerce")
    return df

df = load_data()

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ---------------------------
# KPIs
# ---------------------------
total_Sales = filtered_df["Sales Price"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales Price", f"${total_Sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Total Orders", total_orders)

st.divider()

# ---------------------------
# Sales Price by Category
# ---------------------------
st.subheader("Sales by Category")

Sales_by_category = (
    filtered_df
    .groupby("Category")["Sales Price"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots()
Sales_by_category.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Sales")
ax1.set_xlabel("Category")

st.pyplot(fig1)

# ---------------------------
# Profit by Region
# ---------------------------
st.subheader("Profit by Region")

profit_by_region = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()
profit_by_region.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Profit")
ax2.set_xlabel("Region")

st.pyplot(fig2)

# ---------------------------
# Monthly Sales Price Trend
# ---------------------------
st.subheader("Monthly Sales Trend")

monthly_Sales = (
    filtered_df
    .set_index("Order Date")
    .resample("ME")["Sales Price"]
    .sum()
)

fig3, ax3 = plt.subplots()
monthly_Sales.plot(ax=ax3)
ax3.set_ylabel("Sales Price")
ax3.set_xlabel("Month")

st.pyplot(fig3)

# ---------------------------
# Raw data (optional)
# ---------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)