from datetime import datetime
from typing import List, Tuple

from portfolio_toolkit.account.account import Account
from portfolio_toolkit.asset import PortfolioAsset
from portfolio_toolkit.data_provider.data_provider import DataProvider

from .portfolio import Portfolio


def portfolio_from_dict(data: dict, data_provider: DataProvider) -> Portfolio:
    """
    Loads and validates a JSON file containing portfolio information.

    Args:
        data (dict): The portfolio data as a dictionary.
        data_provider (DataProvider): Data provider instance for fetching ticker information.

    Returns:
        Portfolio: The loaded portfolio object.
    """

    # Validate portfolio structure
    if "name" not in data or "currency" not in data or "transactions" not in data:
        raise ValueError("The JSON does not have the expected portfolio format.")

    portfolio_currency = data["currency"]

    splits = data.get("splits", [])

    assets, account, start_date = process_transactions(
        data["transactions"], splits, portfolio_currency, data_provider
    )

    portfolio = {
        "name": data["name"],
        "currency": data["currency"],
    }

    return Portfolio(
        name=portfolio["name"],
        currency=portfolio["currency"],
        assets=assets,
        account=account,
        start_date=start_date,
        data_provider=data_provider,
    )


def process_transactions(
    transactions: dict,
    splits: dict,
    portfolio_currency: str,
    data_provider: DataProvider,
) -> Tuple[List[PortfolioAsset], Account, datetime]:
    """
    Processes transactions to create asset objects and validate them.

    Args:
        transactions (list): List of transaction dictionaries.
        portfolio_currency (str): The currency of the portfolio.
        data_provider: Optional data provider for fetching ticker information.

    Returns:
        list: List of real assets (non-cash).
        dict: Cash account with all cash transactions.
        datetime: Calculated portfolio start date.
    """
    assets_dict = {}
    transaction_dates = []

    cash_account = Account(name="Cash Account", currency=portfolio_currency)

    # Process all transactions
    for transaction in transactions:
        validate_transaction(transaction)

        transaction_dates.append(datetime.strptime(transaction["date"], "%Y-%m-%d"))

        ticker = get_transaction_ticker(transaction, portfolio_currency)

        # Determine if it's a cash transaction or real asset
        if ticker.startswith("__"):
            cash_account.add_transaction_from_dict(transaction)
        else:
            # Real asset
            if ticker not in assets_dict:
                assets_dict[ticker] = PortfolioAsset.from_ticker(
                    data_provider, ticker, portfolio_currency
                )
            assets_dict[ticker].add_transaction_from_dict(transaction)

            # Create synthetic cash transaction for asset purchases/sales
            if transaction["type"] in ["buy", "sell", "dividend"]:
                cash_account.add_transaction_from_assets_dict(transaction)

    # Process splits
    for split in splits:
        ticker = split["ticker"]
        if ticker in assets_dict:
            remaining_amount = assets_dict[ticker].add_split(split)
            if remaining_amount > 0.01:
                cash_account.add_transaction_from_split_dict(split, remaining_amount)

    start_date = min(transaction_dates) if transaction_dates else None

    # Convert assets dictionary to list
    assets = list(assets_dict.values())

    return assets, cash_account, start_date


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


def validate_transaction(transaction):
    """
    Validates that a transaction contains the required fields: date, type, and quantity.

    Args:
        transaction (dict): The transaction to validate.

    Raises:
        ValueError: If the transaction does not contain the required fields.
    """
    required_fields = ["date", "type", "quantity"]
    for field in required_fields:
        if field not in transaction:
            raise ValueError(
                f"A transaction does not have the expected format. Missing field: {field}"
            )
