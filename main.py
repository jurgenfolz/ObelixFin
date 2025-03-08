from ObelixTrade import DataFetcher, SMACrossoverStrategy, Backtester, Plotter

# 1. Fetch data
fetcher = DataFetcher()
df = fetcher.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=300)

# 2. Apply strategy
strategy = SMACrossoverStrategy(short_window=20, long_window=50)
df_signals = strategy.generate_signals(df)

# 3. Backtest
backtester = Backtester(initial_balance=10000, fee_rate=0.001)
final_value = backtester.run(df_signals)
print("Final Portfolio Value:", final_value)

# 4. Plot
plotter = Plotter()
plotter.plot_signals(df_signals)
