# ObelixTrade

ObelixTrade is a Python crypto trading bot created for backtesting, plotting, live trading and hopefully making me some money to buy beer. I coded it with a object-oriented structure to help me test strategies and eventually trade on exchanges like Binance.

If you are wondering why the name "Obelix Trade", Obelix is the name of my huge orange cat, and he is adorable.

## Features

- **Data Fetching:** Retrieve historical OHLCV data using `ccxt`.
- **Indicators:** Compute technical indicators such as Simple Moving Averages (SMAs).
- **Strategy Backtesting:** Run backtests on strategies.
- **Plotting:** Visualize price data and buy/sell signals.
- **Live Trading:** (Planned) Show me the MOOONEY!


## Requirements

- Python 3.7+\
- [ccxt](https://github.com/ccxt/ccxt)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)
- [ta](https://github.com/bukosabino/ta)

Install the dependencies via:

```bash
pip install -r requirements.txt
```
Usage Example
-------------

Here's a quick example to get started, I prefer using a Jupyter notebook or something for the plots:

```python
from ObelixTrade import DataFetcher, SMACrossoverStrategy, Backtester, Plotter

# 1. Fetch data
fetcher = DataFetcher()
df = fetcher.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=300)

# 2. Apply SMA Crossover Strategy
strategy = SMACrossoverStrategy(short_window=20, long_window=50)
df_signals = strategy.generate_signals(df)

# 3. Backtest the strategy\
backtester = Backtester(initial_balance=10000, fee_rate=0.001)
final_value = backtester.run(df_signals)
print("Final Portfolio Value:", final_value)

# 4. Plot the signals
plotter = Plotter()
plotter.plot_signals(df_signals)
```

## License

This project is for personal use. Feel free to modify it as needed.