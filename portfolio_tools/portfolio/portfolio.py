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
        self.name = None
        self.currency = None
        self.assets = []
        self.start_date = None
        self.df_portfolio = None  # DataFrame to store the portfolio evolution
        self.data_provider = data_provider  # Data provider

        if json_filepath:
            portfolio, self.start_date = load_json(json_filepath)
            self.name = portfolio["name"]
            self.currency = portfolio["currency"]
            self.assets = portfolio["assets"]
            self.df_portfolio = preprocess_data(self.assets, self.start_date, self.data_provider)

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
                    historical_prices[ticker] = self.data_provider.get_price_series(ticker)

        if not historical_prices:
            return [], []

        dates = sorted(set(historical_prices[next(iter(historical_prices))].index))
        dates = [date for date in dates if date >= self.start_date]  # Filter dates from start_date
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
                            current_quantity = self.calculate_current_quantity(ticker, date)
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
                        if transaction["type"] == "buy" or transaction["type"] == "deposit":
                            current_quantity += transaction["quantity"]
                        elif transaction["type"] == "sell" or transaction["type"] == "withdrawal":
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

    def print_current_positions(self, target_date=None):
        from portfolio_tools.portfolio.printer import print_current_positions
        print_current_positions(self.df_portfolio, target_date)

    def print_transactions(self):
        """
        Prints all transactions in CSV format, ordered by date and not grouped by ticker.
        """
        from portfolio_tools.portfolio.printer import print_transactions_csv
        print_transactions_csv(self.assets)

    def print_data_frame(self):
        """
        Prints the portfolio DataFrame in a readable format for debugging purposes.
        """
        print(f"Portfolio '{self.name}' initialized with {len(self.assets)} assets.")
        print(f"Portfolio currency: {self.currency}")
        if self.df_portfolio is not None:
            temp = self.df_portfolio.sort_values(by=['Date'], ascending=True)
            print(temp.to_string())
            print(f"Portfolio DataFrame initialized with {len(self.df_portfolio)} records.")
        else:
            print("No DataFrame available - portfolio not properly initialized.")

    def get_cash_transactions(self):
        """
        Returns transactions for the cash asset (synthetic ticker with __ prefix).
        
        Returns:
            list: List of cash transactions (deposits/withdrawals).
        """
        cash_ticker = f"__{self.currency}"
        for asset in self.assets:
            if asset["ticker"] == cash_ticker:
                return asset["transactions"]
        return []
    
    def get_stock_assets(self):
        """
        Returns only the real stock assets (excluding cash transactions).
        
        Returns:
            list: List of stock assets (excluding synthetic cash ticker).
        """
        return [asset for asset in self.assets if not asset["ticker"].startswith("__")]
    
    def is_cash_ticker(self, ticker):
        """
        Checks if a ticker is a synthetic cash ticker.
        
        Args:
            ticker (str): The ticker to check.
            
        Returns:
            bool: True if it's a cash ticker, False otherwise.
        """
        return ticker.startswith("__")
