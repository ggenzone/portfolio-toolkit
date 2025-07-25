from dataclasses import dataclass
from typing import List

from portfolio_toolkit.account.account import Account
from portfolio_toolkit.asset.portfolio_asset import PortfolioAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider


@dataclass
class Portfolio:
    name: str
    currency: str
    assets: List[PortfolioAsset]
    data_provider: DataProvider
    account: Account
    start_date: str  # = field(init=False)

    # def __post_init__(self):
    #    # Determina la fecha más antigua de las transacciones de todos los activos
    #    all_dates = []
    #    for asset in self.assets:
    #        for tx in asset.transactions:
    #            all_dates.append(tx.date)

    #    if all_dates:
    #        self.start_date = min(all_dates)
    #    else:
    #        self.start_date = "N/A"  # o lanzar una excepción si es requerido

    def __repr__(self):
        return (
            f"Portfolio(name={self.name}, currency={self.currency}, "
            f"assets={len(self.assets)}, start_date={self.start_date}, "
            f"data_provider={type(self.data_provider).__name__}, "
            f"account={self.account})"
        )
