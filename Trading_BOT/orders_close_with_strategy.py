import MetaTrader5 as mt5

def check_close_positions():
    positions = mt5.positions_get()
    if positions is None or len(positions) == 0:
        print('No open positions')
        return
    for pos in positions:
        contract_size = mt5.symbol_info(pos.symbol).trade_contract_size
        profit_percent = (pos.profit / (pos.volume * contract_size))
        print(f"Position {pos.ticket} on {pos.symbol}: current profit {profit_percent:.2f}%")
        if profit_percent >= 1.5:
            if pos.type == 0:
                price = mt5.symbol_info_tick(pos.symbol).bid
                order_type = mt5.ORDER_TYPE_SELL
            else:
                price = mt5.symbol_info_tick(pos.symbol).ask
                order_type = mt5.ORDER_TYPE_BUY
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 10,
                "magic": 123456,
                "comment": "Closed with profit",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK
            }
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Closed order {pos.ticket} on {pos.symbol} with profit of {profit_percent:.2f}%")
                return
            else:
                print(f"Error closing ticket {pos.ticket}: {result.retcode if result else 'No response'}")
                if result:
                    print(f"Error details: {result.comment}")
                return
    print(f'Open positions: {[pos.ticket for pos in mt5.positions_get()]} ')
    return