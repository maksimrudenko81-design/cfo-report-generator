import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

sheet_id = st.text_input("Google Sheets ID (не ссылка, а ID)")

if st.button("Загрузить данные"):

    try:
        # =========================
        # BLOCK 1: ORDERS + REVENUE
        # =========================
        url_orders = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&range=A2:G32"
        df_orders = pd.read_csv(url_orders)

        # чистим строки
        df_orders = df_orders.dropna(how='all')

        st.subheader("Отработанные заказы / Выручка")
        st.dataframe(df_orders)

        # =========================
        # BLOCK 2: PLAN vs FACT
        # =========================
        url_plan = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&range=A36:G64"
        df_plan = pd.read_csv(url_plan)

        df_plan = df_plan.dropna(how='all')

        st.subheader("План vs Факт")
        st.dataframe(df_plan)

        st.success("Данные корректно загружены")

    except Exception as e:
        st.error("Ошибка загрузки")
        st.exception(e)
