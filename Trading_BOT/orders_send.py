import MetaTrader5 as mt5

def send_order(symbol, order_type, lot_size=0.01):
    if not mt5.initialize():
        print("Error connecting to MT5")
        return False

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found")
        return False

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Symbol {symbol} not available for trading")
            return False

    order_types = {
        "buy": mt5.ORDER_TYPE_BUY,
        "sell": mt5.ORDER_TYPE_SELL
    }

    min_volume = float(symbol_info.volume_min)
    max_volume = float(symbol_info.volume_max)
    
    if lot_size < min_volume:
        lot_size = min_volume
        print(f"Volume adjusted to minimum allowed: {min_volume}")
    elif lot_size > max_volume:
        lot_size = max_volume
        print(f"Volume adjusted to maximum allowed: {max_volume}")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Unable to get price for {symbol}")
        return False

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_types[order_type],
        "price": tick.ask if order_type == "buy" else tick.bid,
        "deviation": 10,
        "magic": 123456,
        "comment": "Trade by bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
    }

    order_result = mt5.order_send(request)
    
    if order_result is None:
        print("Error: No response from server")
        return False

    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Error sending order: {order_result.comment}")
        print(f"Error code: {order_result.retcode}")
        return False

    print(f"Order {order_type} executed successfully!")
    return True

def execute_trade(symbol, order_buy, order_sell):
    if order_buy:
        send_order(symbol, "buy")
    elif order_sell:
        send_order(symbol, "sell")
    else:
        print("No trading signal detected")
        return
