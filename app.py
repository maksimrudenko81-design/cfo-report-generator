import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CFO Board Dashboard", layout="wide")

st.title("📊 CFO BOARD DASHBOARD")

sheet_id = st.text_input("Google Sheets ID")

if st.button("Загрузить данные"):

    # =========================
    # LOAD
    # =========================
    gid = "1443532418"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    df = pd.read_csv(url)
    df = df.dropna(how="all")

    # =========================
    # CORE METRICS
    # =========================
    orders = np.array(df.iloc[5, 1:5].astype(str).str.replace("\u00a0","").str.replace(" ",""), dtype=float)
    revenue = np.array(df.iloc[16, 1:5].astype(str).str.replace("\u00a0","").str.replace(" ",""), dtype=float)

    periods = ["P1","P2","P3","P4"]

    orders_cum = np.cumsum(orders)
    revenue_cum = np.cumsum(revenue)

    total_orders = orders.sum()
    total_revenue = revenue.sum()
    gap = total_orders - total_revenue

    # =========================
    # KPI BLOCK (BOARD STYLE)
    # =========================
    st.subheader("🔴 KEY BOARD KPI")

    c1, c2, c3 = st.columns(3)
    c1.metric("Отработано заказов", f"{total_orders:,.0f}")
    c2.metric("Выручка", f"{total_revenue:,.0f}")
    c3.metric("Gap (потенциал / риск)", f"{gap:,.0f}")

    # =========================
    # GAP CHART (BOARD STYLE)
    # =========================
    st.subheader("📉 Orders vs Revenue (Cumulative Gap)")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(periods, orders_cum, label="Orders", linewidth=2)
    ax.plot(periods, revenue_cum, label="Revenue", linewidth=2)

    ax.fill_between(
        periods,
        orders_cum,
        revenue_cum,
        where=(orders_cum > revenue_cum),
        alpha=0.25,
        color="red"
    )

    ax.text(0.5, max(orders_cum.max(), revenue_cum.max())*0.95,
            f"Total Gap: {gap:,.0f}",
            fontsize=12, fontweight="bold")

    ax.set_title("Accumulated Execution vs Revenue Recognition")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()

    st.pyplot(fig)

    # =========================
    # PLAN VS FACT (SIMPLIFIED BOARD VIEW)
    # =========================
    st.subheader("📊 Plan vs Fact (Key Business Drivers)")

    # берём кусок из плана и факта (упрощённо)
    plan = np.array(df.iloc[40, 1:5].astype(str).str.replace("\u00a0","").str.replace(" ",""), dtype=float)
    fact = np.array(df.iloc[50, 1:5].astype(str).str.replace("\u00a0","").str.replace(" ",""), dtype=float)

    labels = ["P1","P2","P3","P4"]

    fig2, ax2 = plt.subplots(figsize=(10,4))

    ax2.bar(labels, plan, alpha=0.4, label="Plan")
    ax2.bar(labels, fact, alpha=0.8, label="Fact")

    ax2.set_title("Plan vs Fact (Total Company)")
    ax2.grid(True, axis="y", linestyle="--", alpha=0.3)
    ax2.legend()

    st.pyplot(fig2)

    # =========================
    # BOARD INSIGHTS (JUDGEMENT LAYER)
    # =========================
    st.subheader("🧠 Управленческие выводы (Board Level)")

    st.markdown(f"""
**1. Финансовый разрыв:**  
Формируется потенциальная выручка **{gap:,.0f}**, не признанная в текущем периоде.

**2. Динамика исполнения:**  
Наблюдается асинхронность между выполнением и признанием выручки → эффект накопления.

**3. Структура бизнеса:**  
Основной объём формирует MICE-сегмент (ключевой драйвер модели).

**4. Риски исполнения:**  
Есть периодические провалы, требующие анализа (особенно в среднем горизонте).

**5. Управленческий вывод:**  
Бизнес растёт не линейно — требуется управление лагом между выполнением и признанием выручки.
""")
