import streamlit as st
from datetime import datetime
import pandas as pd

# Inicializa o estado da sessão
if "saldo" not in st.session_state:
    st.session_state.saldo = 0.0
if "extrato" not in st.session_state:
    st.session_state.extrato = []
if "numero_saques" not in st.session_state:
    st.session_state.numero_saques = 0

LIMITE_SAQUES = 3

# Título com estilo
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>Banco Interativo</h1>
""", unsafe_allow_html=True)

# Menu lateral
menu = st.sidebar.radio("Menu", ("Depósito", "Saque", "Extrato", "Resetar Conta"))

# DEPÓSITO
if menu == "Depósito":
    valor_deposito = st.number_input(
        "Informe o valor do depósito:",
        min_value=0.00,
        format="%.2f",
        value=0.00,
        key="valor_deposito_input"
    )
    if st.button("Depositar"):
        if valor_deposito > 0:
            st.session_state.saldo += valor_deposito
            agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            st.session_state.extrato.append({"Data": agora, "Tipo": "Depósito", "Valor": valor_deposito})
            st.success(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
        else:
            st.error("O valor precisa ser maior que zero.")

# SAQUE
elif menu == "Saque":
    valor_saque = st.number_input(
        "Informe o valor do saque:",
        min_value=0.00,
        format="%.2f",
        value=0.00,
        key="valor_saque_input"
    )
    if st.button("Sacar"):
        if st.session_state.numero_saques >= LIMITE_SAQUES:
            st.warning("Limite de saques diários atingido.")
        elif valor_saque > st.session_state.saldo:
            st.error("Saldo insuficiente.")
        elif valor_saque <= 0:
            st.error("O valor precisa ser maior que zero.")
        else:
            st.session_state.saldo -= valor_saque
            agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            st.session_state.extrato.append({"Data": agora, "Tipo": "Saque", "Valor": -valor_saque})
            st.session_state.numero_saques += 1
            st.success(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")

# EXTRATO
elif menu == "Extrato":
    st.subheader("📄 Histórico de Transações")
    if not st.session_state.extrato:
        st.info("Nenhuma movimentação realizada.")
    else:
        df = pd.DataFrame(st.session_state.extrato)
        df['Valor'] = df['Valor'].map(lambda x: f"R$ {x:.2f}")
        st.dataframe(df, use_container_width=True)

    st.metric("💰 Saldo atual", f"R$ {st.session_state.saldo:.2f}")

    grafico = pd.DataFrame(st.session_state.extrato)
    if not grafico.empty:
        grafico['Acumulado'] = grafico['Valor'].cumsum()
        st.line_chart(grafico.set_index('Data')[['Acumulado']])

# RESETAR CONTA
elif menu == "Resetar Conta":
    if st.button("Resetar Tudo"):
        st.session_state.saldo = 0.0
        st.session_state.extrato = []
        st.session_state.numero_saques = 0
        st.success("Conta resetada com sucesso!")
