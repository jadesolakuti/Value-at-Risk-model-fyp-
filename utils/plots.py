import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
import base64
import numpy as np
from scipy.stats import norm

def apply_consistent_style(ax, title, xlabel, ylabel):
    """Applies uniform styling and dollar formatting to any axis."""
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # Use the dollar formatter for the x-axis
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()

def ensure_negative(val):
    """Helper to ensure VaR/ES sit on the left (loss) side of P&L."""
    return -abs(val) if val is not None else None

def plot_historical(pnl, var_line, es_line):
    var_line, es_line = ensure_negative(var_line), ensure_negative(es_line)
    
    plt.figure(figsize=(6, 4))
    pnl = np.array(pnl)
    
    # Histogram using the 'steelblue' from your preferred look
    plt.hist(pnl, bins=50, alpha=0.7, color='steelblue', edgecolor='white', linewidth=0.5)

    # Vertical lines
    plt.axvline(var_line, color='red', linestyle='--', label=f'VaR: ${var_line:,.2f}')
    plt.axvline(es_line, color='darkred', linestyle=':', label=f'ES: ${es_line:,.2f}')

    # Shading the left tail (Actual losses)
    plt.axvspan(pnl.min(), var_line, color='red', alpha=0.15, label='Loss Tail (VaR region)')

    apply_consistent_style(plt.gca(), "Historical VaR Analysis", "Profit / Loss", "Frequency")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

def plot_parametric(mu, sigma, portfolio_value, var_value, es_value):
    var_value, es_value = ensure_negative(var_value), ensure_negative(es_value)
    
    plt.figure(figsize=(6, 4))
    mu_pnl = mu * portfolio_value
    sigma_pnl = sigma * portfolio_value
    
    # Generate distribution curve
    x_pnl = np.linspace(mu_pnl - 4*sigma_pnl, mu_pnl + 4*sigma_pnl, 500)
    y = norm.pdf(x_pnl, mu_pnl, sigma_pnl)

    plt.plot(x_pnl, y, color='steelblue', linewidth=2, label="Normal Distribution")
    
    # Vertical lines
    plt.axvline(var_value, color='red', linestyle='--', label=f"VaR: ${var_value:,.2f}")
    plt.axvline(es_value, color='darkred', linestyle=':', label=f"ES: ${es_value:,.2f}")

    # Shading the left tail under the curve
    mask = x_pnl <= var_value
    plt.fill_between(x_pnl[mask], y[mask], color='red', alpha=0.15, label='Loss Tail')

    apply_consistent_style(plt.gca(), "Parametric VaR Analysis", "Profit / Loss", "Probability Density")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

def plot_monte_carlo(pnl, var_value, es_value=None):
    # Ensure input is treated as P&L (negative = loss)
    var_value, es_value = ensure_negative(var_value), ensure_negative(es_value)
    
    plt.figure(figsize=(6, 4))
    pnl = np.array(pnl)
    
    plt.hist(pnl, bins=60, alpha=0.7, color='steelblue', edgecolor='white', linewidth=0.5)

    plt.axvline(var_value, color='red', linestyle='--', label=f'VaR: ${var_value:,.2f}')
    if es_value is not None:
        plt.axvline(es_value, color='darkred', linestyle=':', label=f'ES: ${es_value:,.2f}')

    # Shading the left tail
    plt.axvspan(pnl.min(), var_value, color='red', alpha=0.15, label='Loss Tail')

    apply_consistent_style(plt.gca(), "Monte Carlo VaR Analysis", "Profit / Loss", "Frequency")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()