import pandas as pd


def calculate_correlation(returns1, returns2):
    """
    Calculates the correlation between two return series.

    Args:
        returns1 (pd.Series): The first return series.
        returns2 (pd.Series): The second return series.

    Returns:
        float: The correlation between the two return series.
    """
    if isinstance(returns1, pd.DataFrame):
        returns1 = returns1.squeeze()
    if isinstance(returns2, pd.DataFrame):
        returns2 = returns2.squeeze()
    return returns1.corr(returns2)
