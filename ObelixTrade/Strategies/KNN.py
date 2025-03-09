import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from ..indicators import SMA
from .BaseStrategy import BaseStrategy

class KNNStrategy(BaseStrategy):
    """
    KNNStrategy uses a K-Nearest Neighbors classifier to predict whether the price will move up, down, or stay flat.
    
    It computes technical indicators (SMA_short and SMA_long) as features and defines the target variable based on the future return
    calculated after a specified number of periods (future_shift).
    
    We then post-process the predictions to ensure that consecutive "sell" signals
    (separated only by "hold") do not occur.
    """

    def __init__(self, short_window=20, long_window=50, n_neighbors=5, future_shift=1, return_threshold=100):
        self.short_sma = SMA(short_window)
        self.long_sma = SMA(long_window)
        self.n_neighbors = n_neighbors
        self.future_shift = future_shift
        self.return_threshold = return_threshold  # Threshold for decision-making
        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbors)

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes features:
          - SMA_short and SMA_long,
          - Their difference (SMA_diff), and
          - Price momentum (percentage change).
        """
        df = df.copy()
        df['SMA_short'] = self.short_sma.calculate(df)
        df['SMA_long'] = self.long_sma.calculate(df)
        df['SMA_diff'] = df['SMA_short'] - df['SMA_long']
        df['momentum'] = df['close'].pct_change()
        df.dropna(inplace=True)
        return df

    def generate_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates a label based on the future return calculated by shifting the close price by future_shift:
          - Label as 1 ("buy") if the future return is above return_threshold.
          - Label as -1 ("sell") if the future return is below -return_threshold.
          - Label as 0 ("hold") if the future return is between -return_threshold and return_threshold.
        """
        df = df.copy()
        df['future_return'] = df['close'].shift(-self.future_shift) - df['close']

        # Three-class labeling (buy=1, sell=-1, hold=0)
        df['label'] = np.where(
            df['future_return'] > self.return_threshold, 1,
            np.where(df['future_return'] < -self.return_threshold, -1, 0)
        )
        df.dropna(inplace=True)
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates signals using the KNN classifier:
          1. Computes features and labels.
          2. Trains the classifier on the features.
          3. Predicts the signal and converts numerical predictions to 'buy', 'sell', or 'hold'.
          4. Enforces the rule that you cannot have consecutive sells separated only by holds.
        """
        # 1) Compute features and labels
        df_features = self.generate_features(df)
        df_labeled = self.generate_labels(df_features)

        feature_cols = ['SMA_diff', 'momentum']
        X = df_labeled[feature_cols]
        y = df_labeled['label']

        # 2) Train the KNN classifier
        self.model.fit(X, y)

        # 3) Predict signals on the same data
        df_labeled['prediction'] = self.model.predict(X)

        # 4) Map numerical predictions to 'buy', 'sell', or 'hold'
        df_labeled['signal'] = df_labeled['prediction'].map({1: 'buy', -1: 'sell', 0: 'hold'})

        # 5) Post-process signals to avoid consecutive sells separated only by holds
        signals_cleaned = []
        last_non_hold_signal = None

        for signal in df_labeled['signal']:
            if signal == 'sell':
                # If our last non-hold was also 'sell', turn this 'sell' into a 'hold'.
                if last_non_hold_signal == 'sell':
                    signals_cleaned.append('hold')
                else:
                    signals_cleaned.append('sell')
                    last_non_hold_signal = 'sell'
            elif signal == 'buy':
                signals_cleaned.append('buy')
                last_non_hold_signal = 'buy'
            else:  # signal == 'hold'
                signals_cleaned.append('hold')
                # We do NOT update last_non_hold_signal when we see 'hold'
        
        df_labeled['signal'] = signals_cleaned

        # Optionally, drop auxiliary columns before returning
        df_labeled.drop(columns=['future_return', 'label', 'prediction'], inplace=True)
        return df_labeled
