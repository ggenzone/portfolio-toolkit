from datetime import datetime

from portfolio_tools.data_provider.data_provider import DataProvider
from portfolio_tools.portfolio.parser import load_json
from portfolio_tools.portfolio.plot import (
    plot_evolution,
    plot_evolution_stacked,
    plot_evolution_ticker,
    plot_evolution_vs_cost,
)
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

    def calculate_value(self):
        """
        Calculates the total value of the portfolio over time.

        Returns:
            list, list: List of dates and list of total portfolio values.
        """
        historical_prices = {}
        for asset in self.assets:
            ticker = asset["ticker"]
            if ticker not in historical_prices:
                # For cash tickers, don't try to get price from data provider
                if ticker.startswith("__"):
                    # Skip cash tickers in this calculation as they're handled separately
                    continue
                else:
                    historical_prices[ticker] = self.data_provider.get_price_series(
                        ticker
                    )

        if not historical_prices:
            return [], []

        dates = sorted(set(historical_prices[next(iter(historical_prices))].index))
        dates = [
            date for date in dates if date >= self.start_date
        ]  # Filter dates from start_date
        portfolio_value = []

        for date in dates:
            total_value = 0
            for asset in self.assets:
                ticker = asset["ticker"]
                if ticker.startswith("__"):
                    # For cash, add the quantity (since price = 1)
                    current_quantity = self.calculate_current_quantity(ticker, date)
                    total_value += current_quantity  # price = 1.0 for cash
                else:
                    # For stocks, use historical prices
                    if ticker in historical_prices:
                        prices = historical_prices[ticker]
                        if date in prices.index:
                            current_quantity = self.calculate_current_quantity(
                                ticker, date
                            )
                            total_value += prices.loc[date] * current_quantity
            portfolio_value.append(total_value)

        return dates, portfolio_value

    def calculate_current_quantity(self, ticker, date):
        """
        Calculates the accumulated quantity of an asset in the portfolio up to a specific date.
        For cash transactions, handles deposits and withdrawals.

        Args:
            ticker (str): The asset symbol.
            date (datetime): The cutoff date to calculate the accumulated quantity.

        Returns:
            int: Accumulated quantity of the asset up to the specified date.
        """
        current_quantity = 0
        for asset in self.assets:
            if asset["ticker"] == ticker:
                for transaction in asset["transactions"]:
                    if datetime.strptime(transaction["date"], "%Y-%m-%d") <= date:
                        if (
                            transaction["type"] == "buy"
                            or transaction["type"] == "deposit"
                        ):
                            current_quantity += transaction["quantity"]
                        elif (
                            transaction["type"] == "sell"
                            or transaction["type"] == "withdrawal"
                        ):
                            current_quantity -= transaction["quantity"]
        return current_quantity

    def plot_evolution(self):
        plot_evolution(self.df_portfolio)

    def plot_evolution_stacked(self):
        plot_evolution_stacked(self.df_portfolio)

    def plot_evolution_vs_cost(self):
        """
        Plots the evolution of the portfolio value along with the cost of the shares.
        """
        plot_evolution_vs_cost(self.df_portfolio)

    def plot_evolution_ticker(self, ticker):
        plot_evolution_ticker(self.df_portfolio, ticker)

    def print_transactions(self):
        """
        Prints all transactions in CSV format, ordered by date and not grouped by ticker.
        """
        from portfolio_tools.asset.print import print_asset_transactions_csv

        print_asset_transactions_csv(self.assets)

    def print_data_frame(self):
        """
        Prints the portfolio DataFrame in a readable format for debugging purposes.
        """
        print(f"Portfolio '{self.name}' initialized with {len(self.assets)} assets.")
        print(f"Portfolio currency: {self.currency}")
        if self.df_portfolio is not None:
            temp = self.df_portfolio.sort_values(by=["Date"], ascending=True)
            print(temp.to_string())
            print(
                f"Portfolio DataFrame initialized with {len(self.df_portfolio)} records."
            )
        else:
            print("No DataFrame available - portfolio not properly initialized.")
