# src/indicators.py

import pandas as pd
from scipy.signal import savgol_filter

def add_savgol(df, window=21, poly=3):
    """Add Savitzky–Golay smoothed price and slope."""
    df = df.copy()
    df["SG_Filter"] = savgol_filter(df["close"], window_length=window, polyorder=poly)
    df["slope"] = savgol_filter(df["close"], window_length=window, polyorder=poly, deriv=1)
    return df

def add_atr(df, period=14):
    """Add ATR to dataframe."""
    df = df.copy()
    df["prev_close"] = df["close"].shift(1)
    df["tr1"] = df["high"] - df["low"]
    df["tr2"] = (df["high"] - df["prev_close"]).abs()
    df["tr3"] = (df["low"] - df["prev_close"]).abs()
    df["TR"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(window=period).mean()
    return df
