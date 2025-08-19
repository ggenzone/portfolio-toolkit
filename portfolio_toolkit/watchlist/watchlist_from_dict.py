from portfolio_toolkit.asset import MarketAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider
from portfolio_toolkit.watchlist.watchlist import Watchlist


def create_watchlist(data: dict, data_provider: DataProvider) -> Watchlist:
    """
    Loads and validates a JSON file containing watchlist information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.
        data_provider (DataProvider): Data provider instance for fetching ticker information.

    Returns:
        Watchlist: An instance of the Watchlist class with loaded assets.
    """

    # Validate watchlist structure
    if "name" not in data or "assets" not in data:
        raise ValueError("The JSON does not have the expected watchlist format.")

    currency = None
    if "currency" in data:
        currency = data["currency"]

    name = data["name"]

    assets = []
    for asset_data in data["assets"]:
        if "ticker" not in asset_data:
            raise ValueError("Each asset must have a 'ticker' field.")

        ticker = asset_data.get("ticker")
        info = data_provider.get_ticker_info(ticker)
        if currency is None:
            prices = data_provider.get_price_series(ticker)
        else:
            prices = data_provider.get_price_series_converted(ticker, currency)

        asset = MarketAsset(ticker, prices, info, currency)
        assets.append(asset)

    return Watchlist(
        name=name, currency=currency, assets=assets, data_provider=data_provider
    )
