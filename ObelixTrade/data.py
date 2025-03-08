#Classes/functions for fetching data 
import ccxt
import pandas as pd
import datetime

class DataFetcher:
    def __init__(self, exchange_id='binance'):
        self.exchange: ccxt.binance = getattr(ccxt, exchange_id)()
    
    def fetch_ohlcv(self, symbol='BTC/USDT', timeframe='1d', limit=200):
        """Fetches OHLCV data from the exchange using ccxt."""
        raw_data = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df