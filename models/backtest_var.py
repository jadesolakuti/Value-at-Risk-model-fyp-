import numpy as np

def backtest_var(portfolio_returns, var_value, portfolio_value):

    # Convert returns to monetary losses
    pnl = portfolio_returns * portfolio_value

    # Actual losses
    losses = -pnl

    # Breaches occur when actual loss exceeds VaR
    breaches = losses > var_value

    num_breaches = breaches.sum()

    total_days = len(losses)

    breach_ratio = num_breaches / total_days

    return {
        "breaches": int(num_breaches),
        "total_days": total_days,
        "breach_ratio": breach_ratio
    }