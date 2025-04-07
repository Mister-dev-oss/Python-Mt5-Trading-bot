import pandas as pd
import pandas_ta as ta

def sma(df, window=14):
    df[f'SMA_{window}'] = ta.sma(df['close'], length=window)
    return df

def ema(df, window=14):
    df[f'EMA_{window}'] = ta.ema(df['close'], length=window)
    return df

def rsi(df, window=14):
    df['RSI'] = ta.rsi(df['close'], length=window)
    return df

def macd(df, fast=12, slow=26, signal=9):
    macd_result = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)
    df['MACD'] = macd_result['MACD_12_26_9']
    df['MACD_signal'] = macd_result['MACDs_12_26_9']
    df['MACD_hist'] = macd_result['MACDh_12_26_9']
    return df

def bollinger_bands(df, window=20):
    bb_result = ta.bbands(df['close'], length=window)
    df['BB_middle'] = bb_result['BBM_20_2.0']
    df['BB_upper'] = bb_result['BBU_20_2.0']
    df['BB_lower'] = bb_result['BBL_20_2.0']
    return df

def stochastic_oscillator(df, window=14, smooth_window=3):
    stoch_result = ta.stoch(df['high'], df['low'], df['close'], k=window, d=smooth_window)
    df['%K'] = stoch_result['STOCHk_14_3_3']
    df['%D'] = stoch_result['STOCHd_14_3_3']
    return df

def parabolic_sar(df, acceleration=0.02, maximum=0.2):
    sar_values = ta.psar(df['high'], df['low'], acceleration=acceleration, max_acceleration=maximum)
    df['SAR'] = sar_values['PSARl_0.02_0.2']
    return df

def apply_indicators(df):
    df = sma(df, 50)
    df = sma(df, 200)
    df = ema(df, 20)
    df = rsi(df)
    df = macd(df)
    df = bollinger_bands(df)
    df = stochastic_oscillator(df)
    df = parabolic_sar(df)
    return df
