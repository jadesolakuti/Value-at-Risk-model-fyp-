import numpy as np
from scipy.stats import norm


def parametric_var(log_returns, weights, portfolio_value, alpha=0.95, horizon=1):
    
    weights = np.array(weights) 
    if not np.isclose(weights.sum(), 1):
        raise ValueError("Weights must sum to 1")

    cov_matrix = log_returns.cov() * 252 #252 trading days in a year
    portfolio_std_dev = np.sqrt(weights.T @ cov_matrix @ weights) #*0.8 is for scaling down for volatility sensitivity
    print("VOLATILTY from parametric: ", portfolio_std_dev)
    
    z = norm.ppf(1 - alpha)
    VaR = -portfolio_value * portfolio_std_dev * z * np.sqrt(horizon/252)
    ES = portfolio_value * portfolio_std_dev * norm.pdf(abs(z)) / (1 - alpha) * np.sqrt(horizon/252)
    return VaR, ES