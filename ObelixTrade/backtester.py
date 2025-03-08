import pandas as pd

class Backtester:
    def __init__(self, initial_balance: float = 10000, fee_rate: float = 0.001):
        self.initial_balance = initial_balance
        self.fee_rate = fee_rate

    def run(self, df_with_signals: pd.DataFrame) -> float:
        """
        A naive backtest that uses buy/sell signals to go all-in/out.
        """
        balance = self.initial_balance
        btc_held = 0.0
        last_signal = None

        equity_curve = []

        for i in range(len(df_with_signals)):
            row = df_with_signals.iloc[i]
            signal = row['signal']
            price = row['close']

            # Current total equity
            current_equity = balance + btc_held * price
            equity_curve.append(current_equity)

            # Execute signals
            if signal == 'buy' and last_signal != 'buy':
                # Buy with all balance
                if balance > 0:
                    # Subtract fee from balance
                    balance_after_fee = balance * (1 - self.fee_rate)
                    btc_held = balance_after_fee / price
                    balance = 0
                    last_signal = 'buy'
            elif signal == 'sell' and last_signal != 'sell':
                # Sell all BTC
                if btc_held > 0:
                    # Subtract fee after the sell
                    balance = (btc_held * price) * (1 - self.fee_rate)
                    btc_held = 0
                    last_signal = 'sell'

        final_equity = balance + btc_held * df_with_signals['close'].iloc[-1]
        df_with_signals['equity_curve'] = equity_curve
        return final_equity