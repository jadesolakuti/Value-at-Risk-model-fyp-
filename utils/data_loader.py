import yfinance as yf
import datetime as dt
import pandas as pd

def get_prices(tickers):
    startdate = "2016-01-01"
    enddate = "2025-12-31"
    adj_close_df = pd.DataFrame()
    
    for ticker in tickers:
        data = yf.download(ticker, start=startdate, end=enddate)
        if "Adj Close" in data.columns:
            adj_close_df[ticker] = data['Adj Close']
        else:
            adj_close_df[ticker] = data['Close']
        
    return adj_close_df