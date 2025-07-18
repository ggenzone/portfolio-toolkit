from portfolio_tools.asset.create import create_asset

def test_create_asset_cash():
    ticker = "__USD"
    expected = {
        "ticker": "__USD",
        "transactions": [],
        "sector": "Cash",
        "country": "Unknown",
    }
    assert create_asset(ticker) == expected

def test_create_asset_non_cash():
    ticker = "AAPL"
    expected = {
        "ticker": "AAPL",
        "transactions": [],
        "sector": "Unknown",
        "country": "Unknown",
    }
    assert create_asset(ticker) == expected
