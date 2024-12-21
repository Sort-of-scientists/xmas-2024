import pandas as pd

def set_stage(stage):
    st.session_state.stage = stage


def download_file():
    letters_randoms = {
    'A': [1, 5],
    'B': [2, 6],
    'C': [3, 7],
}
    pd.DataFrame(letters_randoms).to_csv("result.csv")

# Main Header
st.header("📈 Реализация")
with st.container():
    with st.expander("Показать инструкцию"):
        st.write('''
        Охапка дров и **плов** готов
        ''')
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaqmkIlh_VDaMu8lr10CBb_Q9EyKoOT89EJA&s")
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💱 Exchange Rates")
        ex_file = st.file_uploader("Загрузите обменные курсы", key="ex_rates", type=['csv'])
        if ex_file:
            with st.spinner("Идет загрузка..."):
                exchange_rates = check_and_load_csv(ex_file)
                if exchange_rates is not None:
                    st.dataframe(exchange_rates.head().style.format(), use_container_width=True)

    with col2:
        st.subheader("💸 Платежи")
        payments_file = st.file_uploader("Загрузите платежи", key="payments", type=['csv'])
        if payments_file:
            with st.spinner("Идет загрузка..."):
                payments = check_and_load_csv(payments_file)
                if payments is not None:
                    st.dataframe(payments.head().style.format(), use_container_width=True)

    with col3:
        st.subheader("🏢 Провайдеры")
        providers_file = st.file_uploader("Загрузите провайдеров", key="providers", type=['csv'])
        if providers_file:
            with st.spinner("Идет загрузка..."):
                providers = check_and_load_csv(providers_file)
                if providers is not None:
                    st.dataframe(providers.head().style.format(), use_container_width=True)

    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    _, middle, right = st.columns(3)
    if middle.button("**Выполнить стратегию!**", icon="😃", use_container_width=True, on_click=set_stage, args=(1,)):
        middle.markdown("Вы нажали на кнопку!")

    if st.session_state.stage > 0:
        # Some code
        binary_contents = b"example content"
        if right.download_button('Разбудить деда', binary_contents, use_container_width=True): # on_click=set_stage, args=(1,)
            right.markdown("Пиздец") # 
