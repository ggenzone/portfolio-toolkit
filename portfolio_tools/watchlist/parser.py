import json
from portfolio_tools.asset.market_asset import MarketAsset
from portfolio_tools.data_provider.data_provider import DataProvider
from portfolio_tools.watchlist.watchlist import Watchlist

def create_watchlist_from_json(
    json_filepath: str, data_provider: DataProvider
) -> Watchlist:
    """
    Loads and validates a JSON file containing watchlist information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.
        data_provider (DataProvider): Data provider instance for fetching ticker information.

    Returns:
        Watchlist: An instance of the Watchlist class with loaded assets.
    """
    with open(json_filepath, mode="r", encoding="utf-8") as file:
        data = json.load(file)

        # Validate watchlist structure
        if "name" not in data or "currency" not in data or "assets" not in data:
            raise ValueError("The JSON does not have the expected watchlist format.")

        name = data["name"]
        currency = data["currency"]

        assets = []
        for asset_data in data["assets"]:
            if "ticker" not in asset_data:
                raise ValueError("Each asset must have a 'ticker' field.")
            
            ticker = asset_data.get("ticker")
            info = data_provider.get_asset_info(ticker)
            prices = data_provider.get_price_series_converted(
                ticker, currency
            )
            
            asset = MarketAsset(ticker, prices, info, currency)
            assets.append(asset)

        return Watchlist(name=name, currency=currency, assets=assets, data_provider=data_provider)