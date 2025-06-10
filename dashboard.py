import streamlit as st
import pandas as pd
import plotly.express as px
import time

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Semiconductor Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Sidebar – Logo and Filters
# -------------------------------
with st.sidebar:
    st.image("data/logo.png", width=150)
    st.title("🔍 Filter the Data")

    df = pd.read_csv("top_10_revenues.csv")
    df["Year"] = df["Year"].astype(int)
    df["Revenue (B USD)"] = pd.to_numeric(df["Revenue (B USD)"], errors="coerce")
    df["Change (%)"] = pd.to_numeric(df["Change (%)"], errors="coerce")

    companies = df["Company"].unique()
    selected_companies = st.multiselect("Select Company(ies)", companies, default=companies)

    min_year, max_year = df["Year"].min(), df["Year"].max()
    selected_years = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# -------------------------------
# Filtered Data
# -------------------------------
df_filtered = df[
    (df["Company"].isin(selected_companies)) &
    (df["Year"].between(*selected_years))
]

with st.spinner("Loading data..."):
    time.sleep(1)

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("📊 Semiconductor Company Revenue Dashboard")
st.markdown("View revenue trends of the top 10 semiconductor companies using real data.")

# -------------------------------
# Section 1: Revenue Over Time
# -------------------------------
st.subheader("1️⃣ Revenue Over Time")
line_data = df_filtered.pivot(index="Year", columns="Company", values="Revenue (B USD)")
st.line_chart(line_data)

# -------------------------------
# Section 2: YoY Change (%)
# -------------------------------
st.subheader("2️⃣ Year-over-Year Change (%)")
bar_data = df_filtered.pivot(index="Year", columns="Company", values="Change (%)")
st.bar_chart(bar_data)

# -------------------------------
# Section 3: Total Revenue by Company
# -------------------------------
st.subheader("3️⃣ Total Revenue by Company")
total = df_filtered.groupby("Company")["Revenue (B USD)"].sum().reset_index().sort_values(by="Revenue (B USD)", ascending=False)
fig = px.bar(
    total,
    x="Company",
    y="Revenue (B USD)",
    title="Total Revenue Across All Selected Years",
    text_auto=True
)
fig.update_layout(yaxis_tickprefix="$")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Section 4: Download Filtered Data
# -------------------------------
st.subheader("📥 Download Filtered Data")
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_revenue_data.csv",
    mime="text/csv"
)
