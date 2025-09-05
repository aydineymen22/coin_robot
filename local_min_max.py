import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path
import numpy as np
from scipy.signal import argrelextrema
from indicators import add_savgol, add_atr


df = pd.read_csv('btc_data.csv', parse_dates=['timestamp'])


df = add_savgol(df, window=21, poly=3)
df = add_atr(df, period=14)


order = 5  
local_max_idx = argrelextrema(df['SG_Filter'].values, np.greater, order=order)[0]
local_min_idx = argrelextrema(df['SG_Filter'].values, np.less, order=order)[0]

buy_signals = []
sell_signals = []

for i in local_min_idx:

    if df.loc[i, 'close'] > 0 and (df.loc[i, 'high'] - df.loc[i, 'low']) > 0.5 * df.loc[i, 'ATR']:
        buy_signals.append((df.loc[i, 'timestamp'], df.loc[i, 'close']))

for i in local_max_idx:
    if df.loc[i, 'close'] > 0 and (df.loc[i, 'high'] - df.loc[i, 'low']) > 0.5 * df.loc[i, 'ATR']:
        sell_signals.append((df.loc[i, 'timestamp'], df.loc[i, 'close']))




fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df["timestamp"], df["close"], label="Close Price", alpha=0.6)
ax.plot(df["timestamp"], df["SG_Filter"], label="Savitzky–Golay Smoothed", linewidth=2)

if buy_signals:
    ax.scatter([t for t, _ in buy_signals], [p for _, p in buy_signals],
               color="green", marker="^", s=100, label="BUY")
if sell_signals:
    ax.scatter([t for t, _ in sell_signals], [p for _, p in sell_signals],
               color="red", marker="v", s=100, label="SELL")

ax.set_title("BTC/USDT with Local Min/Max Buy & Sell Signals (Filtered)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()

plt.tight_layout()


img_path = Path(__file__).resolve().parent.parent / "images" / "btc_local_min_max_clean.png"
plt.savefig(img_path)
plt.show()


# Save enriched dataset with signals
df["buy_signal"] = df["timestamp"].isin([t for t, _ in buy_signals])
df["sell_signal"] = df["timestamp"].isin([t for t, _ in sell_signals])

# Save to new file
df.to_csv("btc_signals.csv", index=False)
print("Saved signals to btc_signals.csv")