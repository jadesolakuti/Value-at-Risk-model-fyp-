from flask import request, jsonify
from utils.plots import plot_historical, plot_parametric, plot_monte_carlo
from models.backtest_var import backtest_var
from models.kupiec_test import kupiec_test


from utils.data_loader import get_prices
from models.historical_var import historical_var
from models.parametric_var import parametric_var
from models.monte_carlo_var import monte_carlo_var
import numpy as np
import pandas as pd



def register_risk_routes(app):

    @app.route("/calculate", methods=["POST"])
    def calculate_risk():
        
        alpha = 0.95
        
        tickers = ['AAPL', 'TSLA', 'NVDA', 'GS', 'JNJ', 'NKE', 'KO', 'XOM']

        portfolio_value = 10000000 #1 million dollars
        #i changed the amount from 10 million naira to 1 million dollars
        
        
        weights = np.array([1/len(tickers)]*len(tickers)) #equally weighted portfolio
        prices = get_prices(tickers)
        log_returns = np.log(prices / prices.shift(1)).dropna()
        portfolio_returns = (log_returns * weights).sum(axis=1)
        portfolio_pnl = portfolio_returns * float(portfolio_value)
        mu = portfolio_returns.mean()
        sigma = portfolio_returns.std()  #portfolio volatility
        print("VOLATILTY from routes: ", sigma)
        print("PORTFOLIO PNL SAMPLE:", portfolio_pnl[:5].values)
        
        log_returns = log_returns.to_frame() if isinstance(log_returns, pd.Series) else log_returns
        
        print("PRICES SHAPE:", prices.shape)
        print("PRICES TYPE:", type(prices))

        print("LOG RETURNS SHAPE:", log_returns.shape)
        print("LOG RETURNS TYPE:", type(log_returns))


        h_var, h_es = historical_var(log_returns,weights,portfolio_value, alpha)
        p_var, p_es = parametric_var(log_returns,weights,portfolio_value, alpha)
        m_var, m_es, mc_losses = monte_carlo_var(log_returns,weights,portfolio_value, alpha)
        
        historical_backtest = backtest_var(
            portfolio_returns,
            h_var,
            portfolio_value
        )
        
        parametric_backtest = backtest_var(
            portfolio_returns,
            p_var,
            portfolio_value
        )

        monte_carlo_backtest = backtest_var(
            portfolio_returns,
            m_var,
            portfolio_value
        )
        
        historical_kupiec = kupiec_test(
            historical_backtest["breaches"],
            historical_backtest["total_days"]
        )

        parametric_kupiec = kupiec_test(
            parametric_backtest["breaches"],
            parametric_backtest["total_days"]
        )

        monte_carlo_kupiec = kupiec_test(
            monte_carlo_backtest["breaches"],
            monte_carlo_backtest["total_days"]
        )

        h_plot = plot_historical(portfolio_pnl, h_var, h_es)
        p_plot = plot_parametric(mu, sigma, portfolio_value, p_var, p_es)
        mc_plot = plot_monte_carlo(mc_losses, m_var, m_es)
        
        # print(type(log_returns))
        # print(log_returns.shape)
        
        print("VAR (historical):", h_var)
        print("Min PnL:", portfolio_pnl.min())
        print("Max PnL:", portfolio_pnl.max())

        breaches = portfolio_pnl <= -h_var
        print("BREACH COUNT:", breaches.sum())
        print("TOTAL OBSERVATIONS:", len(portfolio_pnl))
        print("BREACH RATIO:", breaches.mean())
        # Format numbers with commas and 2 decimal places
        return jsonify({
            "historical": {
                "VaR": round(h_var, 2),
                "ES": round(h_es, 2),
                "plot": h_plot,
                "backtest": historical_backtest,
                "kupiec": historical_kupiec
            },
            "parametric": {
                "VaR": round(p_var, 2),
                "ES": round(p_es, 2),
                "plot": p_plot,
                "backtest": parametric_backtest,
                "kupiec": parametric_kupiec
            },
            "monte_carlo": {
                "VaR": round(m_var, 2),
                "ES": round(m_es, 2),
                "plot": mc_plot,
                "backtest": monte_carlo_backtest,
                "kupiec": monte_carlo_kupiec
            },
           
        })
