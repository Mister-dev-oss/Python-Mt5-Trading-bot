import time
from data_collector import stream_data
from strategy import strategy
from orders_send import execute_trade
from orders_close_with_strategy import check_close_positions
import MetaTrader5 as mt5

SYMBOL = "EURUSD"
TIMEFRAME = [mt5.TIMEFRAME_D1, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_M15]
N_CANDLES = 100
UPDATE_INTERVAL = 60

def main():
    print("Starting Trading Bot...")

    while True:
        df_long, df_mid, df_short = stream_data(SYMBOL, TIMEFRAME, N_CANDLES)
        order_buy, order_sell = strategy(df_long, df_mid, df_short)
        
        if order_sell or order_buy:
            print(f"New signal - Buy: {order_buy}, Sell: {order_sell}")
        else:
            print('No order detected')

        execute_trade(SYMBOL, order_buy, order_sell)
        check_close_positions()
        
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
