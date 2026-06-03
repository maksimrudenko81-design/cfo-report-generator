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
        # CLEAN: убираем полностью пустые строки
        # =========================
        df = df.dropna(how="all")

        # превращаем всё в текст для безопасного поиска
        df_str = df.astype(str)

        # =========================
        # ИЩЕМ БЛОК 1 (защищённо)
        # =========================
        mask_orders = df_str.apply(lambda row: row.str.contains("отработанные", case=False, na=False)).any(axis=1)
        mask_plan = df_str.apply(lambda row: row.str.contains("2.1", na=False)).any(axis=1)

        if not mask_orders.any():
            st.error("Не найден блок 'отработанные заказы'")
            st.dataframe(df)
            st.stop()

        if not mask_plan.any():
            st.error("Не найден блок '2.1'")
            st.dataframe(df)
            st.stop()

        idx_orders = mask_orders[mask_orders].index[0]
        idx_plan = mask_plan[mask_plan].index[0]

        # =========================
        # ORDERS BLOCK
        # =========================
        df_orders = df.iloc[idx_orders:idx_plan]

        st.subheader("📦 Отработанные заказы + выручка")
        st.dataframe(df_orders)

        # =========================
        # PLAN BLOCK
        # =========================
        df_plan = df.iloc[idx_plan:]

        st.subheader("📊 План / Факт")
        st.dataframe(df_plan)

        st.success("Данные разделены стабильно")

    except Exception as e:
        st.error("Ошибка обработки")
        st.exception(e)
