from binance.spot import Spot
from Binance_Spot_Coins_List import coin_list
from keys import Key, Secret
from binance.error import ClientError
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import ta
# Initialize Binance client
client = Spot(api_key=Key, api_secret=Secret)
balance = client.balance()[0]['balance']
print(f'My BTC balance is {balance}')

#to get the current holding I have
current_assets = [symbol['asset'] for symbol in client.user_asset() if symbol['free'] != '0' or symbol['locked'] != '0']
print(f'My current holdings are {current_assets}')

# Global variable for time duration
time_duration = '5m'


response0 = client.get_open_orders("REQUSDT")
print(response0)
response1 = client.cancel_open_orders("REQUSDT")
print(response1)
print(response0)