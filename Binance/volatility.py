from keys import Key, Secret  # Import your Binance API key and secret from a keys.py file
from binance.um_futures import UMFutures
import ta
import pandas as pd
from time import sleep
from binance.error import ClientError

# Initialize Binance client
client = UMFutures(key=Key, secret=Secret)

# Parameters
tp_percentage = 0.5  # Dynamic take profit percentage
sl_percentage = 0.05  # Dynamic stop loss percentage
profit_threshold = 0.5  # Exit trade when profit reaches 50%
loss_threshold = -0.05  # Exit trade when loss reaches -5%
leverage = 10  # Leverage for trading
qty = 10  # Quantity for each trade

def get_tickers():
    """Get list of all available futures coins"""
    resp = client.exchange_info()
    symbols = [symbol['symbol'] for symbol in resp['symbols'] if symbol['contractType'] == 'ISOLATED']
    return symbols

def get_klines(symbol, interval='1m', limit=100):
    """Get recent candlestick data (klines) for a symbol"""
    try:
        resp = pd.DataFrame(client.klines(symbol, interval, limit))
        resp = resp.iloc[:,:6]
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        resp = resp.set_index('Time')
        resp.index = pd.to_datetime(resp.index, unit='ms')
        resp = resp.astype(float)
        return resp
    except ClientError as error:
        print("Error fetching klines:", error)

def calculate_indicators(klines):
    """Calculate technical indicators"""
    rsi = ta.momentum.RSIIndicator(klines['Close']).rsi()
    return rsi

def place_order(symbol, side, price, tp_price, sl_price):
    """Place a new order"""
    try:
        if side == 'BUY':
            resp = client.new_order(symbol=symbol, side=side, type='LIMIT', quantity=qty, price=price)
        else:
            resp = client.new_order(symbol=symbol, side=side, type='LIMIT', quantity=qty, price=price)
        
        # Place take profit and stop loss orders
        if side == 'BUY':
            client.new_order(symbol=symbol, side='SELL', type='TAKE_PROFIT_MARKET', quantity=qty, stopPrice=tp_price)
            client.new_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=qty, stopPrice=sl_price)
        else:
            client.new_order(symbol=symbol, side='BUY', type='TAKE_PROFIT_MARKET', quantity=qty, stopPrice=tp_price)
            client.new_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=qty, stopPrice=sl_price)
        
        return resp
    except ClientError as error:
        print("Error placing order:", error)


while True:
    print('wip')
    try:
        # Get list of futures coins
        symbols = get_tickers()

        for symbol in symbols:
            # Get recent klines data
            klines = get_klines(symbol)

            # Calculate technical indicators
            rsi = calculate_indicators(klines)

            # Place buy order if conditions are met
            if rsi.iloc[-1] < 30:
                current_price = float(client.ticker_price(symbol)['price'])
                tp_price = current_price * (1 + tp_percentage)
                sl_price = current_price * (1 - sl_percentage)
                place_order(symbol, 'BUY', current_price, tp_price, sl_price)
                print("Buy order placed for:", symbol)

        sleep(6)  # Check every 1 minute
    except KeyboardInterrupt:
        print("Exiting...")
        break