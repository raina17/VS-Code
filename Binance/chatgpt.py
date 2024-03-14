from keys import Key, Secret
from binance.um_futures import UMFutures
import ta
import pandas as pd
from time import sleep
from binance.error import ClientError

client = UMFutures(key=Key, secret=Secret)

volume = 20
leverage = 20
type = 'ISOLATED'
qty = 100

# Dynamic take profit and stop loss parameters
def calculate_tp_sl(symbol):
    kl = klines(symbol)
    atr = ta.volatility.average_true_range(kl.High, kl.Low, kl.Close)
    atr_multiplier = 3  # Adjust as needed
    tp = atr.iloc[-1] * atr_multiplier
    sl = atr.iloc[-1] * atr_multiplier * 0.5  # Adjust as needed
    return tp, sl

def get_balance_usdt():
    try:
        response = client.balance(recvWindow=6000)
        for elem in response:
            if elem['asset'] == 'USDT':
                return float(elem['balance'])
    except ClientError as error:
        print(
            "Error:", error
        )   

def get_tickers_usdt():
    coins = []
    resp = client.ticker_price()
    for elem in resp:
        if 'USDT' in elem['symbol']:
            coins.append(elem['symbol'])
    return coins

def klines(symbol):
    try:
        resp = pd.DataFrame(client.klines(symbol, '1m'))
        resp = resp.iloc[:,:6]
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        resp = resp.set_index('Time')
        resp.index = pd.to_datetime(resp.index, unit = 'ms')
        resp = resp.astype(float)
        return resp
    except ClientError as error:
        print(
            "Error:", error
        )
        
def set_leverage(symbol, level):
    try:
        response = client.change_leverage(
            symbol= symbol, leverage= level, recvWindow=6000
        )
        print (response)
    except ClientError as error:
        print(
            "Error:", error
        )

def set_mode(symbol ,type):
    try:
        response = client.change_margin_type(
            symbol=symbol,  marginType=type , recvWindow=6000
        )
        print(response)
    except ClientError as error:
        print(
            "Error:", error
        )

def get_price_precision(symbol):
    resp = client.exchange_info()['symbols']
    for elem in resp:
        if elem ['symbol'] == symbol:
            return elem['pricePrecision']
     
def get_qty_precision(symbol):
    resp = client.exchange_info()['symbols']
    for elem in resp:
        if elem ['symbol'] == symbol:
            return elem['quantityPrecision']

def open_order(symbol, side, tp, sl):
    price = float(client.ticker_price(symbol)['price'])
    qty_precision = get_qty_precision(symbol)
    price_precision = get_price_precision(symbol)
    qty = round(volume / price, qty_precision)
    
    if side == 'buy':
        try:
            resp1 = client.new_order(symbol=symbol, side='BUY', type='LIMIT', quantity=qty, timeInForce='GTC', price=price)
            print(symbol, side, "placing order")
            print(resp1)
            sleep(2)
            # Calculate stop-loss and take-profit prices
            sl_price = round(price - sl, price_precision)
            tp_price = round(price + tp, price_precision)
            resp2 = client.new_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=qty, timeInForce='GTC', stopPrice=sl_price)
            print(resp2)
            sleep(2)
            resp3 = client.new_order(symbol=symbol, side='SELL', type='TAKE_PROFIT_MARKET', quantity=qty, timeInForce='GTC', stopPrice=tp_price)
            print(resp3)
        except ClientError as error:
            print(
                "Error:", error
            )
    elif side == 'sell':
        try:
            resp1 = client.new_order(symbol=symbol, side='SELL', type='LIMIT', quantity=qty, timeInForce='GTC', price=price)
            print(symbol, side, "placing order")
            print(resp1)
            sleep(2)
            # Calculate stop-loss and take-profit prices
            sl_price = round(price + sl, price_precision)
            tp_price = round(price - tp, price_precision)
            resp2 = client.new_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=qty, timeInForce='GTC', stopPrice=sl_price)
            print(resp2)
            sleep(2)
            resp3 = client.new_order(symbol=symbol, side='BUY', type='TAKE_PROFIT_MARKET', quantity=qty, timeInForce='GTC', stopPrice=tp_price)
            print(resp3)
        except ClientError as error:
            print(
                "Error:", error
            )

def get_pos():
    try:
        resp = client.get_position_risk()
        pos = []
        for elem in resp:
            if float(elem['positionAmt']) != 0:
                pos.append(elem['symbol'])
        return pos
    except ClientError as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def check_orders():
    try:
        response = client.get_orders(recvWindow=6000)
        sym = []
        for elem in response:
            sym.append(elem['symbol'])
        return sym
    except ClientError as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

# Close open orders for the needed symbol. If one stop order is executed and another one is still there
def close_open_orders(symbol):
    try:
        response = client.cancel_open_orders(symbol=symbol, recvWindow=6000)
        print(response)
    except ClientError as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


# Strategy. Can use any other:
def str_signal(symbol):
    kl = klines(symbol)
    rsi = ta.momentum.RSIIndicator(kl.Close).rsi()
    rsi_k = ta.momentum.StochRSIIndicator(kl.Close).stochrsi_k()
    rsi_d = ta.momentum.StochRSIIndicator(kl.Close).stochrsi_d()
    ema = ta.trend.ema_indicator(kl.Close, window=200)
    if rsi.iloc[-1] < 40 and ema.iloc[-1] < kl.Close.iloc[-1] and rsi_k.iloc[-1] < 20 and rsi_k.iloc[-3] < rsi_d.iloc[-3] and rsi_k.iloc[-2] < rsi_d.iloc[-2] and rsi_k.iloc[-1] > rsi_d.iloc[-1]:
        return 'up'
    if rsi.iloc[-1] > 60 and ema.iloc[-1] > kl.Close.iloc[-1] and rsi_k.iloc[-1] > 80 and rsi_k.iloc[-3] > rsi_d.iloc[-3] and rsi_k.iloc[-2] > rsi_d.iloc[-2] and rsi_k.iloc[-1] < rsi_d.iloc[-1]:
        return 'down'

    else:
        return 'none'


def rsi_signal(symbol):
    kl = klines(symbol)
    rsi = ta.momentum.RSIIndicator(kl.Close).rsi()
    ema = ta.trend.ema_indicator(kl.Close, window=200)
    if rsi.iloc[-2] < 30 and rsi.iloc[-1] > 30:
        return 'up'
    if rsi.iloc[-2] > 70 and rsi.iloc[-1] < 70:
        return 'down'

    else:
        return 'none'


def macd_signal(symbol):
    kl = klines(symbol)
    macd = ta.trend.macd_diff(kl.Close)
    macd_signal = ta.trend.macd_signal(kl.Close)
    if macd.iloc[-1] > macd_signal.iloc[-1] and macd.iloc[-2] < macd_signal.iloc[-2]:
        return 'up'
    elif macd.iloc[-1] < macd_signal.iloc[-1] and macd.iloc[-2] > macd_signal.iloc[-2]:
        return 'down'
    else:
        return 'none'


def ema200_50(symbol):
    kl = klines(symbol)
    ema200 = ta.trend.ema_indicator(kl.Close, window=100)
    ema50 = ta.trend.ema_indicator(kl.Close, window=50)
    if ema50.iloc[-3] < ema200.iloc[-3] and ema50.iloc[-2] < ema200.iloc[-2] and ema50.iloc[-1] > ema200.iloc[-1]:
        return 'up'
    if ema50.iloc[-3] > ema200.iloc[-3] and ema50.iloc[-2] > ema200.iloc[-2] and ema50.iloc[-1] < ema200.iloc[-1]:
        return 'down'
    else:
        return 'none'


orders = 0
symbol = ''
# getting all symbols from Binace Futures list:
symbols = get_tickers_usdt()
# Other functions remain the same...

# Main loop
while True:
    balance = get_balance_usdt()
    sleep(1)
    if balance == None:
        print('Error: Unable to connect to the API.')
    if balance != None:
        print("Balance: ", balance, " USDT")
        pos = get_pos()
        print(f'Open positions: {pos}')
        ord = check_orders()
        for elem in ord:
            if elem not in pos:
                close_open_orders(elem)

        if len(pos) < qty:
            for elem in get_tickers_usdt():
                tp, sl = calculate_tp_sl(elem)
                signal = macd_signal(elem)

                if signal == 'up' and elem != 'USDCUSDT' and elem not in pos and elem not in ord:
                    print('Found BUY signal for ', elem)
                    set_mode(elem, type)
                    sleep(1)
                    set_leverage(elem, leverage)
                    sleep(1)
                    print('Placing order for ', elem)
                    open_order(elem, 'buy', tp, sl)
                    pos = get_pos()
                    sleep(1)
                    ord = check_orders()
                    sleep(1)
                    sleep(10)

                if signal == 'down' and elem != 'USDCUSDT' and elem not in pos and elem not in ord:
                    print('Found SELL signal for ', elem)
                    set_mode(elem, type)
                    sleep(1)
                    set_leverage(elem, leverage)
                    sleep(1)
                    print('Placing order for ', elem)
                    open_order(elem, 'sell', tp, sl)
                    pos = get_pos()
                    sleep(1)
                    ord = check_orders()
                    sleep(1)
                    sleep(10)
    print('Waiting 3 min')
    sleep(180)
