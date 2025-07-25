from dataclasses import dataclass


@dataclass
class PortfolioAssetTransaction:
    date: str
    transaction_type: str
    quantity: float
    price: float
    currency: str
    total: float
    exchange_rate: float
    subtotal_base: float
    fees_base: float
    total_base: float

    def __repr__(self):
        return (
            f"PortfolioAssetTransaction(date={self.date}, type={self.transaction_type}, quantity={self.quantity}, "
            f"price={self.price}, currency={self.currency}, total={self.total}, exchange_rate={self.exchange_rate}, "
            f"subtotal_base={self.subtotal_base}, fees_base={self.fees_base}, total_base={self.total_base})"
        )
