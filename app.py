import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        # 📥 правильный экспорт Google Sheets
      url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1443532418"

        df = pd.read_csv(url)

        st.success("Данные загружены")

        st.subheader("Preview данных")
        st.dataframe(df)

        st.subheader("Базовая информация")
        st.write("Строк:", len(df))
        st.write("Колонки:", list(df.columns))

    except Exception as e:
        st.error("Ошибка загрузки данных")
        st.exception(e)
