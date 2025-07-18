def print_asset_transactions_csv(assets):
    """
    Prints all transactions in CSV format, ordered by date and not grouped by ticker.

    Args:
        assets (list): List of asset dictionaries containing transactions.
    """
    # Collect all transactions from all assets
    all_transactions = []

    for asset in assets:
        ticker = asset["ticker"]
        for transaction in asset["transactions"]:
            # Create a copy of the transaction and add the ticker
            tx = transaction.copy()
            tx["ticker"] = ticker
            all_transactions.append(tx)

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
            f"{tx.get('date', '')},{tx.get('ticker', '')},"
            f"{tx.get('type', '')},{tx.get('quantity', 0):.2f},"
            f"{tx.get('price', 0):.2f},{tx.get('currency', '')},"
            f"{tx.get('total', 0):.2f},{tx.get('exchange_rate', 0):.2f},"
            f"{tx.get('subtotal_base', 0):.2f},{tx.get('fees_base', 0):.2f},"
            f"{tx.get('total_base', 0):.2f}"
        )
