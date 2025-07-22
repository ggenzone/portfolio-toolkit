import io
import sys
import pandas as pd
from portfolio_tools.asset.print import print_asset_transactions_csv
from portfolio_tools.asset.portfolio_asset import PortfolioAsset
from portfolio_tools.asset.portfolio_asset_transaction import PortfolioAssetTransaction

def test_print_asset_transactions_csv():
    # Create test assets using the actual classes
    prices = pd.Series([150.0, 151.0, 152.0])
    info = {'sector': 'Technology', 'country': 'US'}
    
    # Create first asset (AAPL)
    asset1 = PortfolioAsset(ticker='AAPL', prices=prices, info=info, currency='USD')
    transaction1 = PortfolioAssetTransaction(
        date="2025-07-18",
        transaction_type="buy",
        quantity=10.0,
        price=150.00,
        currency="USD",
        total=1500.00,
        exchange_rate=1.00,
        subtotal_base=1500.00,
        fees_base=0.00,
        total_base=1500.00,
    )
    asset1.add_transaction(transaction1)
    
    # Create second asset (MSFT)
    asset2 = PortfolioAsset(ticker='MSFT', prices=prices, info=info, currency='USD')
    transaction2 = PortfolioAssetTransaction(
        date="2025-07-19",
        transaction_type="sell",
        quantity=5.0,
        price=300.00,
        currency="USD",
        total=1500.00,
        exchange_rate=1.00,
        subtotal_base=1500.00,
        fees_base=0.00,
        total_base=1500.00,
    )
    asset2.add_transaction(transaction2)
    
    assets = [asset1, asset2]

    expected_output = (
        "Date,Ticker,Type,Quantity,Price,Currency,Total,Exchange Rate,Subtotal Base,Fees Base,Total Base\n"
        "2025-07-18,AAPL,buy,10.00,150.00,USD,1500.00,1.00,1500.00,0.00,1500.00\n"
        "2025-07-19,MSFT,sell,5.00,300.00,USD,1500.00,1.00,1500.00,0.00,1500.00\n"
    )

    captured_output = io.StringIO()
    sys.stdout = captured_output

    print_asset_transactions_csv(assets)

    sys.stdout = sys.__stdout__

    assert captured_output.getvalue() == expected_output
