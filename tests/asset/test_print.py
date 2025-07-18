import io
import sys
from portfolio_tools.asset.print import print_asset_transactions_csv

def test_print_asset_transactions_csv():
    assets = [
        {
            "ticker": "AAPL",
            "transactions": [
                {
                    "date": "2025-07-18",
                    "type": "buy",
                    "quantity": 10,
                    "price": 150.00,
                    "currency": "USD",
                    "total": 1500.00,
                    "exchange_rate": 1.00,
                    "subtotal_base": 1500.00,
                    "fees_base": 0.00,
                    "total_base": 1500.00,
                }
            ],
        },
        {
            "ticker": "MSFT",
            "transactions": [
                {
                    "date": "2025-07-19",
                    "type": "sell",
                    "quantity": 5,
                    "price": 300.00,
                    "currency": "USD",
                    "total": 1500.00,
                    "exchange_rate": 1.00,
                    "subtotal_base": 1500.00,
                    "fees_base": 0.00,
                    "total_base": 1500.00,
                }
            ],
        },
    ]

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
