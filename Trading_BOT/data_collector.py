import MetaTrader5 as mt5
import pandas as pd
from indicators import apply_indicators

def connect_mt5():
    if not mt5.initialize():
        print('Error connecting to MT5')
        return False
    else:
        return True

def get_data(symbol, timeframe, n_candles):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def stream_data(symbol, timeframes, n_candles):
    if not connect_mt5():
        return
    
    timeframe_data = {}
    for timeframe in timeframes:
        df = get_data(symbol, timeframe, n_candles)
        df = apply_indicators(df)
        timeframe_data[timeframe] = df
    timeframe_data_list = list(timeframe_data)
    df_long = timeframe_data[timeframe_data_list[0]]
    df_mid = timeframe_data[timeframe_data_list[1]]
    df_short = timeframe_data[timeframe_data_list[2]]
    return df_long, df_mid, df_short
        