from binance.spot import Spot
from Binance_Spot_Coins_List import coin_list
from keys import Key, Secret
from binance.error import ClientError
import pandas as pd
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import ta

# Global variable for time duration
time_duration = '15m'

# Initialize Binance client
client = Spot(api_key=Key, api_secret=Secret)

#to get the current holding I have
for symbol in client.user_asset():
    if symbol['locked'] != '0':
        print(f'the asset that I currently have is {symbol["asset"]}')
        asset = symbol["asset"] + 'USDT'

#number of open orders
open_orders = client.get_open_orders(asset)
print(f'{asset} has {len(open_orders)} open orders')

#to cancel open orders

# cancel_order = client.cancel_open_orders(asset)
# print('Open orders cancelled')

#to convert teh coin to new coin
import requests
print(client.balance())
# Binance API endpoint for converting assets
convert_endpoint = "https://api.binance.com/sapi/v1/asset/transfer"


# Asset to convert from
from_asset = "DEXE"

# Asset to convert to
to_asset = "USDT"

# Quantity to convert
quantity = 0.001  # For example, convert 0.001 BTC to ETH

# Construct payload
payload = {
    "asset": from_asset,
    "target_asset": to_asset,
    "amount": quantity,
    "type": 1  # Type 1 for spot wallet
}

# Send POST request with signed API key and secret
response = requests.post(
    convert_endpoint,
    headers={"X-MBX-APIKEY": Key},
    params=payload
)

# Print response
print(response.json())
