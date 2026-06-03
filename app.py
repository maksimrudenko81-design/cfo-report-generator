import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        # =========================
        # LOAD FULL SHEET
        # =========================
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

        df = pd.read_csv(url)

        st.subheader("RAW DATA")
        st.dataframe(df)

        st.success("Данные загружены")

        st.info("Следующий шаг: разрежем на блоки Orders / Plan / Fact")

    except Exception as e:
        st.error("Ошибка загрузки")
        st.exception(e)
