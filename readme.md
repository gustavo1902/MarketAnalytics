## Market Analytics

Uma ferramenta de análise quantitativa desenvolvida para monitorar a dinâmica de ativos financeiros através de Cálculo Numérico e Estatística. A aplicação processa dados de mercado em tempo real para visualizar momentum, volatilidade e tendências de aceleração de preços.

---

## Funcionalidades Principais

- **Análise Comparativa**: Comparação simultânea de dois ativos financeiros listados no Yahoo Finance.
- **Métricas de Cálculo**: Visualização da 1ª Derivada (Velocidade) e 2ª Derivada (Aceleração) da curva de preços.
- **Detecção de Anomalias**: Identificação visual automática de dias com volatilidade extrema (acima do percentil 90).
- **Indicadores Técnicos**: Média Móvel Simples (SMA) de 30 dias para análise de tendência.
- **Visualização Interativa**: Gráficos dinâmicos com zoom e tooltips precisos utilizando Plotly.

---

## Fundamentação Matemática

O projeto aplica métodos de cálculo discreto em séries temporais financeiras para extrair insights além do preço nominal:

- **Retornos Logarítmicos**: Utilizados preferencialmente sobre a variação percentual simples devido às suas propriedades de aditividade temporal e simetria.
  $$R_t = \ln(P_t / P_{t-1})$$
- **Velocidade (1ª Derivada)**: Representa a taxa de variação diária do preço ($v$).
  $$v(t) \approx P_t - P_{t-1}$$
- **Aceleração (2ª Derivada)**: Representa a taxa de variação do momentum ($a$). Utilizada para identificar exaustão de tendências (ex: preço sobe, mas aceleração desacelera).
  $$a(t) \approx v(t) - v(t-1)$$
- **Volatilidade Histórica**: Desvio padrão móvel dos retornos logarítmicos, anualizado para 252 dias úteis.

---

## Stack Tecnológico

- **Linguagem**: Python 3.10+
- **Interface**: Streamlit (Framework Web)
- **Processamento de Dados**: Pandas & NumPy (Vetorização e Álgebra Linear)
- **Visualização**: Plotly Graph Objects (Renderização Interativa)
- **Fonte de Dados**: `yfinance` API

---

## Instalação e Execução

Requer Python 3.8 ou superior.

1. Clone o repositório:
   ```bash
   git clone https://github.com/gustavo1902/MarketAnalytics.git
   cd MarketAnalytics
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

---

## Estrutura do Projeto

A arquitetura segue o princípio de separação de responsabilidades:

- `app.py`: Camada de apresentação e controle de UI (Streamlit).
- `calculations.py`: Camada de lógica de negócios, contendo as funções puras de cálculo matemático e transformação de dados.
- `requirements.txt`: Lista de dependências com versões fixadas para reprodutibilidade.