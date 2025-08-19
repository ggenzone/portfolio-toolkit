from portfolio_toolkit.position.closed.list_from_portfolio import get_asset_closed_positions
from portfolio_toolkit.asset import PortfolioAsset
from portfolio_toolkit.asset.portfolio import PortfolioAssetTransaction

def test_get_closed_positions_simple_buy_sell():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-20"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)

    assert len(closed_positions) == 1
    assert closed_positions[0].ticker == "AAPL"
    assert closed_positions[0].buy_date == "2025-07-18"
    assert closed_positions[0].sell_date == "2025-07-19"
    assert closed_positions[0].quantity == 5
    assert closed_positions[0].buy_price == 100
    assert closed_positions[0].sell_price == 120

def test_get_closed_positions_multiple_buys_single_sell():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=12, price=120, currency="USD", total=1440, exchange_rate=1, subtotal_base=960, fees_base=0, total_base=1440),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-21"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)

    assert len(closed_positions) == 2
    assert closed_positions[0].buy_date == "2025-07-18"
    assert closed_positions[0].quantity == 10
    assert closed_positions[0].buy_price == 100
    assert closed_positions[0].cost == 1000
    assert closed_positions[0].sell_price == 120
    assert closed_positions[0].sell_date == "2025-07-20"
    assert closed_positions[0].value == 1200

    assert closed_positions[1].buy_date == "2025-07-19"
    assert closed_positions[1].quantity == 2
    assert closed_positions[1].cost == 240
    assert closed_positions[1].buy_price == 120
    assert closed_positions[1].sell_price == 120
    assert closed_positions[1].sell_date == "2025-07-20"
    assert closed_positions[1].value == 240

def test_get_closed_positions_partial_fifo():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=12, price=120, currency="USD", total=1440, exchange_rate=1, subtotal_base=1440, fees_base=0, total_base=1440),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-21"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)

    assert len(closed_positions) == 2
    # First position - full first buy
    assert closed_positions[0].buy_date == "2025-07-18"
    assert closed_positions[0].quantity == 10
    assert closed_positions[0].buy_price == 100
    # Second position - partial second buy
    assert closed_positions[1].buy_date == "2025-07-19"
    assert closed_positions[1].quantity == 2
    assert closed_positions[1].buy_price == 120

def test_get_closed_positions_no_sells():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-20"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)


    assert len(closed_positions) == 0

def test_get_closed_positions_date_filter():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=3, price=120, currency="USD", total=360, exchange_rate=1, subtotal_base=360, fees_base=0, total_base=360),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-19"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)

    assert len(closed_positions) == 1
    assert closed_positions[0].sell_date == "2025-07-19"
    assert closed_positions[0].quantity == 5

def test_get_closed_positions_sell_more_than_available():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=15, price=120, currency="USD", total=1800, exchange_rate=1, subtotal_base=1800, fees_base=0, total_base=1800),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    from_date = "2025-07-18"
    to_date = "2025-07-20"
    closed_positions = get_asset_closed_positions(asset, from_date, to_date)

    assert len(closed_positions) == 1
    assert closed_positions[0].quantity == 10  # Only 10 available to sell
    assert closed_positions[0].cost == 1000
    assert closed_positions[0].value == 1200  # 10 * 120
