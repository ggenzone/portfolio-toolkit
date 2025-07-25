import click
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.utils.log_returns import calculate_log_returns

@click.command()
@click.argument('symbol')
def returns(symbol):
    """Show daily/cumulative returns"""
    data_provider = YFDataProvider()
    prices = data_provider.get_price_series(symbol)
    daily_returns = calculate_log_returns(prices)
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    print(f"📈 Daily Returns for {symbol}:")
    print(daily_returns)
    print(f"📊 Cumulative Returns for {symbol}:")
    print(cumulative_returns)
