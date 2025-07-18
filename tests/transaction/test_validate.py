import pytest
from portfolio_tools.transaction.validate import validate_transaction

def test_validate_transaction_valid():
    transaction = {
        "date": "2025-07-18",
        "type": "buy",
        "quantity": 10,
    }
    # Should not raise an exception
    validate_transaction(transaction)

def test_validate_transaction_missing_date():
    transaction = {
        "type": "buy",
        "quantity": 10,
    }
    with pytest.raises(ValueError, match="Missing field: date"):
        validate_transaction(transaction)

def test_validate_transaction_missing_type():
    transaction = {
        "date": "2025-07-18",
        "quantity": 10,
    }
    with pytest.raises(ValueError, match="Missing field: type"):
        validate_transaction(transaction)

def test_validate_transaction_missing_quantity():
    transaction = {
        "date": "2025-07-18",
        "type": "buy",
    }
    with pytest.raises(ValueError, match="Missing field: quantity"):
        validate_transaction(transaction)
