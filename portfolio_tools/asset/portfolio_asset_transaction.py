class PortfolioAssetTransaction:
    def __init__(
        self,
        date: str,
        transaction_type: str,
        quantity: float,
        price: float,
        currency: str,
        total: float,
        exchange_rate: float,
        subtotal_base: float,
        fees_base: float,
        total_base: float,
    ):
        """
        Represents a transaction for a portfolio asset.

        Args:
            date (str): The date of the transaction (YYYY-MM-DD).
            transaction_type (str): The type of transaction ('buy', 'sell', etc.).
            quantity (float): The quantity of the asset involved in the transaction.
            price (float): The price per unit of the asset.
            currency (str): The currency of the transaction.
            total (float): The total amount of the transaction in the transaction currency.
            exchange_rate (float): The exchange rate to convert to base currency.
            subtotal_base (float): The subtotal in base currency.
            fees_base (float): The fees in base currency.
            total_base (float): The total amount in base currency.
        """
        self.date = date
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.total = total
        self.exchange_rate = exchange_rate
        self.subtotal_base = subtotal_base
        self.fees_base = fees_base
        self.total_base = total_base

    def __repr__(self):
        return (
            f"PortfolioAssetTransaction(date={self.date}, type={self.transaction_type}, quantity={self.quantity}, "
            f"price={self.price}, currency={self.currency}, total={self.total}, exchange_rate={self.exchange_rate}, "
            f"subtotal_base={self.subtotal_base}, fees_base={self.fees_base}, total_base={self.total_base})"
        )
