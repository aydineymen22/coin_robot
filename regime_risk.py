import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("btc_signals.csv", parse_dates=["timestamp"])


df["ema_fast"] = df["close"].ewm(span=20).mean()
df["ema_slow"] = df["close"].ewm(span=50).mean()
df["ema_diff"] = abs(df["ema_fast"] - df["ema_slow"]) / df["close"]

df["regime_ok"] = df["ema_diff"] < 0.01

if "ATR" not in df.columns:
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

stop_losses = []
take_profits = []

for i, row in df.iterrows():
    if row["buy_signal"]:
        entry = row["close"]
        sl = entry - 1.5 * row["ATR"]
        tp = entry + 3.0 * row["ATR"]
    elif row["sell_signal"]: 
        entry = row["close"]
        sl = entry + 1.5 * row["ATR"]
        tp = entry - 3.0 * row["ATR"]
    else:
        sl, tp = np.nan, np.nan

    stop_losses.append(sl)
    take_profits.append(tp)

df["stop_loss"] = stop_losses
df["take_profit"] = take_profits

df["daily_return"] = df["close"].pct_change()
df["cum_return"] = (1 + df["daily_return"]).cumprod()
df["daily_drawdown"] = df["cum_return"] / df["cum_return"].cummax() - 1

df["dd_limit_exceeded"] = df["daily_drawdown"] < -0.05

df["final_buy"] = df["buy_signal"] & df["regime_ok"] & ~df["dd_limit_exceeded"]
df["final_sell"] = df["sell_signal"] & df["regime_ok"] & ~df["dd_limit_exceeded"]

df.to_csv("btc_signals_with_risk.csv", index=False)
print("Saved signals with regime filter & risk rules -> btc_signals_with_risk.csv")




# 7. Plot results
plt.figure(figsize=(14, 8))

# Price
plt.plot(df["timestamp"], df["close"], label="BTC Price", color="black", alpha=0.7)

# Raw signals (Week 4)
plt.scatter(df["timestamp"][df["buy_signal"]], df["close"][df["buy_signal"]], 
            marker="^", color="green", label="Raw Buy", alpha=0.5)
plt.scatter(df["timestamp"][df["sell_signal"]], df["close"][df["sell_signal"]], 
            marker="v", color="red", label="Raw Sell", alpha=0.5)

# Final signals (Week 5)
plt.scatter(df["timestamp"][df["final_buy"]], df["close"][df["final_buy"]], 
            marker="^", color="lime", s=120, label="Final Buy")
plt.scatter(df["timestamp"][df["final_sell"]], df["close"][df["final_sell"]], 
            marker="v", color="darkred", s=120, label="Final Sell")

# Stop loss / take profit (only show for final signals)
for i, row in df[df["final_buy"] | df["final_sell"]].iterrows():
    plt.hlines([row["stop_loss"], row["take_profit"]],
               xmin=row["timestamp"], xmax=row["timestamp"], 
               colors=["red", "green"], linestyles="dotted", alpha=0.7)

# Regime shading
plt.fill_between(df["timestamp"], df["close"].min(), df["close"].max(),
                 where=df["regime_ok"], color="lightblue", alpha=0.1,
                 label="Ranging Regime")

plt.title("BTC Signals with Regime Filter & Risk Management", fontsize=16)
plt.xlabel("Time")
plt.ylabel("Price (USDT)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


