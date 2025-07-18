from portfolio_tools.transaction.create_synthetic_cash import create_synthetic_cash_transaction

def test_create_synthetic_cash_transaction_buy():
    transaction = {
        "date": "2025-07-18",
        "type": "buy",
        "total_base": 1000,
    }
    portfolio_currency = "USD"
    expected = {
        "date": "2025-07-18",
        "type": "buy",
        "quantity": 1000,
        "price": 1.00,
        "currency": "USD",
        "total": 0,
        "exchange_rate": 1,
        "subtotal_base": 1000,
        "fees_base": 0,
        "total_base": 1000,
    }
    assert create_synthetic_cash_transaction(transaction, portfolio_currency) == expected

def test_create_synthetic_cash_transaction_sell():
    transaction = {
        "date": "2025-07-18",
        "type": "sell",
        "total_base": 500,
    }
    portfolio_currency = "EUR"
    expected = {
        "date": "2025-07-18",
        "type": "sell",
        "quantity": 500,
        "price": 1.00,
        "currency": "EUR",
        "total": 0,
        "exchange_rate": 1,
        "subtotal_base": 500,
        "fees_base": 0,
        "total_base": 500,
    }
    assert create_synthetic_cash_transaction(transaction, portfolio_currency) == expected
