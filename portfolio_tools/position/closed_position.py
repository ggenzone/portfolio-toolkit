from dataclasses import dataclass, field

from .position import Position


@dataclass
class ClosedPosition(Position):
    buy_date: str
    sell_price: float
    sell_date: str
    value: float = field(init=False)
    profit: float = field(init=False)
    return_percentage: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()  # Calcula `cost` desde Position
        self.value = self.sell_price * self.quantity
        self.profit = self.value - self.cost
        self.return_percentage = (
            (self.profit / self.cost * 100) if self.cost != 0 else 0
        )

    def __repr__(self):
        return (
            f"ClosedPosition(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, "
            f"cost={self.cost}, buy_date={self.buy_date}, sell_price={self.sell_price}, "
            f"sell_date={self.sell_date}, value={self.value}, profit={self.profit}, "
            f"return_percentage={self.return_percentage})"
        )
