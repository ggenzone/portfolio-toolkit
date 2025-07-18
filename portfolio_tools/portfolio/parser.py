import json
from datetime import datetime

from portfolio_tools.asset.create import create_asset
from portfolio_tools.ticker.get_cash_ticker import get_cash_ticker
from portfolio_tools.transaction.create_synthetic_cash import (
    create_synthetic_cash_transaction,
)
from portfolio_tools.transaction.get_ticker import get_transaction_ticker
from portfolio_tools.transaction.validate import validate_transaction


def load_json(json_filepath):
    """
    Loads and validates a JSON file containing portfolio information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.

    Returns:
        dict: Portfolio information with name, currency, and assets (including cash).
        datetime: Calculated portfolio start date.
    """
    with open(json_filepath, mode="r", encoding="utf-8") as file:
        data = json.load(file)

        # Validate portfolio structure
        if "name" not in data or "currency" not in data or "transactions" not in data:
            raise ValueError("The JSON does not have the expected portfolio format.")

        transaction_dates = []
        assets = {}
        portfolio_currency = data["currency"]

        # Process all transactions
        for transaction in data["transactions"]:
            validate_transaction(transaction)

            transaction_dates.append(datetime.strptime(transaction["date"], "%Y-%m-%d"))

            ticker = get_transaction_ticker(transaction, portfolio_currency)

            # Group all transactions by ticker (including cash)
            if ticker not in assets:
                assets[ticker] = create_asset(ticker)

            assets[ticker]["transactions"].append(transaction)

            # Create synthetic cash transactions for asset purchases/sales
            if transaction["ticker"] is not None:  # Only for real assets, not cash
                cash_ticker = get_cash_ticker(portfolio_currency)

                # Ensure cash asset exists
                if cash_ticker not in assets:
                    assets[cash_ticker] = create_asset(cash_ticker)

                # Create synthetic cash transaction
                cash_transaction = create_synthetic_cash_transaction(
                    transaction, portfolio_currency
                )

                if transaction["type"] in ["buy", "sell"]:
                    assets[cash_ticker]["transactions"].append(cash_transaction)

        start_date = min(transaction_dates) if transaction_dates else None

        portfolio = {
            "name": data["name"],
            "currency": data["currency"],
            "assets": list(assets.values()),
        }

        return portfolio, start_date
