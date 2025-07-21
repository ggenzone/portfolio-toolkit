from .position import Position


class ClosedPosition(Position):
    def __init__(
        self,
        ticker: str,
        buy_price: float,
        quantity: float,
        buy_date: str,
        sell_price: float,
        sell_date: str,
    ):
        """
        Represents a closed position in the portfolio.

        Args:
            ticker (str): The ticker symbol of the asset.
            buy_price (float): The price at which the asset was purchased.
            quantity (float): The quantity of the asset sold.
            buy_date (str): The date the asset was purchased (YYYY-MM-DD).
            sell_price (float): The price at which the asset was sold.
            sell_date (str): The date the asset was sold (YYYY-MM-DD).
        """
        super().__init__(ticker, buy_price, quantity)
        self.buy_date = buy_date
        self.sell_price = sell_price
        self.sell_date = sell_date
        self.value = sell_price * quantity  # Total value of the closed position

    def __repr__(self):
        return (
            f"ClosedPosition(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, "
            f"cost={self.cost}, buy_date={self.buy_date}, sell_price={self.sell_price}, "
            f"sell_date={self.sell_date}, value={self.value})"
        )
