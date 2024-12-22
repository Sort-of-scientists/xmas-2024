import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

from src.simulator import Simulator
from src.strategies import GreedyStrategy


def check_and_load_csv(file):
    """Check if the uploaded file is a CSV and load it."""
    if file is not None:
        _, ext = os.path.splitext(file.name)
        if ext.lower() == '.csv':
            try:
                return pd.read_csv(file)
            except Exception as e:
                st.error(f"Ошибка при загрузке CSV файла: {e}")
                return None
        else:
            st.error("Только CSV файлы разрешены!")
            return None
    return None

def set_stage(stage):
    st.session_state.stage = stage


def download_file():
    letters_randoms = {
        'A': [1, 5],
        'B': [2, 6],
        'C': [3, 7],
    }

    pd.DataFrame(letters_randoms).to_csv("result.csv")

st.set_page_config(
    page_title="Своего рода ученые",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="expanded",
)

payments, providers, exchange_rates = None, None, None


# Main Header
st.header("📈 Платежный конвейер")
with st.container():
    with st.expander(label="Инструкция", icon="❓"):
        st.markdown("""
        1. Выберите стратегию минимизации
        2. Загрузите `.csv` файлы в соответсвующие разделы.
        3. Нажмите кнопку **Выполнить стратегию!**
        4. Скачайте результаты
    """)


    strategy_type = st.selectbox(label="Выберите **стратегию** минимизации...", options=["Ожидаемой комиссии", "Ожидаемого времени успешного платежа"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💱 Обменные курсы")
        ex_file = st.file_uploader("Загрузите **обменные курсы**", key="ex_rates", type=['csv'])
        if ex_file:
            with st.spinner("Идет загрузка..."):
                exchange_rates = check_and_load_csv(ex_file)
                if exchange_rates is not None:
                    st.dataframe(exchange_rates.head().style.format(), use_container_width=True)

    with col2:
        st.subheader("💸 Платежи")
        payments_file = st.file_uploader("Загрузите **платежи**", key="payments", type=['csv'])
        if payments_file:
            with st.spinner("Идет загрузка..."):
                payments = check_and_load_csv(payments_file)
                if payments is not None:
                    st.dataframe(payments.head().style.format(), use_container_width=True)

    with col3:
        st.subheader("🏢 Провайдеры")
        providers_file = st.file_uploader("Загрузите **провайдеров**", key="providers", type=['csv'])
        if providers_file:
            with st.spinner("Идет загрузка..."):
                providers = check_and_load_csv(providers_file)
                if providers is not None:
                    st.dataframe(providers.head().style.format(), use_container_width=True)

    if payments is not None and providers is not None and exchange_rates is not None:
        
        strategy = GreedyStrategy(by="processing_time" if strategy_type == "Ожидаемого времени успешного платежа" else "commission")

        simulator = Simulator(payments=payments, providers=providers, currencies=exchange_rates, strategy=strategy)

    if st.button("**Выполнить стратегию!**", use_container_width=True, on_click=set_stage, args=(1,)):
        
        with st.spinner("Пожалуйста, подождите!"):
            history = simulator.simulate(verbose=True)        

        outputs = simulator._get_output_dataframe(history)
        metrics = simulator._compute_metrics(history)
        
        st.markdown(f"😡 Издержки составили: **{metrics['penalty']:.2f}$**")
        st.markdown(f"😎 95% пользователей ожидают подтверждения оплаты меньше, чем **{metrics['processing_time']['mean']:.2f} миллисекунд!**")
        st.markdown(f"😤 Конверсия составила **{metrics['conversion']:.2f}%**")

        st.download_button('Скачать результат', outputs.to_csv().encode("utf-8"), "result.csv", "text/csv", use_container_width=True)