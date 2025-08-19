from portfolio_toolkit.position.open.list_from_portfolio import get_asset_open_positions
from portfolio_toolkit.asset import PortfolioAsset, PortfolioAssetTransaction

def test_get_asset_open_positions_buy_only():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-20"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 15
    assert result.cost == 1500
    assert result.buy_price == 100

def test_get_asset_open_positions_buy_and_sell():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-20"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 5
    assert result.cost == 500
    assert result.buy_price == 100

def test_get_asset_open_positions_sell_more_than_available():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=15, price=100, currency="USD", total=1500, exchange_rate=1, subtotal_base=1500, fees_base=0, total_base=1500),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-20"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 0
    assert result.cost == 0
    assert result.buy_price == 0

def test_get_asset_open_positions_multiple_buys_and_sells():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=8, price=100, currency="USD", total=800, exchange_rate=1, subtotal_base=800, fees_base=0, total_base=800),
        PortfolioAssetTransaction(date="2025-07-21", transaction_type="sell", quantity=4, price=100, currency="USD", total=400, exchange_rate=1, subtotal_base=400, fees_base=0, total_base=400),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-22"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 3
    assert result.cost == 300
    assert result.buy_price == 100

def test_get_asset_open_positions_partial_sell():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=3, price=100, currency="USD", total=300, exchange_rate=1, subtotal_base=300, fees_base=0, total_base=300),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=2, price=100, currency="USD", total=200, exchange_rate=1, subtotal_base=200, fees_base=0, total_base=200),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-21"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 5
    assert result.cost == 500
    assert result.buy_price == 100

def test_get_asset_open_positions_date_within_transactions():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=8, price=100, currency="USD", total=800, exchange_rate=1, subtotal_base=800, fees_base=0, total_base=800),
        PortfolioAssetTransaction(date="2025-07-21", transaction_type="sell", quantity=4, price=100, currency="USD", total=400, exchange_rate=1, subtotal_base=400, fees_base=0, total_base=400),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-20"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 7
    assert result.cost == 700
    assert result.buy_price == 100

def test_get_asset_open_positions_date_within_transactions_partial_sell():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=3, price=100, currency="USD", total=300, exchange_rate=1, subtotal_base=300, fees_base=0, total_base=300),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=2, price=100, currency="USD", total=200, exchange_rate=1, subtotal_base=200, fees_base=0, total_base=200),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    date = "2025-07-19"
    result = get_asset_open_positions(asset, date)
    assert result.quantity == 7
    assert result.cost == 700
    assert result.buy_price == 100

def test_get_asset_open_positions_multiple_dates():
    transactions = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="buy", quantity=5, price=100, currency="USD", total=500, exchange_rate=1, subtotal_base=500, fees_base=0, total_base=500),
        PortfolioAssetTransaction(date="2025-07-20", transaction_type="sell", quantity=8, price=100, currency="USD", total=800, exchange_rate=1, subtotal_base=800, fees_base=0, total_base=800),
        PortfolioAssetTransaction(date="2025-07-21", transaction_type="sell", quantity=4, price=100, currency="USD", total=400, exchange_rate=1, subtotal_base=400, fees_base=0, total_base=400),
    ]
    asset = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions)
    # Assert for date 2025-07-19
    date_1 = "2025-07-19"
    expected_1 = {"quantity": 15, "cost": 1500, "average_price": 100}
    result_1 = get_asset_open_positions(asset, date_1)
    assert result_1.quantity == expected_1["quantity"]
    assert result_1.cost == expected_1["cost"]
    assert result_1.buy_price == expected_1["average_price"]

    # Assert for date 2025-07-20
    date_2 = "2025-07-20"
    expected_2 = {"quantity": 7, "cost": 700, "average_price": 100}
    result_2 = get_asset_open_positions(asset, date_2)
    assert result_2.quantity == expected_2["quantity"]
    assert result_2.cost == expected_2["cost"]
    assert result_2.buy_price == expected_2["average_price"]

    # Assert for date 2025-07-21
    date_3 = "2025-07-21"
    expected_3 = {"quantity": 3, "cost": 300, "average_price": 100}
    result_3 = get_asset_open_positions(asset, date_3)
    assert result_3.quantity == expected_3["quantity"]
    assert result_3.cost == expected_3["cost"]
    assert result_3.buy_price == expected_3["average_price"]
