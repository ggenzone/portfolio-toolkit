def create_synthetic_cash_transaction(transaction, portfolio_currency):
    """
    Creates a synthetic cash transaction based on a buy or sell transaction.

    Args:
        transaction (dict): The original transaction.
        portfolio_currency (str): The currency of the portfolio.

    Returns:
        dict: A synthetic cash transaction.
    """
    return {
        "date": transaction["date"],
        "type": transaction["type"],
        "quantity": transaction.get("total_base", 0),
        "price": 1.00,
        "currency": portfolio_currency,
        "total": 0,
        "exchange_rate": 1,
        "subtotal_base": transaction.get("total_base", 0),
        "fees_base": 0,
        "total_base": transaction.get("total_base", 0),
    }
