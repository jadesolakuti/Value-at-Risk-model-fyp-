import numpy as np


def historical_var(prices, portfolio_value, alpha=0.95, horizon=1):
    log_returns = np.log(prices / prices.shift(1)).dropna()
    weights = np.array([1 / len(prices.columns)] * len(prices.columns))
    historical_returns = (log_returns * weights).sum(axis=1)
    
    if horizon > 1:
        historical_returns = historical_returns.rolling(window=horizon).sum().dropna()
    
    VaR = -np.percentile(historical_returns, (1 - alpha) * 100) * portfolio_value
    es = -historical_returns[historical_returns <= -VaR/portfolio_value].mean() * portfolio_value
    return VaR, es

