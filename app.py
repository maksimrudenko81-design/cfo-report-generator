import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CFO Панель", layout="wide")

st.title("📊 CFO ПАНЕЛЬ УПРАВЛЕНИЯ")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        # =========================
        # ЗАГРУЗКА ДАННЫХ
        # =========================
        gid = "1443532418"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

        df = pd.read_csv(url)
        df = df.dropna(how="all")

        st.success("Данные загружены")
        st.dataframe(df)

        # =========================
        # ЧИСТКА ДАННЫХ
        # =========================
        def clean(x):
            return float(str(x).replace("\u00a0", "").replace(" ", "").replace(",", "."))

        # =========================
        # ПОИСК БЛОКОВ
        # =========================
        def find_row(keyword):
            return df[df.iloc[:, 0].astype(str).str.contains(keyword, na=False)]

        orders_block = find_row("Общий итог").iloc[0]
        revenue_block = find_row("Общий итог").iloc[1]

        orders = np.array([clean(x) for x in orders_block.values[1:5]])
        revenue = np.array([clean(x) for x in revenue_block.values[1:5]])

        # =========================
        # ПЕРИОДЫ (РУССКИЕ)
        # =========================
        periods = ["Янв", "Фев", "Мар", "Апр"]

        orders_cum = np.cumsum(orders)
        revenue_cum = np.cumsum(revenue)

        total_orders = orders.sum()
        total_revenue = revenue.sum()
        gap = total_orders - total_revenue

        # =========================
        # KPI
        # =========================
        st.subheader("🔴 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ")

        c1, c2, c3 = st.columns(3)
        c1.metric("Отработано заказов", f"{total_orders:,.0f}")
        c2.metric("Выручка", f"{total_revenue:,.0f}")
        c3.metric("Разрыв (потенциал)", f"{gap:,.0f}")

        # =========================
        # GAP ГРАФИК
        # =========================
        st.subheader("📉 Динамика заказов и выручки (накопительно)")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(periods, orders_cum, marker="o", linewidth=2, label="Заказы")
        ax.plot(periods, revenue_cum, marker="s", linewidth=2, label="Выручка")

        ax.fill_between(
            periods,
            orders_cum,
            revenue_cum,
            where=(orders_cum > revenue_cum),
            alpha=0.25,
            color="red",
            label="Разрыв"
        )

        ax.set_title("Накопительная динамика: Заказы vs Выручка")
        ax.set_ylabel("Млн руб.")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend()

        st.pyplot(fig)

        # =========================
        # PLAN VS FACT
        # =========================
        st.subheader("📊 План vs Факт")

        plan_block = find_row("нарастающим план")
        fact_block = find_row("нарастающим факт")

        plan = np.array([clean(x) for x in plan_block.iloc[0].values[1:5]])
        fact = np.array([clean(x) for x in fact_block.iloc[0].values[1:5]])

        fig2, ax2 = plt.subplots(figsize=(10, 4))

        ax2.bar(periods, plan, alpha=0.4, label="План")
        ax2.bar(periods, fact, alpha=0.8, label="Факт")

        ax2.set_title("План vs Факт (накопительно)")
        ax2.set_ylabel("Млн руб.")
        ax2.grid(True, axis="y", linestyle="--", alpha=0.3)
        ax2.legend()

        st.pyplot(fig2)

        # =========================
        # УПРАВЛЕНЧЕСКИЕ ВЫВОДЫ
        # =========================
        st.subheader("🧠 УПРАВЛЕНЧЕСКИЕ ВЫВОДЫ")

        st.markdown(f"""
**1. Финансовый разрыв:**  
Формируется потенциальная выручка **{gap:,.0f}**, ещё не признанная в P&L.

**2. Динамика:**  
Есть разрыв между выполнением и признанием выручки → эффект накопления результата.

**3. Бизнес-модель:**  
Рост идёт неравномерно по периодам, с сильной концентрацией в отдельных месяцах.

**4. Риск:**  
Требуется контроль лагов между выполнением и признанием выручки.

**5. Вывод:**  
Бизнес создаёт ценность быстрее, чем она отражается в выручке.
""")

    except Exception as e:
        st.error("Ошибка обработки данных")
        st.exception(e)
