import pytest
from portfolio_toolkit.account import Account
from portfolio_toolkit.account import AccountTransaction
from datetime import date

def test_add_transaction_from_assets_dict_buy():
    acc = Account(name="Test Account", currency="USD")
    tx_dict = {"date": date(2024, 3, 1), "type": "buy", "ticker": "AAPL", "total_base": 150.0}
    acc.add_transaction_from_assets_dict(tx_dict)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].amount == -150.0
    assert acc.transactions[0].transaction_type == "sell"
    assert "Buy $AAPL asset" in acc.transactions[0].description

def test_add_transaction_from_assets_dict_sell():
    acc = Account(name="Test Account", currency="USD")
    tx_dict = {"date": date(2024, 3, 2), "type": "sell", "ticker": "AAPL", "total_base": 200.0}
    acc.add_transaction_from_assets_dict(tx_dict)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].amount == 200.0
    assert acc.transactions[0].transaction_type == "buy"
    assert "Sell $AAPL asset" in acc.transactions[0].description

def test_add_transaction_from_assets_dict_dividend():
    acc = Account(name="Test Account", currency="USD")
    tx_dict = {"date": date(2024, 3, 3), "type": "dividend", "ticker": "AAPL", "total_base": 10.0}
    acc.add_transaction_from_assets_dict(tx_dict)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].amount == 10.0
    assert acc.transactions[0].transaction_type == "income"
    assert "Dividend received for $AAPL asset" in acc.transactions[0].description

def test_add_transaction_from_assets_dict_invalid_type():
    acc = Account(name="Test Account", currency="USD")
    tx_dict = {"date": date(2024, 3, 4), "type": "invalid", "ticker": "AAPL", "total_base": 10.0}
    with pytest.raises(ValueError):
        acc.add_transaction_from_assets_dict(tx_dict)

def test_add_transaction_from_split_dict():
    acc = Account(name="Test Account", currency="USD")
    split_dict = {"date": date(2024, 4, 1), "ticker": "AAPL", "split_factor": 2.0}
    acc.add_transaction_from_split_dict(split_dict, amount=0.0)
    assert len(acc.transactions) == 1
    assert acc.transactions[0].transaction_type == "buy"
    assert "Stock split for AAPL with factor 2.0" in acc.transactions[0].description
    assert acc.transactions[0].amount == 0.0


def test_multiple_add_transaction_from_assets_dict_and_get_amount_at():
    acc = Account(name="Test Account", currency="USD")
    # 2024-01-10: buy 100 (should be -100, type sell)
    acc.add_transaction_from_assets_dict({"date": date(2024, 1, 10), "type": "buy", "ticker": "AAPL", "total_base": 100.0})
    # 2024-02-15: sell 50 (should be 50, type buy)
    acc.add_transaction_from_assets_dict({"date": date(2024, 2, 15), "type": "sell", "ticker": "AAPL", "total_base": 50.0})
    # 2024-03-01: dividend 10 (should be 10, type income)
    acc.add_transaction_from_assets_dict({"date": date(2024, 3, 1), "type": "dividend", "ticker": "AAPL", "total_base": 10.0})
    # 2024-03-20: buy 40 (should be -40, type sell)
    acc.add_transaction_from_assets_dict({"date": date(2024, 3, 20), "type": "buy", "ticker": "AAPL", "total_base": 40.0})

    # Check amounts at different dates
    assert acc.get_amount_at(date(2024, 1, 9)) == 0.0  # before any tx
    assert acc.get_amount_at(date(2024, 1, 10)) == -100.0  # after first buy
    assert acc.get_amount_at(date(2024, 2, 15)) == -50.0  # after sell
    assert acc.get_amount_at(date(2024, 3, 1)) == -40.0  # after dividend
    assert acc.get_amount_at(date(2024, 3, 19)) == -40.0  # before last buy
    assert acc.get_amount_at(date(2024, 3, 20)) == -80.0  # after last buy
