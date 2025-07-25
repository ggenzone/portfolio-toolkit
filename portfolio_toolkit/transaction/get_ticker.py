def get_transaction_ticker(transaction, portfolio_currency):
    """
    Returns the ticker for a transaction. If the transaction does not have a ticker,
    it returns the synthetic cash ticker based on the portfolio currency.

    Args:
        transaction (dict): The transaction to process.
        portfolio_currency (str): The currency of the portfolio.

    Returns:
        str: The ticker for the transaction.
    """
    if transaction["ticker"] is None:
        return f"__{portfolio_currency}"
    return transaction["ticker"]
