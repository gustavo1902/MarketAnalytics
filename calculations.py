import pandas as pd
import numpy as np

def calculate_log_returns(df: pd.DataFrame, col_name: str = 'Close') -> pd.DataFrame:
    """
    Calcula os retornos logarítmicos, que são mais precisos para modelagem financeira
    do que a variação percentual simples.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos.
        col_name (str): Nome da coluna de preço (padrão 'Close').
        
    Returns:
        pd.DataFrame: DataFrame com a nova coluna 'Log_Returns'.
    """
    try:
        df = df.copy()
        # Log Return = ln(Pt / Pt-1)
        df['Log_Returns'] = np.log(df[col_name] / df[col_name].shift(1))
        return df
    except Exception as e:
        print(f"Erro ao calcular retornos logarítmicos: {e}")
        return df

def calculate_derivatives(df: pd.DataFrame, col_name: str = 'Close') -> pd.DataFrame:
    """
    Aplica Cálculo Discreto para encontrar velocidade e aceleração do preço.
    
    Conceito:
    - 1ª Derivada (Velocity): Taxa de variação do preço (Momentum).
    - 2ª Derivada (Acceleration): Taxa de variação do Momentum (Mudança de tendência).
    """
    df = df.copy()
    
    # 1ª Derivada Discreta (Velocidade): f'(x) ≈ f(x) - f(x-1)
    df['Velocity'] = df[col_name].diff()
    
    # 2ª Derivada Discreta (Aceleração): f''(x) ≈ f'(x) - f'(x-1)
    df['Acceleration'] = df['Velocity'].diff()
    
    return df

def calculate_volatility(df: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """
    Calcula a volatilidade histórica (desvio padrão móvel).
    Window = 21 dias (aproximadamente 1 mês útil de mercado).
    """
    df = df.copy()
    if 'Log_Returns' not in df.columns:
        df = calculate_log_returns(df)
        
    # Volatilidade anualizada 
    df['Volatility_21d'] = df['Log_Returns'].rolling(window=window).std() * np.sqrt(252)
    
    return df

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline principal que executa todos os cálculos."""
    if df.empty:
        return df
        
    df = calculate_log_returns(df)
    df = calculate_derivatives(df)
    df = calculate_volatility(df)
    
    # Limpeza de NaNs gerados pelos cálculos de diff e rolling
    df.dropna(inplace=True)
    
    return df