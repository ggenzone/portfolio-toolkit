from portfolio_toolkit.asset import OptimizationAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider
from portfolio_toolkit.optimization.optimization import Optimization


def create_optimization_from_json(
    data: dict, data_provider: DataProvider
) -> Optimization:
    """
    Loads and validates a JSON file containing optimization information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.
        data_provider (DataProvider): Data provider instance for fetching ticker information.

    Returns:
        Optimization: An instance of the Optimization class with loaded assets.
    """

    # Validate optimization structure
    if "name" not in data or "currency" not in data or "assets" not in data:
        raise ValueError("The JSON does not have the expected optimization format.")

    name = data["name"]
    currency = data["currency"]

    assets = []
    for asset_data in data["assets"]:
        if "ticker" not in asset_data:
            raise ValueError("Each asset must have a 'ticker' field.")

        ticker = asset_data.get("ticker")
        quantity = asset_data.get("quantity", 0)
        info = data_provider.get_ticker_info(ticker)
        prices = data_provider.get_price_series_converted(ticker, currency)

        asset = OptimizationAsset(ticker, prices, info, currency, quantity)
        assets.append(asset)

    return Optimization(
        name=name, currency=currency, assets=assets, data_provider=data_provider
    )
