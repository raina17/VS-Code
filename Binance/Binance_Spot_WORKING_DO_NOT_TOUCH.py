from binance.spot import Spot
from Binance_Spot_Coins_List import coin_list
from keys import Key, Secret
from binance.error import ClientError
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import ta

# Global variable for time duration
time_duration = '15m'

# Initialize Binance client
client = Spot(api_key=Key, api_secret=Secret)

def get_klines_data(symbol, column='Close'):
    """
    Get historical price data for a symbol.

    Args:
        symbol (str): Symbol to retrieve data for.
        column (str): Column to calculate percentage change for (default is 'Close').

    Returns:
        float: Percentage change in the specified column.
    """
    try:
        klines = client.klines(symbol, time_duration)
        if len(klines) >= 401:  # Ensure enough data points for calculations
            df = pd.DataFrame(klines)
            df = df.iloc[400:,:6]
            df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['Time'] = pd.to_datetime(df['Time'], unit='ms')

            first_value = float(df[column].iloc[0])
            last_value = float(df[column].iloc[-1])
            #print(f'last volume of the coin is {last_value}')

            if first_value != 0:
                percentage_change = ((last_value - first_value) / first_value) * 100
                if percentage_change > 1:
                    return percentage_change
                    
                else:
                    return 0
            else:
                percentage_change = 0
            return percentage_change
            
        else:
            return 0  # Return 0 if insufficient data
    except ClientError as error:
        print("Error:", error)
        return 0

def process_symbol(symbol):
    """
    Process a symbol to calculate volume and price changes.

    Args:
        symbol (str): Symbol to process.

    Returns:
        tuple: Symbol, volume change, and price change.
    """
    volume_change = get_klines_data(symbol, column='Volume')
    price_change = get_klines_data(symbol, column='Close')
    return symbol, volume_change, price_change

# Concurrent processing for symbol data
with ThreadPoolExecutor() as executor:
    results = executor.map(process_symbol, coin_list)

# Collect and sort results
sorted_changes_volume = sorted(results, key=lambda x: x[1], reverse=True)
sorted_changes_price = sorted(results, key=lambda x: x[2], reverse=True)

# Print top 5 results
top_coin_volume = sorted_changes_volume[:10]
top_coin_volume_list = []
for symbol, volume_change, price_change in top_coin_volume:
    if price_change > 1 and price_change < 50:
        print(f"{symbol} : {round(volume_change, 2)} : {round(price_change, 2)}")
        top_coin_volume_list.append(symbol)