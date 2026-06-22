import numpy as np

def monte_carlo_var(log_returns, weights, portfolio_value, alpha=0.95, n_sim=50000):
    # log_returns *= 1.5
    num_days = len(log_returns)
    
    random_indices = np.random.choice(num_days, size=n_sim, replace=True)
    
    simulated_returns = log_returns.iloc[random_indices].values
    
    portfolio_sim_returns = simulated_returns @ weights
    
    pnl = portfolio_value * portfolio_sim_returns
    VaR = -np.percentile(pnl, (1 - alpha) * 100)
    ES = -pnl[pnl <= -VaR].mean()

    return VaR, ES, pnl