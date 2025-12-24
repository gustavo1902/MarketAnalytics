import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="Market Math Analytics", layout="wide")

st.title(" Análise Matemática de Ativos")
st.markdown("Dashboard para análise de variação de preço usando **Cálculo Numérico**.")

# Input do usuário na barra lateral
sidebar = st.sidebar
ticker = sidebar.text_input("Símbolo do Ativo (Yahoo Finance)", value="PETR4.SA")
periodo = sidebar.selectbox("Período", ["1mo", "3mo", "6mo", "1y"])

if st.button("Analisar"):
    with st.spinner('Baixando dados e calculando derivadas...'):
        #  Aquisição de Dados
        data = yf.download(ticker, period=periodo)
        
        if not data.empty:
            data['Retorno'] = data['Close'].pct_change()
            
            # 1ª Derivada (Velocidade da mudança de preço)
            data['Velocity'] = data['Close'].diff() 
            # 2ª Derivada (Aceleração - indica mudança de tendência)
            data['Acceleration'] = data['Velocity'].diff()

            # Visualização
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Preço de Fechamento")
                st.line_chart(data['Close'])
            
            with col2:
                st.subheader("Aceleração do Preço (2ª Derivada)")
                st.caption("Picos indicam mudanças bruscas de tendência")
                st.bar_chart(data['Acceleration'])

            # Estatísticas
            st.write("### Estatísticas Descritivas")
            st.dataframe(data.describe())
            
        else:
            st.error("Ativo não encontrado ou sem dados.")

st.info("Desenvolvido para fins de estudo de Python e Finanças.")