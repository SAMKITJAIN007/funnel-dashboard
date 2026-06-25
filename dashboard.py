import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Funnel Dashboard", layout="wide")
st.title("Customer Funnel & Conversion Dashboard")

df = pd.read_csv("data/funnel_data.csv", parse_dates=["date"])

# Sidebar filter
source = st.sidebar.selectbox("Traffic Source", ["All"] + list(df["source"].unique()))
if source != "All":
    df = df[df["source"] == source]

# Aggregate totals
totals = df[["visitors","signups","trials","purchases"]].sum()

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Visitors",    f"{totals['visitors']:,}")
col2.metric("Sign-ups",    f"{totals['signups']:,}")
col3.metric("Trials",      f"{totals['trials']:,}")
col4.metric("Purchases",   f"{totals['purchases']:,}")

st.subheader("Conversion Funnel")

# Funnel chart
stages  = ["Visitors", "Sign-ups", "Trials", "Purchases"]
values  = [totals["visitors"], totals["signups"], totals["trials"], totals["purchases"]]
pct     = [f"{v/totals['visitors']*100:.1f}%" for v in values]

fig_funnel = go.Figure(go.Funnel(
    y=stages, x=values,
    textinfo="value+percent initial",
    marker=dict(color=["#2a78d6","#1baf7a","#eda100","#008300"])
))
fig_funnel.update_layout(margin=dict(t=20, b=20))
st.plotly_chart(fig_funnel, use_container_width=True)

st.subheader("Weekly Trend")

# Weekly trend line
weekly = df.groupby("date")[["visitors","signups","purchases"]].sum().reset_index()
fig_trend = px.line(
    weekly, x="date",
    y=["visitors","signups","purchases"],
    labels={"value":"Count","date":"Week"},
    color_discrete_sequence=["#2a78d6","#1baf7a","#008300"]
)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("Conversion Rate by Source")

# Conversion rates
by_source = df.groupby("source").sum(numeric_only=True)
by_source["cvr"] = (by_source["purchases"] / by_source["visitors"] * 100).round(2)
fig_bar = px.bar(
    by_source.reset_index(), x="source", y="cvr",
    labels={"cvr":"Conversion Rate (%)","source":"Source"},
    color="source",
    color_discrete_sequence=["#2a78d6","#1baf7a","#eda100"]
)
st.plotly_chart(fig_bar, use_container_width=True)