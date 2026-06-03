import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CFO Dashboard", layout="wide")

st.title("📊 CFO Dashboard")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    gid = "1443532418"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    df = pd.read_csv(url)

    st.success("Данные загружены")

    st.subheader("Raw data")
    st.dataframe(df)

    df = df.dropna(how="all")

    orders_raw = df.iloc[5, 1:5].values
    revenue_raw = df.iloc[16, 1:5].values

    orders = np.array([float(str(x).replace("\u00a0","").replace(" ","")) for x in orders_raw])
    revenue = np.array([float(str(x).replace("\u00a0","").replace(" ","")) for x in revenue_raw])

    periods = ["P1","P2","P3","P4"]

    orders_cum = np.cumsum(orders)
    revenue_cum = np.cumsum(revenue)

    st.subheader("Orders vs Revenue Gap")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(periods, orders_cum, marker="o", label="Orders")
    ax.plot(periods, revenue_cum, marker="s", label="Revenue")

    ax.fill_between(periods, orders_cum, revenue_cum,
                    where=(orders_cum > revenue_cum),
                    alpha=0.3,
                    color="red")

    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    st.subheader("KPI")

    col1, col2, col3 = st.columns(3)

    col1.metric("Orders", f"{orders.sum():,.0f}")
    col2.metric("Revenue", f"{revenue.sum():,.0f}")
    col3.metric("Gap", f"{(orders.sum()-revenue.sum()):,.0f}")
