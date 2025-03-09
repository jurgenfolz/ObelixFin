import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Plotter:
    
    def plot_signals(self, df):
        """
        Plots close price, trading signals, and optional indicators interactively using Plotly.
        """
        fig = go.Figure()

        # Add close price trace
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['close'],
            mode='lines',
            name='Close'
        ))

        # Optional indicators
        if 'SMA_short' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['SMA_short'],
                mode='lines',
                name='SMA Short'
            ))
        if 'SMA_long' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['SMA_long'],
                mode='lines',
                name='SMA Long'
            ))

        # Add buy signals
        buy_signals = df[df['signal'] == 'buy']
        fig.add_trace(go.Scatter(
            x=buy_signals['timestamp'],
            y=buy_signals['close'],
            mode='markers',
            name='Buy Signal',
            marker=dict(symbol='triangle-up', size=10, color='green')
        ))

        # Add sell signals
        sell_signals = df[df['signal'] == 'sell']
        fig.add_trace(go.Scatter(
            x=sell_signals['timestamp'],
            y=sell_signals['close'],
            mode='markers',
            name='Sell Signal',
            marker=dict(symbol='triangle-down', size=10, color='red')
        ))

        # Update layout for interactivity and user-friendliness
        fig.update_layout(
            title="Price & Trading Signals",
            xaxis_title="Timestamp",
            yaxis_title="Price",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        fig.show()
    
    def plot_signals_matplot_lib(self, df):
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


    
