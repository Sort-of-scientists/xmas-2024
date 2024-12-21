import streamlit as st
import pandas as pd
import os

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


# Theme Configuration
st.set_page_config(page_title="CSV File Loader", layout="wide", page_icon="📊")

st.markdown(
    """
<style>
button {
    height: auto;
    padding-top: 15px !important;
    padding-bottom: 10px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Main Header
st.header("📈 Data Management Dashboard")

# Sidebar Content
# with st.sidebar:
#     st.subheader("🔧 Выбор стратегии:")
#     strategy = st.selectbox("Выберите стратегию:", ["Время", "Прибыль"])
#     st.markdown(f"Выбранная стратегия: **{strategy.split('(')[0].strip()}**")
#     st.info("Пожалуйста загрузите необходимые **.csv** файлы, а также выберите **стратегию**")


# Create three columns for file uploaders
# col0, col1, col2, col3 = st.rows(4)


with st.container():
    with st.expander("Показать инструкцию"):
        st.write('''
        Охапка дров и плов готов
        ''')
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaqmkIlh_VDaMu8lr10CBb_Q9EyKoOT89EJA&s")

    st.subheader("🔧 Выбор стратегии:")
    strategy = st.selectbox("Выберите стратегию:", ["Время", "Прибыль"], key='strategy')
    st.markdown(f"Выбранная стратегия: **{strategy.split('(')[0].strip()}**")
    st.info("Пожалуйста загрузите необходимые **.csv** файлы, а также выберите **стратегию**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💱 Exchange Rates")
        ex_file = st.file_uploader("Загрузите Exchange Rates CSV", key="ex_rates", type=['csv'])
        if ex_file:
            with st.spinner("Идет загрузка..."):
                exchange_rates = check_and_load_csv(ex_file)
                if exchange_rates is not None:
                    st.dataframe(exchange_rates.head().style.format(), use_container_width=True)

    with col2:
        st.subheader("💸 Payments")
        payments_file = st.file_uploader("Загрузите Payments CSV", key="payments", type=['csv'])
        if payments_file:
            with st.spinner("Идет загрузка..."):
                payments = check_and_load_csv(payments_file)
                if payments is not None:
                    st.dataframe(payments.head().style.format(), use_container_width=True)

    with col3:
        st.subheader("🏢 Providers")
        providers_file = st.file_uploader("Загрузите Providers CSV", key="providers", type=['csv'])
        if providers_file:
            with st.spinner("Идет загрузка..."):
                providers = check_and_load_csv(providers_file)
                if providers is not None:
                    st.dataframe(providers.head().style.format(), use_container_width=True)

    _, middle, _ = st.columns(3)
    if middle.button("Выполнить стратегию!", icon="😃", use_container_width=True):
        middle.markdown("You clicked the emoji button.")