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
#current_assets = [symbol['asset'] for symbol in client.user_asset() if symbol['free'] != '0' or symbol['locked'] != '0']
#print(f'My current holdings are {current_assets}')
# current_holdings = {}
# for symbol in client.user_asset():
#     if (symbol['free']) > (symbol['locked']):
#         current_holdings[symbol['asset']] = (symbol['free'])
#     else:
#         current_holdings[symbol['asset']] = (symbol['locked'])
# print(current_holdings)

# for symbol in current_holdings:
#     print(symbol)
#     print(float(client.ticker_price(symbol + "USDT")["price"])*.95)

#a = client.new_order(symbol=, side=, )
print(client.depth('API3USDT'))