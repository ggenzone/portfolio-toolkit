import numpy as np
import pandas as pd


def get_log_returns(price_series: pd.Series) -> pd.Series:
    """
    Calculates the logarithmic returns of a price series.

    Args:
        price_series (pd.Series): Series of prices.

    Returns:
        pd.Series: Series of logarithmic returns.
    """
    return price_series.pct_change().apply(lambda x: np.log(1 + x))
