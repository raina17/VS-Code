from keys import Key, Secret
from binance.um_futures import UMFutures
import pandas as pd
from binance.error import ClientError
import datetime
from concurrent.futures import ThreadPoolExecutor
from time import sleep

client = UMFutures(key=Key, secret=Secret)

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
    resp = client.ticker_price()
    coins = [elem['symbol'] for elem in resp if 'USDT' in elem['symbol']]
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

def process_symbol(symbol):
    volume_change = get_klines_data(symbol, column='Volume')
    price_change = get_klines_data(symbol, column='Close')
    return symbol, volume_change, price_change

balance = get_balance_usdt()
print(f'My USDT balance is ${balance}')

symbols = get_tickers_usdt()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_symbol, symbols)

sorted_changes_volume = sorted(results, key=lambda x: x[1], reverse=True)[:5]

print("Coin : Percentage change in volume : Percentage change in price")
for symbol, volume_change, price_change in sorted_changes_volume:
    print(f"{symbol} : {round(volume_change,2)} : {round(price_change,2)}")
