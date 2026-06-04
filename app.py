import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CFO Dashboard", layout="wide")

st.title("📊 CFO Dashboard")

sheet_id = st.text_input(
    "Google Sheets ID",
    value="1zAVRqUNVcmU-zFkkL3Azkir4mI4FTC41FGZSgpCuGJU"
)

def clean(x):
    if pd.isna(x):
        return 0
    x = str(x)
    x = x.replace("\u00a0", "").replace(" ", "").replace(",", ".")
    try:
        return float(x)
    except:
        return 0

if st.button("Загрузить данные"):

    try:
        gid = "1443532418"

        url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{sheet_id}/export?format=csv&gid={gid}"
        )

        df = pd.read_csv(url, header=None)

        st.success("Данные загружены")

        # =========================
        # KPI БЛОК
        # =========================

        orders = np.array([clean(df.iloc[8, 1]), clean(df.iloc[8, 2]),
                           clean(df.iloc[8, 3]), clean(df.iloc[8, 4])])

        revenue = np.array([clean(df.iloc[17, 1]), clean(df.iloc[17, 2]),
                             clean(df.iloc[17, 3]), clean(df.iloc[17, 4])])

        plan = np.array([clean(df.iloc[41, 1]), clean(df.iloc[41, 2]),
                         clean(df.iloc[41, 3]), clean(df.iloc[41, 4])])

        fact = np.array([clean(df.iloc[51, 1]), clean(df.iloc[51, 2]),
                         clean(df.iloc[51, 3]), clean(df.iloc[51, 4])])

        periods = ["Янв", "Фев", "Мар", "Апр"]

        orders_cum = np.cumsum(orders)
        revenue_cum = np.cumsum(revenue)

        total_orders = orders.sum()
        total_revenue = revenue.sum()
        gap = total_orders - total_revenue

        # =========================
        # KPI
        # =========================

        st.subheader("KPI")

        col1, col2, col3 = st.columns(3)

        col1.metric("Объем заказов", f"{total_orders:,.0f} ₽".replace(",", " "))
        col2.metric("Реализация", f"{total_revenue:,.0f} ₽".replace(",", " "))
        col3.metric("Разрыв (потенциал)", f"{gap:,.0f} ₽".replace(",", " "))

        # =========================
        # ГРАФИК 1
        # =========================

        st.subheader("Динамика заказов и реализаций")

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(periods, orders_cum, marker="o", label="Заказы")
        ax.plot(periods, revenue_cum, marker="o", label="Реализация")

        ax.fill_between(periods, orders_cum, revenue_cum,
                        where=(orders_cum > revenue_cum),
                        alpha=0.25, label="Разрыв")

        ax.set_ylabel("₽")
        ax.grid(alpha=0.3)
        ax.legend()

        st.pyplot(fig)

        # =========================
        # ПЛАН / ФАКТ
        # =========================

        st.subheader("План vs Факт")

        x = np.arange(len(periods))
        width = 0.35

        fig2, ax2 = plt.subplots(figsize=(12, 6))

        ax2.bar(x - width/2, plan, width, label="План")
        ax2.bar(x + width/2, fact, width, label="Факт")

        ax2.set_xticks(x)
        ax2.set_xticklabels(periods)

        ax2.legend()

        st.pyplot(fig2)

        # =========================
        # ЛОГИКА
        # =========================

        st.subheader("Вывод")

        st.markdown(f"""
- Заказы: **{total_orders:,.0f} ₽**
- Реализация: **{total_revenue:,.0f} ₽**
- Разрыв: **{gap:,.0f} ₽**

Разрыв отражает не выполненные заказы, а **разницу между созданием заказа и признанием выручки**.
""".replace(",", " "))

    except Exception as e:
        st.error("Ошибка")
        st.exception(e)
