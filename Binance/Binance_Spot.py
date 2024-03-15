from binance.spot import Spot
from Binance_Spot_Coins_List import coin_list
from keys import Key, Secret
from binance.error import ClientError
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import ta

# Global variable for time duration
time_duration = '5m'

# Initialize Binance client
client = Spot(api_key=Key, api_secret=Secret)

def get_klines_data(symbol, column='Close'):
    """
    Get historical price data for a symbol and calculate percentage change.

    Args:
        symbol (str): Symbol to retrieve data for.
        column (str): Column to calculate percentage change for (default is 'Close').

    Returns:
        float: Percentage change in the specified column.
    """
    try:
        klines = client.klines(symbol, time_duration)
        if len(klines) >= 401:  # Ensure enough data points for calculations
            df = pd.DataFrame(klines).iloc[400:,:6]  # Extract relevant data
            df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['Time'] = pd.to_datetime(df['Time'], unit='ms')

            first_value = float(df[column].iloc[0])
            last_value = float(df[column].iloc[-1])

            if first_value != 0:
                percentage_change = ((last_value - first_value) / first_value) * 100
                return max(0, percentage_change)  # Ensure non-negative percentage change
            else:
                return 0
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
    results = list(executor.map(process_symbol, coin_list))  # Convert map object to list for reuse

# Collect and sort results
sorted_changes_volume = sorted(results, key=lambda x: x[1], reverse=True)
sorted_changes_price = sorted(results, key=lambda x: x[2], reverse=True)

# Print top 5 results
top_coin_volume = [symbol for symbol, _, price_change in sorted_changes_volume[:10] if 1 < price_change < 30]
for symbol, volume_change, price_change in sorted_changes_volume[:10]:
    if symbol in top_coin_volume:
        print(f"{symbol} : {round(volume_change, 2)} : {round(price_change, 2)}")

def get_signal(symbol, signal_function, **kwargs):
    """
    Get trading signal for a symbol using a specific indicator.

    Args:
        symbol (str): Symbol to get signal for.
        signal_function (function): Function to calculate signal.
        **kwargs: Additional arguments for the signal function.

    Returns:
        str: Trading signal ('BUY', 'SELL', or 'HOLD').
    """
    try:
        klines = client.klines(symbol, time_duration)
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        return signal_function(df, **kwargs)
    except ClientError as error:
        print(f"Error processing {symbol}: {error}")
        return 'HOLD'

def get_rsi_signal(df, period=14, rsi_threshold=70):
    """
    Get RSI signal for a symbol.

    Args:
        df (DataFrame): DataFrame containing price data.
        period (int): RSI period (default is 14).
        rsi_threshold (int): RSI threshold for buy/sell signal (default is 70).

    Returns:
        str: RSI signal ('BUY', 'SELL', or 'HOLD').
    """
    rsi = ta.momentum.RSIIndicator(close=df['close'], window=period)
    rsi_value = rsi.rsi().iloc[-1]
    if rsi_value > rsi_threshold:
        return 'SELL'
    elif rsi_value < (100 - rsi_threshold):
        return 'BUY'
    else:
        return 'HOLD'

def get_macd_signal(df):
    """
    Get MACD signal for a symbol.

    Args:
        df (DataFrame): DataFrame containing price data.

    Returns:
        str: MACD signal ('BUY' or 'SELL').
    """
    macd = ta.trend.macd_diff(close=df['close'])
    return 'BUY' if macd.iloc[-1] > 0 else 'SELL'

def get_stochastic_signal(df, k_period=14, d_period=3):
    """
    Get Stochastic Oscillator signal for a symbol.

    Args:
        df (DataFrame): DataFrame containing price data.
        k_period (int): Period for %K calculation (default is 14).
        d_period (int): Period for %D calculation (default is 3).

    Returns:
        str: Stochastic Oscillator signal ('BUY', 'SELL', or 'HOLD').
    """
    stoch = ta.momentum.StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=k_period, smooth_window=d_period)
    k_value = stoch.stoch().iloc[-1]
    d_value = stoch.stoch_signal().iloc[-1]
    if k_value > d_value:
        return 'BUY'
    elif k_value < d_value:
        return 'SELL'
    else:
        return 'HOLD'

def get_bollinger_band_signal(df, window=20, std_dev=2):
    """
    Get Bollinger Bands signal for a symbol.

    Args:
        df (DataFrame): DataFrame containing price data.
        window (int): Moving average window size (default is 20).
        std_dev (int): Standard deviation for bands calculation (default is 2).

    Returns:
        str: Bollinger Bands signal ('BUY', 'SELL', or 'HOLD').
    """
    bb = ta.volatility.BollingerBands(close=df['close'], window=window, window_dev=std_dev)
    bb_high = bb.bollinger_hband().iloc[-1]
    bb_low = bb.bollinger_lband().iloc[-1]
    close_price = df['close'].iloc[-1]
    if close_price > bb_high:
        return 'SELL'
    elif close_price < bb_low:
        return 'BUY'
    else:
        return 'HOLD'

# Dictionary to store coin signals
coin_signals = {}
for symbol in top_coin_volume:
    coin_signals[symbol] = {
        'RSI': get_signal(symbol, get_rsi_signal),
        'MACD': get_signal(symbol, get_macd_signal),
        'Stochastic': get_signal(symbol, get_stochastic_signal),
        'Bollinger': get_signal(symbol, get_bollinger_band_signal)
    }

# Print coin signals
print(coin_signals)
