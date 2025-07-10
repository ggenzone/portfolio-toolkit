import json
from datetime import datetime

def load_json(json_filepath):
    """
    Loads and validates a JSON file containing portfolio information.

    Args:
        json_filepath (str): Path to the JSON file to load data from.

    Returns:
        list: List of assets with their validated transactions.
        datetime: Calculated portfolio start date.
    """
    with open(json_filepath, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        transaction_dates = []
        assets = []

        for asset in data:
            if "ticker" not in asset or "transactions" not in asset:
                raise ValueError("The JSON does not have the expected format.")

            assets.append({
                "ticker": asset["ticker"],
                "transactions": asset["transactions"],
                "sector": asset.get("sector", "Unknown"),
                "country": asset.get("country", "Unknown")
            })

            for transaction in asset["transactions"]:
                if "date" not in transaction or "type" not in transaction or "quantity" not in transaction:
                    raise ValueError("A transaction does not have the expected format.")

                transaction_dates.append(datetime.strptime(transaction["date"], "%Y-%m-%d"))

        start_date = min(transaction_dates) if transaction_dates else None

        return assets, start_date
