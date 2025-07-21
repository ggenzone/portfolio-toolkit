from .position import Position


class ValuedPosition(Position):
    def __init__(
        self, ticker: str, buy_price: float, quantity: float, current_price: float
    ):
        """
        Represents a position with its current valuation.

        Args:
            ticker (str): The ticker symbol of the asset.
            buy_price (float): The price at which the asset was purchased.
            quantity (float): The quantity of the asset held.
            current_price (float): The current price of the asset.
        """
        super().__init__(ticker, buy_price, quantity)
        self.current_price = current_price
        self.value = current_price * quantity  # Current value of the position

    def __repr__(self):
        return f"ValuedPosition(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, cost={self.cost}, current_price={self.current_price}, value={self.value})"
