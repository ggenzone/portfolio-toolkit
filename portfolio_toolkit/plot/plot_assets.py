# Moved from plot/plot_assets.py to portfolio_tools/plot/plot_assets.py
import matplotlib.pyplot as plt


def plot_assets(price_series_list, asset_names):
    """
    Plots the closing prices for multiple assets.

    Args:
        price_series_list (list of pd.Series): List of closing price series.
        asset_names (list of str): List of asset names.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    for prices, name in zip(price_series_list, asset_names):
        plt.plot(prices, label=name)

    plt.title("Asset Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    plt.grid()
    plt.show()
