import pytest
import pandas as pd
from portfolio_toolkit.asset.portfolio.portfolio_asset import PortfolioAsset
from portfolio_toolkit.asset.portfolio.portfolio_asset_transaction import PortfolioAssetTransaction


def test_portfolio_asset_add_transaction_and_repr():
    prices = pd.Series([10, 12, 14], index=pd.date_range("2024-01-01", periods=3))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={"sector": "Tech"}, currency="USD")
    tx = PortfolioAssetTransaction(
        date=pd.Timestamp("2024-01-01"),
        transaction_type="buy",
        quantity=2,
        price=10,
        currency="USD",
        total=20,
        exchange_rate=1.0,
        subtotal_base=20,
        fees_base=0,
        total_base=20,
    )
    asset.add_transaction(tx)
    assert len(asset.transactions) == 1
    assert asset.transactions[0].quantity == 2
    r = repr(asset)
    assert "AAPL" in r and "Tech" in r


def test_portfolio_asset_add_transaction_from_dict():
    prices = pd.Series([10, 12], index=pd.date_range("2024-01-01", periods=2))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={}, currency="USD")
    tx_dict = {
        "date": pd.Timestamp("2024-01-02"),
        "type": "buy",
        "quantity": 1,
        "price": 12,
        "currency": "USD",
        "total": 12,
        "exchange_rate": 1.0,
        "subtotal_base": 12,
        "fees_base": 0,
        "total_base": 12,
    }
    asset.add_transaction_from_dict(tx_dict)
    assert len(asset.transactions) == 1
    assert asset.transactions[0].price == 12

