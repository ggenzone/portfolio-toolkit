import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.utils.correlation import calculate_correlation
from portfolio_toolkit.utils.log_returns import calculate_log_returns


@click.command()
@click.argument("symbols", nargs=-1, required=True)
def correlation(symbols):
    """Compare multiple tickers"""
    if len(symbols) < 2:
        click.echo("Error: At least 2 symbols are required")
        return

    """Calculate correlation between asset pairs."""
    data_provider = YFDataProvider()
    ticker_list = [t.strip() for t in symbols if t.strip()]
    prices = {ticker: data_provider.get_price_series(ticker) for ticker in ticker_list}
    returns = {ticker: calculate_log_returns(prices[ticker]) for ticker in ticker_list}
    print("|" + "-" * 37 + "|")
    print(f"{'| Ticker 1':<12}| {'Ticker 2':<10}| {'Correlation':<12}|")
    print("|" + "-" * 11 + "|" + "-" * 11 + "|" + "-" * 13 + "|")
    for i in range(len(ticker_list)):
        for j in range(i + 1, len(ticker_list)):
            corr = calculate_correlation(
                returns[ticker_list[i]], returns[ticker_list[j]]
            )
            print(f"| {ticker_list[i]:<10}| {ticker_list[j]:<10}| {corr:<12.4f}|")
    print("|" + "-" * 37 + "|")
