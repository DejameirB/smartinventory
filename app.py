import streamlit as st
from database import SessionLocal
from models import Product, Sale
import pandas as pd

st.set_page_config(page_title="SmartInventory", layout="wide")

st.title("SmartInventory — QuickMart Sales Dashboard")
st.markdown("90-day sales analysis across 50 products and 6 categories")

session = SessionLocal()

# ── SUMMARY METRICS ──
sales = session.query(Sale).all()
products = session.query(Product).all()

total_units = sum(s.units_sold for s in sales)
weekend_sales = sum(s.units_sold for s in sales if s.is_weekend)
weekday_sales = sum(s.units_sold for s in sales if not s.is_weekend)
weekend_days = len([s for s in sales if s.is_weekend])
weekday_days = len([s for s in sales if not s.is_weekend])
avg_weekend = round(weekend_sales / weekend_days, 1) if weekend_days > 0 else 0
avg_weekday = round(weekday_sales / weekday_days, 1) if weekday_days > 0 else 0
weekend_lift = round(((avg_weekend - avg_weekday) / avg_weekday) * 100, 1) if avg_weekday > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Units Sold", f"{total_units:,}")
col2.metric("Avg Weekend Units", f"{avg_weekend:,}")
col3.metric("Weekend Lift vs Weekday", f"{weekend_lift}%")

st.divider()

# ── PRODUCTS TABLE ──
st.subheader("Products Table")
product_data = pd.DataFrame([
    {
        "ID": p.id,
        "Product Name": p.product_name,
        "Category": p.category,
        "Base Sale Rate": p.base_sale_rate,
        "Weekend Multiplier": p.weekend_multiplier
    }
    for p in products
])
st.dataframe(product_data, use_container_width=True)

st.divider()

# ── SALES TABLE ──
st.subheader("Sales Records (first 100 rows)")
sales_data = pd.DataFrame([
    {
        "Date": s.sale_date,
        "Day": s.day_of_week,
        "Product": s.product_name,
        "Category": s.category,
        "Units Sold": s.units_sold,
        "Weekend": s.is_weekend
    }
    for s in sales[:100]
])
st.dataframe(sales_data, use_container_width=True)

session.close()