import numpy as np
#horizon = day

def historical_var(log_returns, weights, portfolio_value, alpha=0.95, horizon=1):
    weights = np.array(weights) 
    if not np.isclose(weights.sum(), 1):
        raise ValueError("Weights must sum to 1")
    
    # log_returns *= 1.5
    
    log_returns = log_returns.iloc[:, :len(weights)]
    log_returns = log_returns.copy()

    historical_returns = log_returns.dot(weights)
    if horizon > 1:
        historical_returns = historical_returns.rolling(window=horizon).sum().dropna()
    
    VaR_return = np.percentile(historical_returns, (1 - alpha) * 100)
    VaR = -VaR_return * portfolio_value

    ES = -historical_returns[historical_returns <= VaR_return].mean() * portfolio_value
    return VaR, ES


