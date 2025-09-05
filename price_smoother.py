import pandas as pd
from datetime import datetime, timedelta
import time 
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.signal import savgol_filter


df = pd.read_csv("btc_data.csv", parse_dates=['timestamp'])

df['SG_filter'] = savgol_filter(df['close'], window_length=21, polyorder=3)

df['slope'] = df['SG_filter'].diff()
df['curvature'] = df['slope'].diff()


fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Price + smoothing
axes[0].plot(df["timestamp"], df["close"], label="Close Price", alpha=0.6)
axes[0].plot(df["timestamp"], df["SG_filter"], label="Savitzky–Golay Smoothed", linewidth=2)
axes[0].set_title("BTC/USDT Price (Savitzky–Golay Filter)")
axes[0].legend()
axes[0].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Slope (1st derivative)
axes[1].plot(df["timestamp"], df["slope"], color="green")
axes[1].set_title("First Derivative (Slope)")

# Curvature (2nd derivative)
axes[2].plot(df["timestamp"], df["curvature"], color="red")
axes[2].set_title("Second Derivative (Curvature)")

plt.tight_layout()
plt.savefig("../images/btc_savgol_derivatives.png")
plt.show()