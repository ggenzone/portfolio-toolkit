from portfolio_toolkit.position.closed.list_from_portfolio import get_closed_positions
from portfolio_toolkit.asset import PortfolioAsset, PortfolioAssetTransaction
from portfolio_toolkit.position import ClosedPosition

def test_get_closed_positions_multiple_assets():
    transactions_aapl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=10, price=100, currency="USD", total=1000, exchange_rate=1, subtotal_base=1000, fees_base=0, total_base=1000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=5, price=120, currency="USD", total=600, exchange_rate=1, subtotal_base=600, fees_base=0, total_base=600),
    ]
    transactions_googl = [
        PortfolioAssetTransaction(date="2025-07-18", transaction_type="buy", quantity=20, price=100, currency="USD", total=2000, exchange_rate=1, subtotal_base=2000, fees_base=0, total_base=2000),
        PortfolioAssetTransaction(date="2025-07-19", transaction_type="sell", quantity=10, price=120, currency="USD", total=1200, exchange_rate=1, subtotal_base=1200, fees_base=0, total_base=1200),
    ]
    asset_aapl = PortfolioAsset(ticker="AAPL", prices=None, info={}, transactions=transactions_aapl)
    asset_googl = PortfolioAsset(ticker="GOOGL", prices=None, info={}, transactions=transactions_googl)
    assets = [asset_aapl, asset_googl]
    from_date = "2025-07-18"
    to_date = "2025-07-20"
    closed_positions = get_closed_positions(assets, from_date, to_date)

    assert len(closed_positions) == 2
    # Check AAPL position
    aapl_position = next(pos for pos in closed_positions if pos.ticker == "AAPL")
    assert aapl_position.quantity == 5
    assert aapl_position.sell_price == 120
    assert aapl_position.buy_price == 100

    # Check GOOGL position
    googl_position = next(pos for pos in closed_positions if pos.ticker == "GOOGL")
    assert googl_position.quantity == 10
    assert googl_position.sell_price == 120
    assert googl_position.buy_price == 100

