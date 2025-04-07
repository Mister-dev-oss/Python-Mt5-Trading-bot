import pandas as pd
import MetaTrader5 as mt5

def strategy(long, mid, short):
    
    order_buy = False
    order_sell = False

    # Segnale Long
    if mid['RSI'].iloc[-1] < 30 and short['MACD'].iloc[-1] > short['MACD_signal'].iloc[-1] and long['close'].iloc[-1] > long['SMA_50'].iloc[-1]:
        order_buy = True
        return order_buy, order_sell
    
    # Segnale Short
    elif mid['RSI'].iloc[-1] > 70 and short['MACD'].iloc[-1] < short['MACD_signal'].iloc[-1] and long['close'].iloc[-1] < long['SMA_50'].iloc[-1]:
        order_sell = True
        return order_buy, order_sell
    
    else:
        return order_buy, order_sell

