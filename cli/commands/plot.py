import click
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.plot.plot_assets import plot_assets


@click.command()
@click.argument('tickers')
@click.argument('currency')
def plot(tickers, currency):
    """Plot the price evolution of a list of assets.
    
    TICKERS: Comma-separated list of tickers (e.g. AAPL,MSFT,GOOGL)
    CURRENCY: Target currency (e.g., EUR, USD, CAD)
    """
    data_provider = YFDataProvider()
    ticker_list = [t.strip() for t in tickers.split(',') if t.strip()]
    target_currency = currency.upper()
    series = [data_provider.get_price_series_converted(ticker, target_currency) for ticker in ticker_list]
    plot_assets(series, ticker_list)
