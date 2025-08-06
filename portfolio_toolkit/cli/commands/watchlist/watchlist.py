import click

from .performance import performance


@click.group()
def watchlist():
    """Portfolio analysis commands"""
    pass


watchlist.add_command(performance)
