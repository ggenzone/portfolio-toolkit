import json
from datetime import datetime


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
            if (
                "date" not in transaction
                or "type" not in transaction
                or "quantity" not in transaction
            ):
                raise ValueError("A transaction does not have the expected format.")

            transaction_dates.append(datetime.strptime(transaction["date"], "%Y-%m-%d"))

            # Determine ticker (use synthetic ticker for cash transactions)
            if transaction["ticker"] is None:
                ticker = f"__{portfolio_currency}"  # e.g., "__EUR"
            else:
                ticker = transaction["ticker"]

            # Group all transactions by ticker (including cash)
            if ticker not in assets:
                assets[ticker] = {
                    "ticker": ticker,
                    "transactions": [],
                    "sector": "Cash" if ticker.startswith("__") else "Unknown",
                    "country": "Unknown",
                }
            assets[ticker]["transactions"].append(transaction)

            # Create synthetic cash transactions for asset purchases/sales
            if transaction["ticker"] is not None:  # Only for real assets, not cash
                cash_ticker = f"__{portfolio_currency}"

                # Ensure cash asset exists
                if cash_ticker not in assets:
                    assets[cash_ticker] = {
                        "ticker": cash_ticker,
                        "transactions": [],
                        "sector": "Cash",
                        "country": "Unknown",
                    }

                # Create synthetic cash transaction
                if transaction["type"] == "buy":
                    # When buying assets, cash decreases (sell cash)
                    cash_transaction = {
                        "date": transaction["date"],
                        "type": "sell",
                        "quantity": transaction.get(
                            "total_base", transaction.get("total", 0)
                        ),
                        "price": 1.00,
                        "currency": transaction.get("currency", portfolio_currency),
                        "total": transaction.get("total", 0),
                        "exchange_rate": transaction.get("exchange_rate", 0),
                        "subtotal_base": transaction.get("subtotal_base", 0),
                        "fees_base": transaction.get(
                            "fees_base", 0
                        ),  # Fees already deducted
                        "total_base": transaction.get("total_base", 0),
                    }
                elif transaction["type"] == "sell":
                    # When selling assets, cash increases (buy cash)
                    net_proceeds = transaction.get(
                        "total_base", transaction.get("total", 0)
                    ) - transaction.get("fees_base", 0)
                    cash_transaction = {
                        "date": transaction["date"],
                        "type": "buy",
                        "quantity": net_proceeds,
                        "price": 1.00,
                        "currency": transaction.get("currency", portfolio_currency),
                        "total": transaction.get("total", 0),
                        "exchange_rate": transaction.get("exchange_rate", 0),
                        "subtotal_base": transaction.get("subtotal_base", 0),
                        "fees_base": transaction.get(
                            "fees_base", 0
                        ),  # Fees already deducted
                        "total_base": transaction.get("total_base", 0),
                    }

                if transaction["type"] in ["buy", "sell"]:
                    assets[cash_ticker]["transactions"].append(cash_transaction)

        start_date = min(transaction_dates) if transaction_dates else None

        portfolio = {
            "name": data["name"],
            "currency": data["currency"],
            "assets": list(assets.values()),
        }

        return portfolio, start_date
