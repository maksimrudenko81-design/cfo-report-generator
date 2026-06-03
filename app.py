import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")
st.title("📊 CFO Report Generator")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)

        # приводим всё к строкам
        df = df.dropna(how="all")

        # находим пустые строки (разделители блоков)
        empty_rows = df.isna().all(axis=1)

        split_points = list(df[empty_rows].index)

        # добавляем границы
        blocks = []
        start = 0

        for end in split_points:
            if end > start:
                blocks.append(df.iloc[start:end])
            start = end + 1

        # последний блок
        if start < len(df):
            blocks.append(df.iloc[start:])

        # =====================
        # ВИЗУАЛИЗАЦИЯ БЛОКОВ
        # =====================

        for i, block in enumerate(blocks):
            st.subheader(f"📦 Блок {i+1}")
            st.dataframe(block)

        st.success(f"Найдено блоков: {len(blocks)}")

    except Exception as e:
        st.error("Ошибка")
        st.exception(e)
