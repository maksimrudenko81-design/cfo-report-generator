import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)

        # =========================
        # НАХОДИМ РАЗДЕЛЫ
        # =========================
        df_str = df.astype(str)

        # индекс начала блоков
        idx_orders = df_str[df_str.iloc[:,0].str.contains("1 - отработанные заказы", na=False)].index[0]
        idx_plan = df_str[df_str.iloc[:,0].str.contains("2.1 - План", na=False)].index[0]

        # =========================
        # ORDERS BLOCK
        # =========================
        df_orders = df.iloc[idx_orders+2:idx_plan]

        st.subheader("📦 Отработанные заказы + выручка")
        st.dataframe(df_orders)

        # =========================
        # PLAN BLOCK
        # =========================
        df_plan = df.iloc[idx_plan+2:]

        st.subheader("📊 План / Факт")
        st.dataframe(df_plan)

        st.success("Данные разделены корректно")

    except Exception as e:
        st.error("Ошибка обработки")
        st.exception(e)
