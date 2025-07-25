import click

from ..utils import not_implemented


@click.command()
@click.argument("symbol")
def volatility(symbol):
    """Plot volatility over time"""
    not_implemented(f"ticker plot volatility {symbol}")
