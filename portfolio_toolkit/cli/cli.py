import click

from .. import __version__
from .commands.clear_cache import clear_cache
from .commands.optimization.optimization import optimization
from .commands.portfolio.portfolio import portfolio

# New organized command groups
from .commands.ticker.ticker import ticker


@click.group()
@click.version_option(version=__version__, package_name="portfolio-toolkit")
def cli():
    """Portfolio Toolkit CLI - Manage and analyze your investment portfolios."""
    pass


cli.add_command(clear_cache)

# New organized command groups
cli.add_command(ticker)
cli.add_command(optimization)
cli.add_command(portfolio)


def main():
    cli()


if __name__ == "__main__":
    main()
