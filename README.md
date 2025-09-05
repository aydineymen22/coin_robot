# coin_robot
# 📈 Bitcoin Local Extrema Trading Bot

This project implements a **Bitcoin trading strategy** based on detecting **local maxima and minima** in price movements.  
The algorithm buys at **local minima** and sells at **local maxima**, using volatility filters (ATR) to avoid noise.  

The project is structured into four Python modules:
1. **fetching_data.py** → Fetch historical BTC data using `ccxt`  
2. **price_smoother.py** → Apply smoothing (EMA, Savitzky–Golay) & calculate derivatives  
3. **local_min_max.py** → Detect extrema, generate buy/sell signals with ATR filter  
4. **bot.py** → Paper trade live BTC/USDT with simulated PnL logging  
5. **indicator.py** → Creating savgol filters
6. **backtesting.py** → Testing the code wit vectorbt
7. **trades.csv** → For logging buy and sell signals created
---

## 🚀 Features
- Fetch OHLCV (Open-High-Low-Close-Volume) candlestick data  
- Smooth price series and compute slope/curvature  
- Detect local maxima/minima and place trades  
- ATR-based filtering to reduce false signals  
- Backtesting with fees & slippage  
- Live paper trading with trade logging  

---
Note: I have recently started learning finance so with knowledge I have so far I created this project. I am going to enhance this project while I proceed learning.
Note: I accumulated all of the code into bot.py;thus, you only need to use bot.py. The others I created while I learning. 

🔒 Disclaimer
This bot is for educational purposes only.
Cryptocurrency trading involves high risk, and past performance does not guarantee future results.
Use at your own risk.
