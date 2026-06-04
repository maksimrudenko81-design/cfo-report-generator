import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CFO Dashboard",
    layout="wide"
)

st.title("📊 CFO Dashboard")

sheet_id = st.text_input(
    "Google Sheets ID",
    value="1zAVRqUNVcmU-zFkkL3Azkir4mI4FTC41FGZSgpCuGJU"
)

if st.button("Загрузить данные"):

    try:

        gid = "1443532418"

        url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{sheet_id}/export?format=csv&gid={gid}"
        )

        df = pd.read_csv(url, header=None)

        st.success("Данные загружены")

        # ==================================
        # ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
        # ==================================

        def clean_number(x):

            if pd.isna(x):
                return 0

            x = str(x)

            x = x.replace("\u00a0", "")
            x = x.replace(" ", "")
            x = x.replace(",", ".")

            if x == "":
                return 0

            try:
                return float(x)
            except:
                return 0

        # ==================================
        # БЛОК 1
        # ОБЪЕМ ЗАКАЗОВ
        # ==================================

        orders = np.array([
            clean_number(df.iloc[7, 1]),
            clean_number(df.iloc[7, 2]),
            clean_number(df.iloc[7, 3]),
            clean_number(df.iloc[7, 4]),
        ])

        # ==================================
        # БЛОК 2
        # РЕАЛИЗАЦИИ
        # ==================================

        revenue = np.array([
            clean_number(df.iloc[16, 1]),
            clean_number(df.iloc[16, 2]),
            clean_number(df.iloc[16, 3]),
            clean_number(df.iloc[16, 4]),
        ])

        periods = ["Янв", "Фев", "Мар", "Апр"]

        orders_cum = np.cumsum(orders)
        revenue_cum = np.cumsum(revenue)

        total_orders = orders.sum()
        total_revenue = revenue.sum()
        gap = total_orders - total_revenue

        # ==================================
        # KPI
        # ==================================

        st.subheader("Ключевые показатели")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Объем заказов",
            f"{total_orders:,.0f} ₽".replace(",", " ")
        )

        col2.metric(
            "Реализация",
            f"{total_revenue:,.0f} ₽".replace(",", " ")
        )

        col3.metric(
            "Разрыв (потенциал)",
            f"{gap:,.0f} ₽".replace(",", " ")
        )

        # ==================================
        # ГРАФИК 1
        # ==================================

        st.subheader("Динамика заказов и реализаций")

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            periods,
            orders_cum,
            linewidth=3,
            marker="o",
            label="Объем заказов"
        )

        ax.plot(
            periods,
            revenue_cum,
            linewidth=3,
            marker="o",
            label="Реализация"
        )

        ax.fill_between(
            periods,
            orders_cum,
            revenue_cum,
            where=(orders_cum > revenue_cum),
            alpha=0.25,
            label="Разрыв"
        )

        ax.set_ylabel("₽")
        ax.grid(alpha=0.3)

        ax.legend()

        st.pyplot(fig)

        # ==================================
        # ПЛАН VS ФАКТ
        # ==================================

        st.subheader("Выполнение плана")

        plan = np.array([
            clean_number(df.iloc[40, 1]),
            clean_number(df.iloc[40, 2]),
            clean_number(df.iloc[40, 3]),
            clean_number(df.iloc[40, 4]),
        ])

        fact = np.array([
            clean_number(df.iloc[50, 1]),
            clean_number(df.iloc[50, 2]),
            clean_number(df.iloc[50, 3]),
            clean_number(df.iloc[50, 4]),
        ])

        fig2, ax2 = plt.subplots(figsize=(12, 6))

        x = np.arange(len(periods))
        width = 0.35

        ax2.bar(
            x - width / 2,
            plan,
            width,
            label="План"
        )

        ax2.bar(
            x + width / 2,
            fact,
            width,
            label="Факт"
        )

        ax2.set_xticks(x)
        ax2.set_xticklabels(periods)

        ax2.legend()

        st.pyplot(fig2)

        # ==================================
        # ВКЛАД НАПРАВЛЕНИЙ
        # ==================================

        st.subheader("Вклад направлений в реализацию")

        categories = [
            "Визы",
            "Миграция",
            "MICE",
            "Билеты",
            "Сувениры"
        ]

        values = [
            clean_number(df.iloc[16, 6]),
            clean_number(df.iloc[17, 6]),
            clean_number(df.iloc[18, 6]),
            clean_number(df.iloc[19, 6]),
            clean_number(df.iloc[20, 6]),
        ]

        fig3, ax3 = plt.subplots(figsize=(12, 6))

        ax3.barh(categories, values)

        st.pyplot(fig3)

        # ==================================
        # УПРАВЛЕНЧЕСКИЕ ВЫВОДЫ
        # ==================================

        st.subheader("Управленческие выводы")

        st.markdown(
            f"""
            • Объем заказов составил **{total_orders:,.0f} ₽**.

            • Реализация составила **{total_revenue:,.0f} ₽**.

            • Разрыв между объемом заказов и реализацией составил **{gap:,.0f} ₽**.

            • Показатель отражает различие между моментом создания заказа и моментом признания реализации.

            • Для управления процессом рекомендуется контролировать динамику разрыва и скорость прохождения заказов по этапам обработки.
            """.replace(",", " ")
        )

    except Exception as e:

        st.error("Ошибка обработки данных")
        st.exception(e)
