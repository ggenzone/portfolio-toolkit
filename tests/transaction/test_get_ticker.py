from portfolio_tools.transaction.get_ticker import get_transaction_ticker

def test_get_transaction_ticker_with_ticker():
    transaction = {"ticker": "AAPL"}
    assert get_transaction_ticker(transaction, "USD") == "AAPL"

def test_get_transaction_ticker_without_ticker():
    transaction = {"ticker": None}
    assert get_transaction_ticker(transaction, "USD") == "__USD"

def test_get_transaction_ticker_with_different_currency():
    transaction = {"ticker": None}
    assert get_transaction_ticker(transaction, "EUR") == "__EUR"
