from ccxt import binance
import pandas as pd
from datetime import datetime, timedelta
import time
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


exchange = binance()

symbol = 'BTC/USDT'
timeframe = '1h'

now = datetime.now()

since = int((now - timedelta(days=90)).timestamp() * 1000)  

all_candles = []
limit = 1000

while True:
    candles = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    if not candles:
        break
    all_candles += candles
    since = candles[-1][0] + 1 
    time.sleep(exchange.rateLimit / 1000)
    if candles[-1][0] >= int(now.timestamp() * 1000):
        break

df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.to_csv("btc_data.csv", index=False)


# print(df.head())


df['previous_close'] = df['close'].shift(1)
df['tr1'] = df['high'] - df['low']
df['tr2'] = abs(df['high'] - df['previous_close'])
df['tr3'] = abs(df['low'] - df['previous_close'])
df['TR'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)

period = 14
df['ATR'] = df['TR'].rolling(window=period).mean()



fig = plt.figure(figsize=(12,8))

ax1 = fig.add_subplot(2, 1, 1)  
ax1.plot(df['timestamp'], df['close'], color='blue', label='Close Price')
ax1.set_title('BTC/USDT Close Price')
ax1.set_ylabel('Price (USDT)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax1.legend(loc='upper left')

ax2 = fig.add_subplot(2, 1, 2)  
ax2.plot(df['timestamp'], df['ATR'], color='orange', label='14-period ATR')
ax2.set_title('Average True Range (ATR)')
ax2.set_ylabel('ATR', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')
ax2.tick_params(axis='x', rotation=45)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig('../images/btc_atr_plot.png')
plt.show()
