from portfolio_tools.data_provider.data_provider import DataProvider
from portfolio_tools.portfolio.parser import load_json
from portfolio_tools.portfolio.preprocesador import preprocess_data


class Portfolio:
    """
    Class to represent and manage an asset portfolio.
    """

    def __init__(self, json_filepath: str, data_provider: DataProvider):
        """
        Initializes the Portfolio class and optionally loads data from a JSON file.

        Args:
            json_filepath (str, optional): Path to the JSON file to load data from.
            data_provider (DataProvider, optional): Data provider to obtain historical prices.

        Returns:
            None
        """
        self.name = None
        self.currency = None
        self.assets = []
        self.start_date = None
        self.df_portfolio = None  # DataFrame to store the portfolio evolution
        self.data_provider = data_provider  # Data provider
        self.account = None  # Placeholder for account information

        if json_filepath:
            portfolio, assets, account, self.start_date = load_json(
                json_filepath, data_provider
            )
            self.name = portfolio["name"]
            self.currency = portfolio["currency"]
            self.assets = assets
            self.account = account

            # Include cash account in assets if it has transactions
            # if account and "transactions" in account and account["transactions"]:
            #    cash_ticker = f"__{account['currency']}"
            #    cash_asset = {
            #        "ticker": cash_ticker,
            #        "transactions": account["transactions"]
            #    }
            #    self.assets.append(cash_asset)

            self.df_portfolio = preprocess_data(
                self.assets, self.start_date, self.data_provider, self.currency
            )
