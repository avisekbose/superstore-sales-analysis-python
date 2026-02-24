import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")
st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive analysis of Sales and profit performance")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore Sales/superstore_eda_V7.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format = "mixed", errors= "coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format = "mixed", errors= "coerce")
    return df

df = load_data()

# Dataset name in sidebar
st.sidebar.info("📁 Dataset: Superstore Sales")

# Dataset Overview
st.subheader("📂 Dataset Overview")
total_rows = df.shape[0]
total_cols = df.shape[1]
st.markdown(f"""
This dataset contains **{total_rows:,} rows** and **{total_cols} columns**  
covering sales transactions, customers, products, and performance metrics.
""")
st.divider()

# Display column names and descriptions
st.subheader("📊 Summary Statistics")
selected_cols = ["Sales Price", "Quantity", "Discount", "Profit"]
summary = df[selected_cols].describe().T
st.dataframe(summary)

# Sidebar filters
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

st.divider()

# KPIs
total_Sales = filtered_df["Sales Price"].sum()
total_profit = filtered_df["Profit"].sum()
total_discount = filtered_df["Discount"].sum()
total_orders = filtered_df["Order ID"].nunique()
col1, col2, col3 = st.columns(3)
col1.metric("**💰 Total Sales Price**", f"${total_Sales:,.0f}")
col2.metric("**📈 Total Profit**", f"${total_profit:,.0f}")
col3.metric("**🧾 Total Orders**", total_orders)

st.divider()

# Sales Price by Category
st.subheader("Sales by Category")
st.write("The chart shows the distribution of sales across different categories based on the applied filters.\nTechnology consistently generates the highest sales, followed by Furniture and Office Supplies.")

Sales_by_category = (filtered_df.groupby("Category")["Sales Price"].sum().sort_values(ascending=False))
fig1, ax1 = plt.subplots(figsize=(5, 3))
Sales_by_category.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Sales", fontsize=8)
ax1.set_xlabel("Category", fontsize=8)
plt.tight_layout()
st.pyplot(fig1)

# Profit by Region
st.subheader("Profit by Region")
st.write("The charts show the distribution of sales across categories and profit across regions based on the applied filters. West region generates the highest profit, followed by South, Central, and East regions. This indicates that the West region is the most profitable area for the business, while the Central region has the lowest profit among the four regions.")

profit_by_region = (filtered_df.groupby("Region")["Profit"].sum().sort_values(ascending=False))
fig2, ax2 = plt.subplots(figsize=(5, 3))
profit_by_region.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Profit", fontsize=8)
ax2.set_xlabel("Region", fontsize=8)
plt.tight_layout()
st.pyplot(fig2)

# Monthly Sales Price Trend
st.subheader("Monthly Sales Trend")
st.write("The line chart illustrates the monthly sales trend based on the applied filters. The sales show a clear seasonal pattern, with peaks around November and December, likely due to holiday shopping. There is also a noticeable dip in sales during the summer months, which may be attributed to reduced consumer spending during that period.")

monthly_Sales = (filtered_df.set_index("Order Date").resample("ME")["Sales Price"].sum())
fig3, ax3 = plt.subplots(figsize=(5, 3))
monthly_Sales.plot(ax=ax3)
ax3.set_ylabel("Sales Price", fontsize = 8)
ax3.set_xlabel("Month", fontsize = 8)
plt.tight_layout()
st.pyplot(fig3)

# T# Top 10 Most Profitable Products
st.subheader("Top 10 Most Profitable Products")
st.write("The table lists the top 10 most profitable products based on the applied filters. These products contribute significantly to the overall profit, and understanding their performance can help in inventory management and marketing strategies.")
top10_profit = filtered_df.groupby("Product Name")["Profit"].sum().nlargest(10)

fig4, ax4 = plt.subplots(figsize=(10, 8))
top10_profit.plot(kind="bar", ax=ax4)
ax4.set_ylabel("Profit", fontsize=10)
ax4.set_xlabel("Product Name", fontsize=10)
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
st.pyplot(fig4)

# Top 10 Most Loss-Making Products
st.subheader("Top 10 Most Loss-Making Products")
st.write("The table lists the top 10 most loss-making products based on the applied filters. These products are generating negative profit, and analyzing their performance can help identify issues such as pricing, cost management, or demand forecasting that may need to be addressed to improve profitability.")
top10_loss = filtered_df.groupby("Product Name")["Profit"].sum().nsmallest(10)

fig5, ax5 = plt.subplots(figsize=(10, 8))
top10_loss.plot(kind="bar", ax=ax5, color="red")
ax5.set_ylabel("Profit", fontsize=10)
ax5.set_xlabel("Product Name", fontsize=10)
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
st.pyplot(fig5)

# Prepare aggregated product-level metrics
st.subheader("Sales vs Profit by Product")
st.write("The scatter plot illustrates the relationship between total sales and total profit for each product based on the applied filters. The regression line indicates the overall trend, showing whether higher sales are generally associated with higher profits. This analysis can help identify products that are performing well in terms of profitability relative to their sales, as well as those that may be underperforming.")

product_metrics = (filtered_df.groupby("Product Name").agg(Total_Sales=("Sales Price", "sum"),Total_Profit=("Profit", "sum")).reset_index())

st.write("The table below shows the total sales and total profit for each product based on the applied filters.")

x = product_metrics["Total_Sales"]
y = product_metrics["Total_Profit"]

fig6, ax6 = plt.subplots(figsize=(6, 4))
ax6.scatter(x, y, alpha=0.6)
coeffs = np.polyfit(x, y, 1)
reg_line = np.poly1d(coeffs)
ax6.plot(x, reg_line(x), linewidth=1)
ax6.set_xlabel("Total Sales", fontsize=9)
ax6.set_ylabel("Total Profit", fontsize=9)
ax6.set_title("Sales vs Profit by Product", fontsize=11)
ax6.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig6)

# Joint Distribution using 2D histogram
st.subheader("Sales vs Profit Distribution")
st.write("The 2D histogram illustrates the joint distribution of total sales and total profit for each product based on the applied filters.")

fig7, ax7 = plt.subplots(figsize=(6, 4))
hb = ax7.hexbin(x,y, gridsize=25, cmap='Blues', mincnt=1)
ax7.set_title("Sales vs Profit Density", fontsize=11)
ax7.set_xlabel("Total Sales", fontsize=9)
ax7.set_ylabel("Total Profit", fontsize=9)
ax7.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig7)

# Distribution of shipping urgency
st.subheader("Distribution of Shipping Urgency")
st.write("The bar chart shows the distribution of shipping urgency levels based on the applied filters. This information can help the business understand the demand for different shipping options and optimize logistics accordingly.")

shipping_urgency_counts = filtered_df["Shipping Urgency"].value_counts()

fig8, ax8 = plt.subplots(figsize=(5, 3))
shipping_urgency_counts.plot(kind="bar", ax=ax8, color=["skyblue", "salmon", "lightgreen"])
ax8.set_xlabel("Shipping Urgency", fontsize=8)
ax8.set_ylabel("Count", fontsize=8)
ax8.set_title("Distribution of Shipping Urgency", fontsize=10)
ax8.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig8)

# Profit Distribution Across Days to Ship Categories
st.subheader("Profit Distribution Across Days to Ship Categories")
st.write("The box plot illustrates the distribution of profit across different categories of days to ship based on the applied filters. This analysis can help identify if there are any significant differences in profitability based on shipping times, which may inform decisions on inventory management and customer service strategies.")

filtered_df["Days to Ship Category"] = pd.cut(filtered_df["Days to Ship"], bins=[-1, 0, 3, float("inf")], labels=["Immediate", "Urgent", "Standard"])

fig9, ax9 = plt.subplots(figsize=(6, 4))
sns.violinplot(x="Days to Ship Category", y="Profit", data=filtered_df, ax=ax9)
ax9.set_xlabel("Days to Ship Category", fontsize=8)
ax9.set_ylabel("Profit", fontsize=8)
ax9.set_title("Profit Distribution by Days to Ship", fontsize=10)
ax9.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig9)

# Profitability by Shipping Mode
st.subheader("Profitability by Shipping Mode")
st.write("The bar chart compares the average profit for each shipping mode based on the applied filters. This analysis can help the business understand which shipping options are more profitable and may guide decisions on shipping policies and customer incentives.")
ship_mode_profit = (filtered_df.groupby("Ship Mode")["Profit"].sum().reset_index())

fig10, ax10 = plt.subplots(figsize=(5, 3))
sns.barplot(x="Ship Mode", y="Profit", data=ship_mode_profit, ax=ax10, palette="Set2")
ax10.set_xlabel("Ship Mode", fontsize=8)
ax10.set_ylabel("Total Profit", fontsize=8)
ax10.set_title("Total Profit by Ship Mode", fontsize=10)
ax10.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig10)

# Total Sales and Profit by Region
st.subheader("Total Sales and Profit by Region")
st.write("The grouped bar chart compares total sales and total profit across different regions based on the applied filters. This analysis can help identify which regions are performing well in terms of sales and profitability, allowing the business to focus on growth opportunities and address challenges in underperforming areas.")

region_summary = filtered_df.groupby("Region").agg({"Total Sales": "sum","Profit": "sum"}).reset_index()

fig11, ax11 = plt.subplots(figsize=(6, 4))
sns.barplot(x="Region", y="Total Sales", data=region_summary, ax=ax11, color="lightblue", label="Total Sales")
sns.barplot(x="Region", y="Profit", data=region_summary, ax=ax11, color="salmon", label="Total Profit")
ax11.set_xlabel("Region", fontsize=8)
ax11.set_ylabel("Amount", fontsize=8)
ax11.set_title("Total Sales and Profit by Region", fontsize=10)
ax11.legend()
ax11.tick_params(axis='both', labelsize=8)
plt.tight_layout()
st.pyplot(fig11)

# Original Price vs Discounted Price by Sub-Category
st.subheader("Original Price vs Discounted Price by Sub-Category")
st.write("The line chart compares the average original price and average discounted price for each sub-category based on the applied filters. This analysis can help the business understand the pricing dynamics and discount strategies across different product sub-categories, which may inform decisions on promotions and inventory management.")

# Aggregate data
price_comparison = (
    filtered_df
    .groupby("Sub-Category")
    .agg({
        "Sales Price": "mean",
        "Original Price": "mean"
    })
    .reset_index()
)

price_comparison.rename(
    columns={"Sales Price": "Average Discounted Price"},
    inplace=True
)

# Create figure properly for Streamlit
fig12, ax12 = plt.subplots(figsize=(8, 4))

ax12.plot(
    price_comparison["Sub-Category"],
    price_comparison["Original Price"],
    marker="o",
    label="Original Price"
)

ax12.plot(
    price_comparison["Sub-Category"],
    price_comparison["Average Discounted Price"],
    marker="o",
    label="Discounted Price"
)

ax12.set_title("Original vs Discounted Price by Sub-Category", fontsize=11)
ax12.set_xlabel("Sub-Category", fontsize=9)
ax12.set_ylabel("Average Price", fontsize=9)
ax12.tick_params(axis="x", labelrotation=45, labelsize=8)
ax12.tick_params(axis="y", labelsize=8)
ax12.legend(fontsize=8)
plt.tight_layout()
st.pyplot(fig12)

# Raw data (optional)
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)