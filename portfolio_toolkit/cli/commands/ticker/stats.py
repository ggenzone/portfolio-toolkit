import click

from ..utils import not_implemented


@click.command()
@click.argument("symbol")
def stats(symbol):
    """Show statistical metrics (volatility, mean, etc.)"""
    not_implemented(f"ticker print stats {symbol}")
