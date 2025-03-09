import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from ..indicators import SMA
from .BaseStrategy import BaseStrategy

class KNNStrategy(BaseStrategy):
    """
    KNNStrategy uses a K-Nearest Neighbors classifier to predict whether the price will move up or down.
    
    It computes technical indicators (SMA_short and SMA_long) as features and then defines the target
    variable (label) as:
    
    - 'buy' (encoded as 1) if the next period's return is positive.
    - 'sell' (encoded as 0) if the next period's return is non-positive.
    
    The classifier is trained on these features, and then it predicts signals for the data.
    """

    def __init__(self, short_window=20, long_window=50, n_neighbors=5):
        self.short_sma = SMA(short_window)
        self.long_sma = SMA(long_window)
        self.n_neighbors = n_neighbors
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
        Creates a label based on the next period's return:
          - Label as 1 ("buy") if the return is positive.
          - Label as 0 ("sell") if the return is negative or zero.
        """
        df = df.copy()
        df['future_return'] = df['close'].shift(-1) - df['close']
        df['label'] = np.where(df['future_return'] > 0, 1, 0)
        df.dropna(inplace=True)
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates signals using the KNN classifier:
          1. Computes features and labels.
          2. Trains the classifier on the features.
          3. Predicts the signal and converts it to 'buy' or 'sell'.
          
        Note: This example uses the entire dataset for training and prediction.
        In a real scenario, you might want to use a walk-forward method or separate training and testing sets.
        """
        # Compute features and labels
        df_features = self.generate_features(df)
        df_labeled = self.generate_labels(df_features)
        
        feature_cols = ['SMA_diff', 'momentum']
        X = df_labeled[feature_cols]
        y = df_labeled['label']

        # Train the KNN classifier
        self.model.fit(X, y)
        # Predict signals on the same data
        df_labeled['prediction'] = self.model.predict(X)
        # Convert numerical predictions to signals
        df_labeled['signal'] = df_labeled['prediction'].apply(lambda x: 'buy' if x == 1 else 'sell')
        
        # Optionally, drop auxiliary columns before returning
        df_labeled.drop(columns=['future_return', 'label', 'prediction'], inplace=True)
        return df_labeled
