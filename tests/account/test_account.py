import pytest
from portfolio_toolkit.account import Account
from portfolio_toolkit.account import AccountTransaction
from datetime import date


def test_add_transaction():
    acc = Account(name="Test Account", currency="USD")
    tx = AccountTransaction(transaction_date=date(2024, 1, 1), transaction_type="buy", amount=100.0, description="Test buy")
    acc.add_transaction(tx)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].amount == 100.0


def test_add_transaction_from_dict():
    acc = Account(name="Test Account", currency="USD")
    tx_dict = {"date": date(2024, 1, 2), "type": "buy", "total_base": 200.0, "description": "Buy asset"}
    acc.add_transaction_from_dict(tx_dict)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].amount == 200.0
    assert acc.transactions[0].transaction_type == "buy"


def test_get_amount():
    acc = Account(name="Test Account", currency="USD")
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 1, 1), transaction_type="buy", amount=100.0))
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 1, 2), transaction_type="sell", amount=-50.0))
    assert acc.get_amount() == 50.0


def test_get_amount_at():
    acc = Account(name="Test Account", currency="USD")
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 1, 1), transaction_type="buy", amount=100.0))
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 2, 1), transaction_type="sell", amount=-30.0))
    assert acc.get_amount_at(date(2024, 1, 15)) == 100.0
    assert acc.get_amount_at(date(2024, 2, 2)) == 70.0


def test_sort_transactions():
    acc = Account(name="Test Account", currency="USD")
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 2, 1), transaction_type="buy", amount=100.0))
    acc.add_transaction(AccountTransaction(transaction_date=date(2024, 1, 1), transaction_type="buy", amount=50.0))
    acc.sort_transactions()
    assert acc.transactions[0].transaction_date == date(2024, 1, 1)
    assert acc.transactions[1].transaction_date == date(2024, 2, 1)
