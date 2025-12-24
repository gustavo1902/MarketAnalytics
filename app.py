import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="Market Math Analytics", layout="wide")

st.title(" Análise Matemática de Ativos")
st.markdown("Dashboard para análise de variação de preço usando **Cálculo Numérico**.")