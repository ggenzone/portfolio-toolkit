from dataclasses import dataclass, field


@dataclass
class Position:
    ticker: str
    buy_price: float
    quantity: float
    cost: float = field(init=False)

    def __post_init__(self):
        self.cost = self.buy_price * self.quantity

    def __repr__(self):
        return (
            f"Position(ticker={self.ticker}, buy_price={self.buy_price}, "
            f"quantity={self.quantity}, cost={self.cost})"
        )
