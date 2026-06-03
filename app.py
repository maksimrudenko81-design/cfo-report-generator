import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

st.write("Вставь CSV-ссылку на Google Sheets (лист periods или categories)")

url = st.text_input("Google Sheets CSV URL")

if st.button("Загрузить данные"):

    try:
        df = pd.read_csv(url)

        st.success("Данные загружены")

        st.subheader("Preview")
        st.dataframe(df)

        st.subheader("Базовая статистика")

        st.write("Строк:", len(df))
        st.write("Колонки:", list(df.columns))

    except Exception as e:
        st.error("Ошибка загрузки данных")
        st.exception(e)
