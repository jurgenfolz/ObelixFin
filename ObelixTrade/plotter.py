import matplotlib.pyplot as plt

class Plotter:
    def plot_signals(self, df):
        """
        Plots close price, signals, and optionally indicators.
        """
        plt.figure(figsize=(10, 6))
        
        # Plot close price
        plt.plot(df['timestamp'], df['close'], label='Close')

        # Check if any indicator columns exist
        if 'SMA_short' in df.columns:
            plt.plot(df['timestamp'], df['SMA_short'], label='SMA Short')
        if 'SMA_long' in df.columns:
            plt.plot(df['timestamp'], df['SMA_long'], label='SMA Long')

        # Buy markers
        buy_signals = df[df['signal'] == 'buy']
        plt.scatter(buy_signals['timestamp'], buy_signals['close'], marker='^', label='Buy Signal')

        # Sell markers
        sell_signals = df[df['signal'] == 'sell']
        plt.scatter(sell_signals['timestamp'], sell_signals['close'], marker='v', label='Sell Signal')

        plt.title("Price & Trading Signals")
        plt.legend()
        plt.show()
