class Position:
    def __init__(self, ticker: str, buy_price: float, quantity: float):
        """
        Represents a position in the portfolio.

        Args:
            ticker (str): The ticker symbol of the asset.
            buy_price (float): The price at which the asset was purchased.
            quantity (float): The quantity of the asset held.
        """
        self.ticker = ticker
        self.buy_price = buy_price
        self.quantity = quantity
        self.cost = buy_price * quantity  # Total cost of the position

    def __repr__(self):
        return f"Position(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, cost={self.cost})"
