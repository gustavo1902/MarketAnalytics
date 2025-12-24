import pandas as pd
import numpy as np

def calculate_log_returns(df: pd.DataFrame, col_name: str = 'Close') -> pd.DataFrame:
    """Calcula retornos logarítmicos."""
    df = df.copy()
    df['Log_Returns'] = np.log(df[col_name] / df[col_name].shift(1))
    return df

def calculate_derivatives(df: pd.DataFrame, col_name: str = 'Close') -> pd.DataFrame:
    """Calcula Velocidade (1ª Derivada) e Aceleração (2ª Derivada)."""
    df = df.copy()
    df['Velocity'] = df[col_name].diff()
    df['Acceleration'] = df['Velocity'].diff()
    return df

def calculate_volatility(df: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Calcula volatilidade histórica anualizada (janela de 21 dias)."""
    df = df.copy()
    if 'Log_Returns' not in df.columns:
        df = calculate_log_returns(df)
    df['Volatility_21d'] = df['Log_Returns'].rolling(window=window).std() * np.sqrt(252)
    return df

def calculate_sma(df: pd.DataFrame, window: int = 30, col_name: str = 'Close') -> pd.DataFrame:
    """Calcula a Média Móvel Simples (SMA)."""
    df = df.copy()
    df[f'SMA_{window}'] = df[col_name].rolling(window=window).mean()
    return df

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo de processamento."""
    if df.empty:
        return df
    
    # Executa todos os cálculos em cadeia
    df = calculate_log_returns(df)
    df = calculate_derivatives(df)
    df = calculate_volatility(df)
    df = calculate_sma(df, window=30) # Adicionando SMA de 30 dias
    
    df.dropna(inplace=True)
    return df