import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EV Market Intelligence", page_icon="⚡", layout="wide")
st.title("⚡ EV Market Intelligence Dashboard")
st.caption("Capstone project | Executive strategy • Business intelligence • Sustainable mobility research")

@st.cache_data
def load_data():
    return pd.read_csv("ev_market_train.csv")

df = load_data()
# Sidebar filters
st.sidebar.header("Dashboard filters")
years = sorted(df["model_year"].dropna().unique().tolist())
year_range = st.sidebar.slider("Model year", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Vehicle category", categories, default=categories)
regions = sorted(df["market_region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Market region", regions, default=regions)
batteries = sorted(df["battery_type"].dropna().unique().tolist())
selected_batteries = st.sidebar.multiselect("Battery technology", batteries, default=batteries)
countries = sorted(df["manufacturing_country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect("Manufacturing country", countries, default=countries)

filtered = df[
    df["model_year"].between(year_range[0], year_range[1]) &
    df["category"].isin(selected_categories) &
    df["market_region"].isin(selected_regions) &
    df["battery_type"].isin(selected_batteries) &
    df["manufacturing_country"].isin(selected_countries)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Change one or more filters.")
    st.stop()

def fmt_num(x):
    return f"{x:,.0f}"

total_sales = filtered["annual_sales_units"].sum(skipna=True)
avg_range = filtered["range_km"].mean()
avg_rating = filtered["customer_rating"].mean()
avg_price = filtered["price_usd"].mean()
avg_battery = filtered["battery_capacity_kwh"].mean()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Records", fmt_num(len(filtered)))
c2.metric("Annual sales units*", fmt_num(total_sales))
c3.metric("Avg. driving range", f"{avg_range:,.0f} km")
c4.metric("Avg. customer rating", f"{avg_rating:.2f}/5" if pd.notna(avg_rating) else "N/A")
c5.metric("Avg. listed price", f"${avg_price:,.0f}")

st.caption("*Sales are summed from the supplied dataset. Check for extreme values before treating totals as real-world market estimates.")

tab1, tab2, tab3 = st.tabs(["Executive overview", "Technology & product", "Geography & data quality"])

with tab1:
    left,right = st.columns(2)
    cat = filtered.groupby("category", as_index=False).agg(sales=("annual_sales_units","sum"), records=("vehicle_id","count"), rating=("customer_rating","mean")).sort_values("sales",ascending=False)
    left.plotly_chart(px.bar(cat, x="category", y="sales", title="Annual sales by vehicle category", labels={"category":"Category","sales":"Sales units"}, hover_data=["records","rating"]), use_container_width=True)
    maker = filtered.groupby("manufacturer", as_index=False).agg(sales=("annual_sales_units","sum"), rating=("customer_rating","mean"), records=("vehicle_id","count")).sort_values("sales",ascending=False).head(15)
    right.plotly_chart(px.bar(maker, x="sales", y="manufacturer", orientation="h", title="Top 15 manufacturers by summed sales", labels={"sales":"Sales units","manufacturer":"Manufacturer"}, hover_data=["rating","records"]), use_container_width=True)
    left2,right2 = st.columns(2)
    annual = filtered.groupby("model_year", as_index=False).agg(sales=("annual_sales_units","sum"), records=("vehicle_id","count"))
    left2.plotly_chart(px.line(annual, x="model_year", y="sales", markers=True, title="Sales by model year", labels={"model_year":"Model year","sales":"Sales units"}), use_container_width=True)
    reg = filtered.groupby("market_region", as_index=False).agg(sales=("annual_sales_units","sum"), records=("vehicle_id","count")).sort_values("sales",ascending=False)
    right2.plotly_chart(px.bar(reg, x="market_region", y="sales", title="Market region comparison", labels={"market_region":"Region","sales":"Sales units"}), use_container_width=True)

with tab2:
    left,right = st.columns(2)
    batt = filtered.groupby("battery_type", as_index=False).agg(records=("vehicle_id","count"), avg_range=("range_km","mean"), avg_rating=("customer_rating","mean"), avg_capacity=("battery_capacity_kwh","mean"))
    left.plotly_chart(px.pie(batt, names="battery_type", values="records", hole=.45, title="Battery technology mix", hover_data=["avg_range","avg_rating"]), use_container_width=True)
    right.plotly_chart(px.bar(batt, x="battery_type", y="avg_range", title="Average range by battery technology", labels={"battery_type":"Battery type","avg_range":"Average range (km)"}, hover_data=["records","avg_capacity","avg_rating"]), use_container_width=True)
    cat_range = filtered.groupby("category", as_index=False).agg(avg_range=("range_km","mean"), avg_capacity=("battery_capacity_kwh","mean"), avg_price=("price_usd","mean"), avg_rating=("customer_rating","mean"), records=("vehicle_id","count"))
    left2,right2 = st.columns(2)
    left2.plotly_chart(px.scatter(filtered, x="battery_capacity_kwh", y="range_km", color="battery_type", hover_data=["category","manufacturer"], title="Battery capacity vs. driving range"), use_container_width=True)
    right2.plotly_chart(px.bar(cat_range.sort_values("avg_range",ascending=False), x="category", y="avg_range", title="Average range by category", labels={"category":"Category","avg_range":"Average range (km)"}, hover_data=["avg_price","avg_rating","records"]), use_container_width=True)

with tab3:
    left,right = st.columns(2)
    country_df = filtered.groupby("manufacturing_country", as_index=False).agg(records=("vehicle_id","count"), sales=("annual_sales_units","sum"), avg_range=("range_km","mean")).sort_values("records",ascending=False)
    left.plotly_chart(px.bar(country_df, x="manufacturing_country", y="records", title="Records by manufacturing country", labels={"manufacturing_country":"Country","records":"Vehicle records"}), use_container_width=True)
    right.plotly_chart(px.bar(country_df, x="manufacturing_country", y="sales", title="Summed sales by manufacturing country", labels={"manufacturing_country":"Country","sales":"Sales units"}), use_container_width=True)
    missing = filtered.isna().sum().reset_index()
    missing.columns = ["field","missing_count"]
    missing = missing[missing["missing_count"]>0].sort_values("missing_count",ascending=False)
    st.subheader("Missing values in filtered data")
    if missing.empty:
        st.success("No missing values in the filtered subset.")
    else:
        st.plotly_chart(px.bar(missing, x="field", y="missing_count", title="Missing values by field"), use_container_width=True)

st.subheader("Filtered data explorer")
show_cols = ["vehicle_id","model_name","manufacturer","model_year","manufacturing_country","market_region","category","battery_type","battery_capacity_kwh","range_km","price_usd","annual_sales_units","customer_rating"]
st.dataframe(filtered[show_cols].head(1000), use_container_width=True, hide_index=True)
st.download_button("Download filtered rows as CSV", filtered.to_csv(index=False).encode("utf-8"), "ev_filtered_data.csv", "text/csv")

with st.expander("Methodology & caveats"):
    st.markdown("""
    - This dashboard uses `ev_market_train.csv` as the analysis dataset. The test file is included in the project package but is not merged into the dashboard analysis.
    - KPIs and charts recalculate from the sidebar filters.
    - Annual sales are summed from row-level records. The data contains a highly skewed sales distribution, so validate extreme values and the meaning of each row before interpreting totals as market-wide sales.
    - Correlation between battery capacity and range is descriptive, not proof of causation.
    - Customer ratings and other fields have missing values; averages ignore missing values by default.
    - Treat results as dataset-specific insights, not verified real-world market facts.
    """)
