import pandas as pd
from .indicators import SMA

class BaseStrategy:
    """Abstract base class for all trading strategies."""
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Must return a DataFrame with a 'signal' column (e.g. 'buy', 'sell', or None).
        """
        raise NotImplementedError("This method must be overridden by subclasses.")

class SMACrossoverStrategy(BaseStrategy):
    """Simple Moving Average Crossover Strategy.
    The **SMACrossoverStrategy** is a type of momentum strategy that uses two simple moving averages (SMAs) to identify changes in market trends. Here's how it works in detail:

    ### 1\. **Concept of SMAs**

    -   **Simple Moving Average (SMA)**:\
        An SMA calculates the average price over a specified number of periods (e.g., 20 or 50 days). It smooths out price data to help identify trends.

    ### 2\. **The Two SMAs**

    -   **Short SMA (e.g., 20-period SMA)**:\
        This moves quickly with the price and reacts faster to recent price changes.

    -   **Long SMA (e.g., 50-period SMA)**:\
        This is slower to react, reflecting a longer-term trend.

    ### 3\. **How the Crossover Works**

    -   **Buy Signal ("Bullish Crossover")**:\
        When the **short SMA** crosses above the **long SMA**, it suggests that the recent price movement is strong enough to overcome the longer-term trend. This is interpreted as a bullish signal---indicating a potential upward move---and the strategy issues a "buy" signal.

    -   **Sell Signal ("Bearish Crossover")**:\
        Conversely, when the **short SMA** crosses below the **long SMA**, it indicates that the price is starting to weaken compared to its longer-term trend. This is a bearish signal, prompting a "sell" signal.

    ### 4\. **Implementation in Code**

    In the **SMACrossoverStrategy** class, the following steps take place:

    1.  **Indicator Calculation**:

        -   The strategy calculates the short-term SMA (`SMA_short`) and long-term SMA (`SMA_long`) for each row of your historical data.
    2.  **Signal Generation**:

        -   The code then compares these two values for every time step:
            -   If `SMA_short` > `SMA_long` and the previous signal wasn't "buy", it sets the signal for that period to "buy".
            -   If `SMA_short` < `SMA_long` and the previous signal wasn't "sell", it sets the signal to "sell".
        -   This approach prevents repeatedly issuing the same signal if the condition is maintained.
    3.  **Avoiding Duplicate Signals**:

        -   The variable `previous_signal` ensures that the strategy only issues a new signal when the crossover actually changes direction, reducing noise in the trading signals.

    ### 5\. **Why Use a Crossover Strategy?**

    -   **Simplicity**:\
        It's easy to implement and understand, especially for someone with a strong background in math and programming.

    -   **Trend Following**:\
        The strategy is designed to ride trends by entering a trade only when a new trend (upward or downward) is detected.

    -   **Foundation for More Complex Models**:\
        While basic, the SMA crossover can be the starting point. Once you're comfortable with it, you can enhance the strategy with other indicators, risk management rules, or even combine it with machine learning models.

    ### 6\. **Limitations**

    -   **Lagging Indicator**:\
        SMAs are based on historical prices, so signals are delayed. This means you might get in or out of a trade later than optimal.

    -   **Whipsaw Effect**:\
        In choppy or sideways markets, frequent crossovers might occur, leading to false signals and potentially higher trading costs."""
        
    def __init__(self, short_window=20, long_window=50):
        self.short_sma = SMA(short_window)
        self.long_sma = SMA(long_window)

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()   # Make an explicit copy if needed
        df['SMA_short'] = self.short_sma.calculate(df)
        df['SMA_long'] = self.long_sma.calculate(df)

        # Drop rows with NaN
        df.dropna(inplace=True)
        df['signal'] = None

        previous_signal = None
        for i in range(len(df)):
            
            if df['SMA_short'].iloc[i] > df['SMA_long'].iloc[i]:
                if previous_signal != 'buy':
                    # Use .loc with the row index
                    df.loc[df.index[i], 'signal'] = 'buy'
                    previous_signal = 'buy'
            else:
                if previous_signal != 'sell':
                    df.loc[df.index[i], 'signal'] = 'sell'
                    previous_signal = 'sell'

        return df
