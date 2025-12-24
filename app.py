import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from calculations import process_data

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
        data = yf.download(ticker, period=periodo)
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        if not data.empty:
            # st.write(data.head()) 

            # Processamento (chama sua função do calculations.py)
            df = process_data(data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Preço de Fechamento")
                st.line_chart(df['Close'])
            
            with col2:
                st.subheader("Aceleração do Preço (2ª Derivada)")
                st.bar_chart(df['Acceleration'])

            st.write("### Estatísticas Descritivas")
            st.dataframe(df.describe())
            
        else:
            st.error(f"Não foi possível baixar dados para o ticker {ticker}. Tente 'PETR4.SA' ou 'AAPL'.")

st.info("Desenvolvido para fins de estudo de Python e Finanças.")