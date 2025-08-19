import pytest
import pandas as pd
from portfolio_toolkit.asset.optimization.optimization_asset import OptimizationAsset

def test_optimization_asset_properties_and_repr():
    prices = pd.Series([100, 102, 101, 105], index=pd.date_range("2024-01-01", periods=4))
    asset = OptimizationAsset(ticker="AAPL", prices=prices, info={"sector": "Tech"}, currency="USD", quantity=5)
    # returns, log_returns, mean_return, volatility should be set
    assert hasattr(asset, "returns")
    assert hasattr(asset, "log_returns")
    assert abs(asset.mean_return - asset.log_returns.mean()) < 1e-8
    assert abs(asset.volatility - asset.log_returns.std()) < 1e-8
    assert asset.quantity == 5
    r = repr(asset)
    assert "AAPL" in r and "Tech" in r

def test_optimization_asset_to_dataframe():
    prices1 = pd.Series([10, 11, 12], index=pd.date_range("2024-01-01", periods=3))
    prices2 = pd.Series([20, 19, 21], index=pd.date_range("2024-01-01", periods=3))
    asset1 = OptimizationAsset(ticker="AAPL", prices=prices1, info={"sector": "Tech"}, currency="USD", quantity=2)
    asset2 = OptimizationAsset(ticker="TSLA", prices=prices2, info={"sector": "Auto"}, currency="USD", quantity=3)
    df = OptimizationAsset.to_dataframe([asset1, asset2])
    assert set(df["ticker"]) == {"AAPL", "TSLA"}
    assert set(df["quantity"]) == {2, 3}
