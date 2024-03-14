from testkeys import Key, Secret, Base_url  
from binance.um_futures import UMFutures
import pandas as pd
from binance.error import ClientError
import datetime
from time import sleep
client = UMFutures(key= Key, secret= Secret, base_url = Base_url )

def get_balance_usdt():
    try:
        response = client.balance(recvWindow=6000)
        for elem in response:
                if elem['asset'] == 'USDT':
                    return float((elem['balance']))
    except ClientError as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )   
def get_tickers_usdt():
    coins = []
    resp = client.ticker_price()
    for elem in resp:
        if 'USDT' in elem['symbol']:
            coins.append(elem['symbol'])
    return coins

def get_klines_data(symbol, column='Close'):
    try:
        resp = pd.DataFrame(client.klines(symbol, '15m'))
        resp = resp.iloc[:,:6]
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        resp['Time'] = pd.to_datetime(resp['Time'], unit='ms')
        
        today = datetime.datetime.now().date()
        resp = resp[resp['Time'].dt.date == today]

        first_value = float(resp[column].iloc[0])
        last_value = float(resp[column].iloc[-1])
        
        if first_value != 0:
            percentage_change = ((last_value - first_value) / first_value) * 100
        else:
            percentage_change = 0
        
        return percentage_change
        
    except ClientError as error:
        print("Error:", error)

percentage_changes_volume = {}
percentage_changes_price = {}
symbols = get_tickers_usdt()

for symbol in symbols:
    percentage_changes_volume[symbol] = get_klines_data(symbol, column='Volume')
    percentage_changes_price[symbol] = get_klines_data(symbol, column='Close')

sorted_changes_volume = sorted(percentage_changes_volume.items(), key=lambda x: x[1], reverse=True)
sorted_changes_price = sorted(percentage_changes_price.items(), key=lambda x: x[1], reverse=True)
balance = get_balance_usdt()
sleep(5)
top_5_volume = sorted_changes_volume[:5]

# print(f'My USDT balance is ${balance}')
# print("Coin : Percentage change in volume : Percentage change in price")
# for symbol, volume_change in top_5_volume:
#     price_change = percentage_changes_price[symbol]
#     print(f"{symbol} : {round(volume_change,2)} : {round(price_change,2)}")

tp = .10 #take profit percentage
sl = .02 #stop loss percentage
volume = 10 #usdt used to trade
leverage = 20
type = 'ISOLATED'
#qty = 100

print(f'My fucking balance is $ {balance}')

trading_coin = top_5_volume[0][0]
trading_price = top_5_volume[0][1]
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

def open_order(symbol):
    price = float(client.ticker_price(symbol)['price'])
    qty_precision = get_qty_precision(symbol)
    price_precision = get_price_precision(symbol)
    qty = round(volume / price, qty_precision)
    
    
    try:
        resp1 = client.new_order(symbol=symbol, side='BUY', type='LIMIT', quantity=qty, timeInForce='GTC', price=price)
        print(symbol, "placing order")
        print(resp1)
        sleep(2)
        # Calculate stop-loss and take-profit prices
        sl_price = round(price - (price * sl), price_precision)
        tp_price = round(price + (price * tp), price_precision)
        resp2 = client.new_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=qty, timeInForce='GTC', stopPrice=sl_price)
        print(resp2)
        sleep(2)
        resp3 = client.new_order(symbol=symbol, side='SELL', type='TAKE_PROFIT_MARKET', quantity=qty, timeInForce='GTC', stopPrice=tp_price)
        print(resp3)
    except ClientError as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

open_order(trading_coin)