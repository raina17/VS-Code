from keys import Key, Secret
from binance.um_futures import UMFutures
import pandas as pd
from binance.error import ClientError
import datetime
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

#this function returns the list of al the coins available in USDT futures
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

print(f'My USDT balance is ${balance}')
print("Coin : Percentage change in volume : Percentage change in price")
for symbol, volume_change in top_5_volume:
    price_change = percentage_changes_price[symbol]
    print(f"{symbol} : {round(volume_change,2)} : {round(price_change,2)}")


