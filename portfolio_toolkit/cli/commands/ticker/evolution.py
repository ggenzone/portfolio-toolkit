import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.plot.plot_assets import plot_assets


@click.command()
@click.argument("symbols", nargs=-1, required=True)
@click.option(
    "-c",
    "--currency",
    "currency",
    default="USD",
    help="Target currency for price conversion (default: USD)",
)
def evolution(symbols, currency):
    """Plot the price evolution of a list of assets."""
    if len(symbols) < 2:
        click.echo("Error: At least 2 symbols are required")
        return

    """Calculate correlation between asset pairs."""
    data_provider = YFDataProvider()
    ticker_list = [t.strip() for t in symbols if t.strip()]
    target_currency = currency.upper()
    series = [
        data_provider.get_price_series_converted(ticker, target_currency)
        for ticker in ticker_list
    ]
    plot_assets(series, ticker_list)
