import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch 1 year of historical data for Apple
df = yf.download("AAPL", period="60d", interval="1d")

# Print the first few rows
print(df.head())

# Calculate 20-day (short) and 50-day (long) moving averages
df['MA_short'] = df['Close'].rolling(window=20).mean()
df['MA_long']  = df['Close'].rolling(window=50).mean()

df['Signal'] = 0
df.loc[df['MA_short'] > df['MA_long'], 'Signal'] = 1
df.loc[df['MA_short'] < df['MA_long'], 'Signal'] = -1

# Calculate daily returns
df['Daily_Return'] = df['Close'].pct_change()

# Shift the signal by 1 day to simulate entering on the next open (simplification)
df['Shifted_Signal'] = df['Signal'].shift(1)

# Strategy return = today's daily return * yesterday's position
df['Strategy_Return'] = df['Daily_Return'] * df['Shifted_Signal']

df['Cumulative_Buy_and_Hold'] = (1 + df['Daily_Return']).cumprod()  # if you just held AAPL
df['Cumulative_Strategy']     = (1 + df['Strategy_Return']).cumprod()


plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Cumulative_Buy_and_Hold'], label='Buy & Hold', color='blue')
plt.plot(df.index, df['Cumulative_Strategy'], label='Strategy', color='red')
plt.title("Moving Average Crossover Strategy vs. Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.savefig('strategy_vs_buy_and_hold.png')

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Close Price', alpha=0.5)
plt.plot(df.index, df['MA_short'], label='20-day MA', color='green')
plt.plot(df.index, df['MA_long'], label='50-day MA', color='orange')
plt.title("AAPL Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.savefig('price_with_moving_averages.png')


buy_and_hold_return = df['Cumulative_Buy_and_Hold'].iloc[-1] - 1
strategy_return = df['Cumulative_Strategy'].iloc[-1] - 1

print(f"Buy & Hold Return: {buy_and_hold_return:.2%}")
print(f"Strategy Return: {strategy_return:.2%}")
