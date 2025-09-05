import vectorbt as vbt
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('btc_signals.csv', parse_dates=['timestamp'])

entries = df['buy_signal'].values
exits = df['sell_signal'].values

price = df['close'].values

pf = vbt.Portfolio.from_signals(
    close=df["close"],
    entries=entries,
    exits=exits,
    fees=0.001,      # 0.1% fees
    slippage=0.001,  # 0.1% slippage
    freq="1h"
)

print(pf.stats())
print("Sharpe Ratio:", pf.sharpe_ratio())
print("Max Drawdown:", pf.max_drawdown())
stats = pf.stats()
# stats.to_csv("backtest_stats.csv")




