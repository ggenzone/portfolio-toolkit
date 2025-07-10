from datetime import datetime
from portfolio_tools.portfolio.parser import load_json
from portfolio_tools.portfolio.preprocesador import preprocess_data
from portfolio_tools.portfolio.plot import plot_composition, plot_evolution, plot_evolution_stacked, plot_evolution_vs_cost, plot_evolution_ticker

class Portfolio:
    """
    Class to represent and manage an asset portfolio.
    """
    def __init__(self, json_filepath=None, data_provider=None):
        """
        Initializes the Portfolio class and optionally loads data from a JSON file.

        Args:
            json_filepath (str, optional): Path to the JSON file to load data from.
            data_provider (DataProvider, optional): Data provider to obtain historical prices.

        Returns:
            None
        """
        self.assets = []
        self.start_date = None
        self.df_portfolio = None  # DataFrame to store the portfolio evolution
        self.data_provider = data_provider  # Data provider

        if json_filepath:
            self.assets, self.start_date = load_json(json_filepath)
            self.df_portfolio = preprocess_data(self.assets, self.start_date, self.data_provider)

    def calculate_value(self):
        """
        Calculates the total value of the portfolio over time.

        Returns:
            list, list: List of dates and list of total portfolio values.
        """
        historical_prices = {}
        for asset in self.assets:
            if asset["ticker"] not in historical_prices:
                historical_prices[asset["ticker"]] = self.data_provider.get_price_series(asset["ticker"])

        dates = sorted(set(historical_prices[next(iter(historical_prices))].index))
        dates = [date for date in dates if date >= self.start_date]  # Filter dates from start_date
        portfolio_value = []

        for date in dates:
            total_value = 0
            for asset in self.assets:
                prices = historical_prices[asset["ticker"]]
                if date in prices.index:
                    current_quantity = self.calculate_current_quantity(asset["ticker"], date)
                    total_value += prices.loc[date] * current_quantity
            portfolio_value.append(total_value)

        return dates, portfolio_value

    def calculate_current_quantity(self, ticker, date):
        """
        Calculates the accumulated quantity of an asset in the portfolio up to a specific date.

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
                        if transaction["type"] == "buy":
                            current_quantity += transaction["quantity"]
                        elif transaction["type"] == "sell":
                            current_quantity -= transaction["quantity"]
        return current_quantity

    def plot_composition(self, group_by="Ticker"):
        plot_composition(self.df_portfolio, group_by)

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

    def print_current_positions(self):
        from portfolio_tools.portfolio.printer import print_current_positions
        print_current_positions(self.df_portfolio)
