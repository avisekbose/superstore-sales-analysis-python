import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")
sns.set_theme(style="whitegrid")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore Sales/superstore_eda_V7.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])
    return df

df = load_data()

# Sidebar
st.sidebar.info("📁 Dataset: Superstore Sales")
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect("Select Region", df["Region"].unique(), df["Region"].unique())
segment = st.sidebar.multiselect("Select Segment", df["Segment"].unique(), df["Segment"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique(), df["Category"].unique())
sub_category = st.sidebar.multiselect("Select Sub-Category", df["Sub-Category"].unique(), df["Sub-Category"].unique())

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
].copy()

# KPIs
st.subheader("📊 Key Metrics")
total_sales = filtered_df["Sales Price"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🧾 Total Orders", total_orders)

st.divider()

# Sales by Category
st.subheader("Sales by Category")
sales_by_category = filtered_df.groupby("Category")["Sales Price"].sum().sort_values()

fig, ax = plt.subplots(figsize=(5, 3))
sales_by_category.plot(kind="bar", ax=ax)
st.pyplot(fig)

# Profit by Region
st.subheader("Profit by Region")
profit_by_region = filtered_df.groupby("Region")["Profit"].sum().sort_values()

fig, ax = plt.subplots(figsize=(5, 3))
profit_by_region.plot(kind="bar", ax=ax)
st.pyplot(fig)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.set_index("Order Date").resample("M")["Sales Price"].sum()

fig, ax = plt.subplots(figsize=(6, 3))
monthly_sales.plot(ax=ax)
st.pyplot(fig)

# Product Metrics
product_metrics = filtered_df.groupby("Product Name").agg(
    Total_Sales=("Sales Price", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

# Scatter Plot
st.subheader("Sales vs Profit by Product")
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(product_metrics["Total_Sales"], product_metrics["Total_Profit"], alpha=0.6)

coeffs = np.polyfit(product_metrics["Total_Sales"], product_metrics["Total_Profit"], 1)
reg_line = np.poly1d(coeffs)
ax.plot(product_metrics["Total_Sales"], reg_line(product_metrics["Total_Sales"]), color="red")

st.pyplot(fig)

# Raw Data 
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)