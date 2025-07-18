from portfolio_tools.ticker.get_cash_ticker import get_cash_ticker

def test_get_cash_ticker():
    assert get_cash_ticker("USD") == "__USD"
    assert get_cash_ticker("EUR") == "__EUR"
    assert get_cash_ticker("JPY") == "__JPY"
    assert get_cash_ticker("GBP") == "__GBP"
