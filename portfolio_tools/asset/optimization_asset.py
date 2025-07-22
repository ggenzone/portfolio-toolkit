from dataclasses import dataclass

from .market_asset import MarketAsset


@dataclass
class OptimizationAsset(MarketAsset):
    quantity: float = 0.0  # evitar el error

    def __repr__(self):
        return (
            f"OptimizationAsset(ticker={self.ticker}, sector={self.sector}, currency={self.currency}, "
            f"quantity={self.quantity}, prices_length={len(self.prices)}, info_keys={list(self.info.keys())})"
        )
