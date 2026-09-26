import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "retail_dw")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

@st.cache_data
def load_data(query):
    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)


# ---------------------------------------------------------
# Page title
# ---------------------------------------------------------

st.title("📊 Retail Analytics Dashboard")
st.markdown(
    "Interactive sales and customer analytics based on the "
    "UCI Online Retail dataset."
)

st.divider()


# ---------------------------------------------------------
# Load summary metrics
# ---------------------------------------------------------

summary = load_data("""
    SELECT
        COUNT(*) AS transactions,
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(DISTINCT invoice_no) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers
    FROM sales_mart;
""")

customer_summary = load_data("""
    SELECT
        customer_type,
        COUNT(*) AS customer_count
    FROM customer_mart
    GROUP BY customer_type;
""")

total_revenue = float(summary.iloc[0]["total_revenue"])
total_orders = int(summary.iloc[0]["total_orders"])
total_customers = int(summary.iloc[0]["total_customers"])
transactions = int(summary.iloc[0]["transactions"])

repeat_customers = int(
    customer_summary.loc[
        customer_summary["customer_type"] == "Repeat Customer",
        "customer_count"
    ].sum()
)

repeat_rate = (
    repeat_customers / total_customers * 100
    if total_customers > 0
    else 0
)


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"£{total_revenue:,.2f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Transactions",
    f"{transactions:,}"
)

col5.metric(
    "Repeat Rate",
    f"{repeat_rate:.1f}%"
)


st.divider()


# ---------------------------------------------------------
# Monthly Revenue Trend
# ---------------------------------------------------------

st.subheader("📈 Monthly Revenue Trend")

monthly_sales = load_data("""
    SELECT
        year,
        month,
        MIN(full_date) AS month_date,
        SUM(revenue) AS revenue,
        COUNT(DISTINCT invoice_no) AS orders
    FROM sales_mart
    GROUP BY year, month
    ORDER BY year, month;
""")

monthly_sales["month_date"] = pd.to_datetime(
    monthly_sales["month_date"]
)

st.line_chart(
    monthly_sales.set_index("month_date")["revenue"]
)


# ---------------------------------------------------------
# Revenue and Orders
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Monthly Revenue")

    revenue_chart = monthly_sales[
        ["month_date", "revenue"]
    ].copy()

    revenue_chart = revenue_chart.set_index("month_date")

    st.bar_chart(revenue_chart)


with col2:
    st.subheader("🧾 Monthly Orders")

    order_chart = monthly_sales[
        ["month_date", "orders"]
    ].copy()

    order_chart = order_chart.set_index("month_date")

    st.bar_chart(order_chart)


# ---------------------------------------------------------
# Top Products
# ---------------------------------------------------------

st.subheader("🏆 Top 10 Products by Revenue")

top_products = load_data("""
    SELECT
        description,
        SUM(quantity) AS quantity_sold,
        ROUND(SUM(revenue), 2) AS revenue
    FROM sales_mart
    GROUP BY description
    ORDER BY revenue DESC
    LIMIT 10;
""")

top_products = top_products.sort_values(
    "revenue",
    ascending=True
)

st.bar_chart(
    top_products.set_index("description")["revenue"]
)


# ---------------------------------------------------------
# Country Sales
# ---------------------------------------------------------

st.subheader("🌍 Sales by Country")

country_sales = load_data("""
    SELECT
        country,
        ROUND(SUM(revenue), 2) AS revenue,
        COUNT(DISTINCT invoice_no) AS orders
    FROM sales_mart
    GROUP BY country
    ORDER BY revenue DESC;
""")

st.dataframe(
    country_sales,
    use_container_width=True
)


# ---------------------------------------------------------
# Customer Retention
# ---------------------------------------------------------

st.subheader("👥 Customer Retention")

col1, col2 = st.columns(2)

with col1:

    retention_data = load_data("""
        SELECT
            customer_type,
            COUNT(*) AS customer_count
        FROM customer_mart
        GROUP BY customer_type;
    """)

    st.bar_chart(
        retention_data.set_index("customer_type")
        ["customer_count"]
    )


with col2:

    st.metric(
        "Repeat Customers",
        f"{repeat_customers:,}"
    )

    st.metric(
        "One-Time Customers",
        f"{total_customers - repeat_customers:,}"
    )

    st.metric(
        "Repeat Purchase Rate",
        f"{repeat_rate:.1f}%"
    )


# ---------------------------------------------------------
# Top Customers
# ---------------------------------------------------------

st.subheader("⭐ Top 10 Customers by Revenue")

top_customers = load_data("""
    SELECT
        customer_id,
        country,
        order_count,
        ROUND(total_revenue, 2) AS total_revenue,
        recency_days,
        customer_type
    FROM customer_mart
    ORDER BY total_revenue DESC
    LIMIT 10;
""")

st.dataframe(
    top_customers,
    use_container_width=True
)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "Retail Analytics Platform | PostgreSQL + Python + Streamlit"
)