import pandas as pd

class BaseStrategy:
    """Abstract base class for all trading strategies."""
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Must return a DataFrame with a 'signal' column (e.g. 'buy', 'sell', or None).
        """
        raise NotImplementedError("This method must be overridden by subclasses.")