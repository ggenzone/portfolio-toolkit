from dataclasses import dataclass, field

from .position import Position


@dataclass
class ValuedPosition(Position):
    current_price: float
    sector: str
    country: str
    value: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()  # Calcula cost
        self.value = self.current_price * self.quantity

    def __repr__(self):
        return (
            f"ValuedPosition(ticker={self.ticker}, buy_price={self.buy_price}, quantity={self.quantity}, "
            f"cost={self.cost}, current_price={self.current_price}, value={self.value})"
        )
