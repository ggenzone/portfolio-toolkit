import json
from datetime import datetime
from typing import Dict, List, Tuple

from portfolio_tools.account.account import Account
from portfolio_tools.asset.create import create_market_asset
from portfolio_tools.asset.portfolio_asset import PortfolioAsset
from portfolio_tools.data_provider.data_provider import DataProvider
from portfolio_tools.transaction.get_ticker import get_transaction_ticker
from portfolio_tools.transaction.validate import validate_transaction


def load_json(
    json_filepath: str, data_provider: DataProvider
) -> Tuple[Dict[str, str], List[PortfolioAsset], Account, datetime]:
    """
    Loads and validates a JSON file containing portfolio information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.
        data_provider (DataProvider): Data provider instance for fetching ticker information.

    Returns:
        Tuple[Dict[str, str], List[PortfolioAsset], Account, datetime]:
            - Portfolio information with name and currency.
            - List of real assets (non-cash).
            - Cash account with all cash transactions.
            - Calculated portfolio start date.
    """
    with open(json_filepath, mode="r", encoding="utf-8") as file:
        data = json.load(file)

        # Validate portfolio structure
        if "name" not in data or "currency" not in data or "transactions" not in data:
            raise ValueError("The JSON does not have the expected portfolio format.")

        portfolio_currency = data["currency"]

        assets, account, start_date = process_transactions(
            data["transactions"], portfolio_currency, data_provider
        )

        portfolio = {
            "name": data["name"],
            "currency": data["currency"],
        }

        return portfolio, assets, account, start_date


def process_transactions(
    transactions: dict, portfolio_currency: str, data_provider: DataProvider
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
                assets_dict[ticker] = create_market_asset(
                    data_provider, ticker, portfolio_currency
                )
            assets_dict[ticker].add_transaction_from_dict(transaction)

            # Create synthetic cash transaction for asset purchases/sales
            if transaction["type"] in ["buy", "sell"]:
                cash_account.add_transaction_from_assets_dict(transaction)

    start_date = min(transaction_dates) if transaction_dates else None

    # Convert assets dictionary to list
    assets = list(assets_dict.values())

    return assets, cash_account, start_date
