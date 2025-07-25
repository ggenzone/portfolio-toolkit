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
