from portfolio_toolkit.position.open.list_from_portfolio import get_open_positions
from portfolio_toolkit.asset import PortfolioAsset
from portfolio_toolkit.asset.portfolio import PortfolioAssetTransaction

def test_get_open_positions_single_asset():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    assets = [asset]
    date = "2025-07-20"
    positions = get_open_positions(assets, date)

    assert len(positions) == 1
    assert positions[0].ticker == "AAPL"
    assert positions[0].cost == 1500
    assert positions[0].quantity == 15
    assert positions[0].value == 0

def test_get_open_positions_multiple_assets():
    transactions_aapl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
    ]
    transactions_googl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=20, price=100, currency="USD", total=2000, exchange_rate=1, subtotal_base=2000, fees_base=0, total_base=2000),
    ]
    asset_aapl = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions_aapl)
    asset_googl = PortfolioAsset(ticker="GOOGL", prices=None, info={}, transactions=transactions_googl)
    assets = [asset_aapl, asset_googl]
    date = "2025-07-19"
    positions = get_open_positions(assets, date)

    assert len(positions) == 2
    assert positions[0].ticker == "AAPL"
    assert positions[0].cost == 1000
    assert positions[0].quantity == 10
    assert positions[1].ticker == "GOOGL"
    assert positions[1].cost == 2000
    assert positions[1].quantity == 20

def test_get_open_positions_no_transactions():
    assets = [
        PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=[]),
        PortfolioAsset(ticker="GOOGL", prices=None, info={}, transactions=[]),
    ]
    date = "2025-07-19"
    positions = get_open_positions(assets, date)

    assert len(positions) == 0  # Should return 0 records when there are no transactions

def test_get_open_positions_date_before_transactions():
    transactions_aapl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
    ]
    transactions_googl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=20, price=100, currency="USD", total=2000, exchange_rate=1, subtotal_base=2000, fees_base=0, total_base=2000),
    ]
    assets = [
        PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions_aapl),
        PortfolioAsset(ticker="GOOGL", prices=None, info={}, transactions=transactions_googl),
    ]
    date = "2025-07-17"
    positions = get_open_positions(assets, date)

    assert len(positions) == 0  # Should return 0 records for dates before any transactions

def test_get_open_positions_multiple_transactions():
    transactions_aapl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="buy", quantity=8, price=100, currency="USD", total=800, exchange_rate=1, subtotal_base=800, fees_base=0, total_base=800),
        PortfolioAssetTransaction(date="2025-07-21", transaction_type="sell", quantity=3, price=100, currency="USD", total=300, exchange_rate=1, subtotal_base=300, fees_base=0, total_base=300),
    ]
    assets = [
        PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions_aapl),
    ]
    date = "2025-07-22"
    positions = get_open_positions(assets, date)

    assert len(positions) == 1
    assert positions[0].ticker == "AAPL"
    assert positions[0].cost == 1000
    assert positions[0].quantity == 10
