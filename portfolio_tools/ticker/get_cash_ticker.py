def get_cash_ticker(portfolio_currency):
    """
    Returns the synthetic ticker for cash based on the portfolio currency.

    Args:
        portfolio_currency (str): The currency of the portfolio.

    Returns:
        str: The synthetic cash ticker (e.g., "__USD").
    """
    return f"__{portfolio_currency}"
