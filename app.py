import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from calculations import process_data

# Configuração da Página
st.set_page_config(page_title="Market Math Analytics", layout="wide")

st.title(" Market Math Analytics")
st.markdown("Análise avançada de ativos usando **Cálculo Numérico** e **Estatística**.")

# --- SIDEBAR DE CONTROLES ---
st.sidebar.header("Configurações")
ticker1 = st.sidebar.text_input("Ativo Principal", value="PETR4.SA").upper()
comparar = st.sidebar.checkbox("Comparar com outro ativo?")
ticker2 = ""
if comparar:
    ticker2 = st.sidebar.text_input("Segundo Ativo", value="VALE3.SA").upper()

periodo = st.sidebar.selectbox("Período", ["3mo", "6mo", "1y", "2y", "5y"])
mostrar_sma = st.sidebar.checkbox("Mostrar Média Móvel (30 dias)", value=True)
marcar_volatilidade = st.sidebar.checkbox("Marcar Alta Volatilidade", value=True)

# --- FUNÇÃO AUXILIAR DE DOWNLOAD ---
def carregar_ativo(simbolo):
    if not simbolo: return None
    try:
        dados = yf.download(simbolo, period=periodo)
        if isinstance(dados.columns, pd.MultiIndex):
            dados.columns = dados.columns.get_level_values(0)
        
        if dados.empty: return None
        return process_data(dados)
    except Exception as e:
        st.error(f"Erro ao carregar {simbolo}: {e}")
        return None

if st.sidebar.button("Analisar Ativos"):
    with st.spinner('Processando dados...'):
        df1 = carregar_ativo(ticker1)
        df2 = carregar_ativo(ticker2) if comparar and ticker2 else None

        if df1 is not None:            
            # Gráfico de Preço + SMA + Volatilidade
            fig_price = go.Figure()

            # Linha do Ativo 1
            fig_price.add_trace(go.Scatter(x=df1.index, y=df1['Close'], mode='lines', name=ticker1))
            
            # Média Móvel Ativo 1
            if mostrar_sma:
                fig_price.add_trace(go.Scatter(
                    x=df1.index, y=df1['SMA_30'], 
                    mode='lines', name=f'SMA 30 ({ticker1})', 
                    line=dict(dash='dot', width=1)
                ))

            # Marcadores de Alta Volatilidade Ativo 1
            if marcar_volatilidade:
                # Definindo "Alta Volatilidade" como o top 10% (percentil 90)
                limite_vol = df1['Volatility_21d'].quantile(0.90)
                pontos_criticos = df1[df1['Volatility_21d'] > limite_vol]
                
                fig_price.add_trace(go.Scatter(
                    x=pontos_criticos.index, 
                    y=pontos_criticos['Close'],
                    mode='markers',
                    name=f'Alta Volatilidade ({ticker1})',
                    marker=dict(color='red', size=8, symbol='x')
                ))

            # Linha do Ativo 2 
            if df2 is not None:
                fig_price.add_trace(go.Scatter(
                    x=df2.index, y=df2['Close'], 
                    mode='lines', name=ticker2,
                    line=dict(color='orange')
                ))

            fig_price.update_layout(title="Histórico de Preços & Volatilidade", xaxis_title="Data", yaxis_title="Preço (R$)")
            st.plotly_chart(fig_price, use_container_width=True)

            # Gráfico de Derivadas (Aceleração)
            st.subheader("Física do Mercado: Aceleração de Preço")
            fig_acc = go.Figure()
            
            fig_acc.add_trace(go.Bar(x=df1.index, y=df1['Acceleration'], name=f'Aceleração {ticker1}'))
            
            if df2 is not None:
                 fig_acc.add_trace(go.Bar(x=df2.index, y=df2['Acceleration'], name=f'Aceleração {ticker2}', opacity=0.5))

            fig_acc.update_layout(title="2ª Derivada (Aceleração)", xaxis_title="Data", yaxis_title="Aceleração")
            st.plotly_chart(fig_acc, use_container_width=True)

            # --- EXPLICAÇÃO MATEMÁTICA ---
            with st.expander(" Explicação Matemática (Clique para abrir)"):
                st.markdown(r"""                
                Utilizamos **Cálculo Diferencial Discreto** para entender a dinâmica do preço.
                
                #### 1. Velocidade (1ª Derivada)
                Representa o **Momentum** ou a mudança diária do preço.
                $$
                v(t) = P_t - P_{t-1}
                $$
                
                #### 2. Aceleração (2ª Derivada)
                Representa a **taxa de variação do Momentum**. É crucial para identificar inversões de tendência.
                * Se o preço sobe ($v > 0$) mas a aceleração é negativa ($a < 0$), a tendência de alta está perdendo força (exaustão).
                $$
                a(t) = v(t) - v(t-1)
                $$
                
                #### 3. Volatilidade
                Calculada via desvio padrão móvel dos retornos logarítmicos, anualizada.
                $$
                \sigma = \mathrm{std}\!\left(
                \ln\left(\frac{P_t}{P_{t-1}}\right)
                \right)\times\sqrt{252}
                $$
                """)
                
        else:
            st.warning("Nenhum dado encontrado para o ativo principal.")