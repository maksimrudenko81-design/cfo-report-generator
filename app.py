import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CFO Board Dashboard", layout="wide")

st.title("📊 CFO BOARD DASHBOARD")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    try:
        # =========================
        # LOAD DATA
        # =========================
        gid = "1443532418"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

        df = pd.read_csv(url)
        df = df.dropna(how="all")

        st.success("Данные загружены")
        st.dataframe(df)

        # =========================
        # CLEAN FUNCTION
        # =========================
        def clean(x):
            return float(str(x).replace("\u00a0", "").replace(" ", "").replace(",", "."))

        # =========================
        # FIND ROWS (NO HARDCODE)
        # =========================
        def find_row(keyword):
            return df[df.iloc[:, 0].astype(str).str.contains(keyword, na=False)]

        # Orders / Revenue
        orders_block = find_row("Общий итог").iloc[0]
        revenue_block = find_row("Общий итог").iloc[1]

        orders = np.array([clean(x) for x in orders_block.values[1:5]])
        revenue = np.array([clean(x) for x in revenue_block.values[1:5]])

        periods = ["P1", "P2", "P3", "P4"]

        orders_cum = np.cumsum(orders)
        revenue_cum = np.cumsum(revenue)

        total_orders = orders.sum()
        total_revenue = revenue.sum()
        gap = total_orders - total_revenue

        # =========================
        # KPI BLOCK
        # =========================
        st.subheader("🔴 KEY KPI")

        c1, c2, c3 = st.columns(3)
        c1.metric("Отработано заказов", f"{total_orders:,.0f}")
        c2.metric("Выручка", f"{total_revenue:,.0f}")
        c3.metric("Gap (потенциал)", f"{gap:,.0f}")

        # =========================
        # GAP CHART
        # =========================
        st.subheader("📉 Orders vs Revenue (Gap View)")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(periods, orders_cum, marker="o", linewidth=2, label="Orders")
        ax.plot(periods, revenue_cum, marker="s", linewidth=2, label="Revenue")

        ax.fill_between(
            periods,
            orders_cum,
            revenue_cum,
            where=(orders_cum > revenue_cum),
            alpha=0.25,
            color="red"
        )

        ax.set_title("Cumulative Orders vs Revenue")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend()

        st.pyplot(fig)

        # =========================
        # PLAN VS FACT
        # =========================
        st.subheader("📊 Plan vs Fact")

        plan_block = find_row("нарастающим план")
        fact_block = find_row("нарастающим факт")

        plan = np.array([clean(x) for x in plan_block.iloc[0].values[1:5]])
        fact = np.array([clean(x) for x in fact_block.iloc[0].values[1:5]])

        fig2, ax2 = plt.subplots(figsize=(10, 4))

        ax2.bar(periods, plan, alpha=0.4, label="Plan")
        ax2.bar(periods, fact, alpha=0.8, label="Fact")

        ax2.set_title("Plan vs Fact (Cumulative)")
        ax2.grid(True, axis="y", linestyle="--", alpha=0.3)
        ax2.legend()

        st.pyplot(fig2)

        # =========================
        # BOARD INSIGHTS
        # =========================
        st.subheader("🧠 Управленческие выводы")

        st.markdown(f"""
**1. Финансовый разрыв:**  
Формируется потенциальная выручка **{gap:,.0f}**, не признанная в текущем периоде.

**2. Динамика:**  
Наблюдается разрыв между выполнением и признанием выручки → накопление результата.

**3. Бизнес-модель:**  
Основной вклад формируют крупные сервисные блоки (MICE и смежные направления).

**4. Риск:**  
Есть асимметрия между периодами выполнения и признания → требуется контроль лагов.

**5. Вывод:**  
Рост бизнеса идёт рывками, а не линейно — важно управлять накоплением выручки.
""")

    except Exception as e:
        st.error("Ошибка обработки данных")
        st.exception(e)
