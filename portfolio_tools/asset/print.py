from typing import List

from .portfolio_asset import PortfolioAsset


def print_asset_transactions_csv(assets: List[PortfolioAsset]):
    """
    Prints all transactions in CSV format, ordered by date and not grouped by ticker.

    Args:
        assets (List[PortfolioAsset]): List of PortfolioAsset objects containing transactions.
    """
    # Collect all transactions from all assets
    all_transactions = []

    for asset in assets:
        ticker = asset.ticker
        for transaction in asset.transactions:
            # Create a transaction data tuple with ticker
            tx_data = {
                "date": transaction.date,
                "ticker": ticker,
                "type": transaction.transaction_type,
                "quantity": transaction.quantity,
                "price": transaction.price,
                "currency": transaction.currency,
                "total": transaction.total,
                "exchange_rate": transaction.exchange_rate,
                "subtotal_base": transaction.subtotal_base,
                "fees_base": transaction.fees_base,
                "total_base": transaction.total_base,
            }
            all_transactions.append(tx_data)

    # Sort by date
    all_transactions.sort(key=lambda x: x["date"])

    if not all_transactions:
        print("No transactions available.")
        return

    # Print CSV header
    print(
        "Date,Ticker,Type,Quantity,Price,Currency,Total,Exchange Rate,Subtotal Base,Fees Base,Total Base"
    )

    # Print each transaction
    for tx in all_transactions:
        print(
            f"{tx['date']},{tx['ticker']},"
            f"{tx['type']},{tx['quantity']:.2f},"
            f"{tx['price']:.2f},{tx['currency']},"
            f"{tx['total']:.2f},{tx['exchange_rate']:.2f},"
            f"{tx['subtotal_base']:.2f},{tx['fees_base']:.2f},"
            f"{tx['total_base']:.2f}"
        )
