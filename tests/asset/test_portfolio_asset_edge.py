import pytest
import pandas as pd
from portfolio_toolkit.asset.portfolio.portfolio_asset import PortfolioAsset
from portfolio_toolkit.asset.portfolio.portfolio_asset_transaction import PortfolioAssetTransaction

def test_portfolio_asset_empty_transactions():
    prices = pd.Series([10, 12], index=pd.date_range("2024-01-01", periods=2))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={}, currency="USD")
    assert asset.transactions == []
    df = PortfolioAsset.to_dataframe([asset])
    assert df.empty

def test_portfolio_asset_add_split_no_positions():
    prices = pd.Series([10, 12], index=pd.date_range("2024-01-01", periods=2))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={}, currency="USD")
    split_dict = {"date": pd.Timestamp("2024-01-02"), "split_factor": 2.0}
    cash = asset.add_split(split_dict)
    assert cash == 0.0
    assert len(asset.transactions) == 0

def test_portfolio_asset_add_transaction_invalid_dict():
    prices = pd.Series([10, 12], index=pd.date_range("2024-01-01", periods=2))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={}, currency="USD")
    # Falta campo obligatorio 'date'
    tx_dict = {"type": "buy", "quantity": 1, "price": 12, "currency": "USD", "total": 12, "exchange_rate": 1.0, "subtotal_base": 12, "fees_base": 0, "total_base": 12}
    with pytest.raises(KeyError):
        asset.add_transaction_from_dict(tx_dict)

def test_portfolio_asset_repr_with_many_transactions():
    prices = pd.Series([10, 12, 14], index=pd.date_range("2024-01-01", periods=3))
    asset = PortfolioAsset(ticker="AAPL", prices=prices, info={"sector": "Tech"}, currency="USD")
    for i in range(10):
        tx = PortfolioAssetTransaction(
            date=pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
            transaction_type="buy",
            quantity=1,
            price=10 + i,
            currency="USD",
            total=10 + i,
            exchange_rate=1.0,
            subtotal_base=10 + i,
            fees_base=0,
            total_base=10 + i,
        )
        asset.add_transaction(tx)
    r = repr(asset)
    assert "transactions_count=10" in r
