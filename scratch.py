from keys import Key, Secret
from binance.um_futures import UMFutures
import pandas as pd
from binance.error import ClientError

client = UMFutures(key=Key, secret=Secret)

import datetime

def get_tickers_usdt():
    coins = []
    resp = client.ticker_price()
    for elem in resp:
        if 'USDT' in elem['symbol']:
            coins.append(elem['symbol'])
    return coins

def klines(symbol):
    try:
        resp = pd.DataFrame(client.klines(symbol, '5m'))
        resp = resp.iloc[:,:6]
        resp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        resp['Time'] = pd.to_datetime(resp['Time'], unit='ms')
        
        # Get today's date
        today = datetime.datetime.now().date()
        
        # Filter rows where the date in the 'Time' column matches today's date
        resp = resp[resp['Time'].dt.date == today]

        first_volume = float(resp['Volume'].iloc[0])
        last_volume = float(resp['Volume'].iloc[-1])
        
        if first_volume != 0:
            percentage_change = ((last_volume - first_volume) / first_volume) * 100
        else:
            percentage_change = 0
        
        return percentage_change
        
    except ClientError as error:
        print(
            "Error:", error
        )

# Calculate the percentage change for each symbol and store in a dictionary
percentage_changes = {}
symbols = get_tickers_usdt()
for symbol in symbols:
    percentage_changes[symbol] = klines(symbol)

# Sort the dictionary by values (percentage changes) in descending order
sorted_changes = sorted(percentage_changes.items(), key=lambda x: x[1], reverse=True)

# Get the top symbol with the largest percentage change
top_symbol = sorted_changes[0][0]
top_change = sorted_changes[0][1]

print("Top coin with the largest change in volume:", top_symbol)
print("Percentage change in volume:", top_change)