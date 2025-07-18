def create_asset(ticker):
    """
    Creates an initial asset object for a given ticker.

    Args:
        ticker (str): The ticker for the asset.

    Returns:
        dict: The initial asset object.
    """
    return {
        "ticker": ticker,
        "transactions": [],
        "sector": "Cash" if ticker.startswith("__") else "Unknown",
        "country": "Unknown",
    }
