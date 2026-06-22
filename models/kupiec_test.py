import numpy as np
from scipy.stats import chi2


def kupiec_test(num_breaches, total_days, alpha=0.95):

    p = 1 - alpha
    x = num_breaches
    T = total_days

    # edge safety
    if T == 0:
        return {
            "LR_pof": 0.0,
            "critical_value": 3.8415,
            "passed": True
        }

    # observed probability
    p_hat = x / T if T > 0 else 0

    # log-likelihood version (stable)
    term1 = x * np.log(p + 1e-12) + (T - x) * np.log(1 - p + 1e-12)
    term2 = x * np.log(p_hat + 1e-12) + (T - x) * np.log(1 - p_hat + 1e-12)

    LR_pof = -2 * (term1 - term2)

    critical_value = chi2.ppf(0.95, df=1)

    return {
        "LR_pof": float(LR_pof),
        "critical_value": float(critical_value),
        "passed": bool(LR_pof <= critical_value)
    }