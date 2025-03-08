#Classes for technical indicators or wrappers for ta
import pandas as pd

class SMA:
    """Simple Moving Average indicator."""
    def __init__(self, window: int = 20):
        self.window = window
    
    def calculate(self, df: pd.DataFrame, price_col: str = 'close') -> pd.Series:
        """Returns a Series representing the SMA."""
        return df[price_col].rolling(window=self.window).mean()