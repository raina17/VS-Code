from binance.spot import Spot
from Binance_Spot_Coins_List import coin_list
from keys import Key, Secret
from binance.error import ClientError
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import ta

# Global variable for time duration
time_duration = '30m'

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
    if price_change > 1 and price_change < 30:
        print(f"{symbol} : {round(volume_change, 2)} : {round(price_change, 2)}")
        top_coin_volume_list.append(symbol)

def get_rsi_signal(symbol, interval=time_duration, period=14, rsi_threshold=70):
    """
    Get RSI signal for a symbol.

    Args:
        symbol (str): Symbol to get RSI signal for.
        interval (str): Time interval for data (default is '15m').
        period (int): RSI period (default is 14).
        rsi_threshold (int): RSI threshold for buy/sell signal (default is 70).

    Returns:
        str: RSI signal ('BUY', 'SELL', or 'HOLD').
    """
    klines = client.klines(symbol, interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    
    # Calculate RSI
    rsi = ta.momentum.RSIIndicator(close=df['close'], window=period)
    rsi_value = rsi.rsi().iloc[-1]

    # Generate signals
    if rsi_value > rsi_threshold:
        return 'SELL'
    elif rsi_value < (100 - rsi_threshold):
        return 'BUY'
    else:
        return 'HOLD'

def get_macd_signal(symbol, interval=time_duration):
    """
    Get MACD signal for a symbol.

    Args:
        symbol (str): Symbol to get MACD signal for.
        interval (str): Time interval for data (default is '15m').

    Returns:
        str: MACD signal ('BUY' or 'SELL').
    """
    klines = client.klines(symbol, interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    
    # Calculate MACD
    macd = ta.trend.macd_diff(close=df['close'])
    macd_signal = 'BUY' if macd.iloc[-1] > 0 else 'SELL'
    return macd_signal

def get_stochastic_signal(symbol, interval=time_duration, k_period=14, d_period=3):
    """
    Get Stochastic Oscillator signal for a symbol.

    Args:
        symbol (str): Symbol to get Stochastic Oscillator signal for.
        interval (str): Time interval for data (default is '15m').
        k_period (int): Period for %K calculation (default is 14).
        d_period (int): Period for %D calculation (default is 3).

    Returns:
        str: Stochastic Oscillator signal ('BUY', 'SELL', or 'HOLD').
    """
    klines = client.klines(symbol, interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])

    # Calculate Stochastic Oscillator
    stoch = ta.momentum.StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=k_period, smooth_window=d_period)
    k_value = stoch.stoch().iloc[-1]
    d_value = stoch.stoch_signal().iloc[-1]

    # Generate signals
    if k_value > d_value:
        return 'BUY'
    elif k_value < d_value:
        return 'SELL'
    else:
        return 'HOLD'

def get_bollinger_band_signal(symbol, interval=time_duration, window=20, std_dev=2):
    """
    Get Bollinger Bands signal for a symbol.

    Args:
        symbol (str): Symbol to get Bollinger Bands signal for.
        interval (str): Time interval for data (default is '15m').
        window (int): Moving average window size (default is 20).
        std_dev (int): Standard deviation for bands calculation (default is 2).

    Returns:
        str: Bollinger Bands signal ('BUY', 'SELL', or 'HOLD').
    """
    klines = client.klines(symbol, interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])

    # Calculate Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['close'], window=window, window_dev=std_dev)
    bb_high = bb.bollinger_hband().iloc[-1]
    bb_low = bb.bollinger_lband().iloc[-1]
    close_price = df['close'].iloc[-1]

    # Generate signals
    if close_price > bb_high:
        return 'SELL'
    elif close_price < bb_low:
        return 'BUY'
    else:
        return 'HOLD'



# Dictionary to store coin signals
coin_signals = {}
for symbol in top_coin_volume_list:
    rsi_signal = get_rsi_signal(symbol)
    macd_signal = get_macd_signal(symbol)
    stochastic_signal = get_stochastic_signal(symbol)
    bollinger_band_signal = get_bollinger_band_signal(symbol)
    coin_signals[symbol] = {'RSI': rsi_signal, 'MACD': macd_signal, 'Stochastic': stochastic_signal, 'Bollinger': bollinger_band_signal}

# Print coin signals
print(coin_signals)
