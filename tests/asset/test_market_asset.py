import pytest
import pandas as pd
from portfolio_toolkit.asset.market.market_asset import MarketAsset
from portfolio_toolkit.asset.market.market_asset_list import MarketAssetList

def test_market_asset_to_dict_and_repr():
    prices = pd.Series([100, 101, 102], index=pd.date_range("2024-01-01", periods=3))
    info = {"sector": "Tech", "country": "USA", "currency": "USD"}
    asset = MarketAsset(ticker="AAPL", prices=prices, info=info)
    d = asset.to_dict()
    assert d["ticker"] == "AAPL"
    assert d["sector"] == "Tech"
    assert d["country"] == "USA"
    assert d["currency"] == "USD"
    r = repr(asset)
    assert "AAPL" in r and "Tech" in r and "USD" in r

def test_market_asset_missing_info_defaults():
    prices = pd.Series([10, 11], index=pd.date_range("2024-01-01", periods=2))
    asset = MarketAsset(ticker="TSLA", prices=prices, info={})
    d = asset.to_dict()
    assert d["sector"] == "Unknown"
    assert d["country"] == "Unknown"
    assert d["currency"] == "Unknown"

def test_market_asset_list_to_list_and_dataframe():
    prices1 = pd.Series([1, 2], index=pd.date_range("2024-01-01", periods=2))
    prices2 = pd.Series([3, 4], index=pd.date_range("2024-01-01", periods=2))
    asset1 = MarketAsset(ticker="AAPL", prices=prices1, info={"sector": "Tech", "country": "USA"})
    asset2 = MarketAsset(ticker="TSLA", prices=prices2, info={"sector": "Auto", "country": "USA"})
    mal = MarketAssetList([asset1, asset2])
    l = mal.to_list()
    assert isinstance(l, list) and len(l) == 2
    df = mal.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert set(df["ticker"]) == {"AAPL", "TSLA"}
