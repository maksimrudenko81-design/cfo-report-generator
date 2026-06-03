import streamlit as st

st.set_page_config(page_title="CFO Report Generator", layout="wide")

st.title("📊 CFO Report Generator")

st.write("Подключение к Google Sheets будет добавлено на следующем шаге")

url = st.text_input("Вставь ссылку на Google Sheets (CSV экспорт)")

if st.button("Проверить подключение"):
    if url:
        st.success("Ссылка получена. Данные будут загружены на следующем шаге.")
    else:
        st.error("Вставь ссылку")
