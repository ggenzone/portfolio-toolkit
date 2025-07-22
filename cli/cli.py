import click
from cli.commands.clear_cache import clear_cache

# New organized command groups
from cli.commands.ticker.ticker import ticker
from cli.commands.watchlist.watchlist import watchlist
from cli.commands.optimization.optimization import optimization
from cli.commands.portfolio.portfolio import portfolio


@click.group()
@click.version_option(version='0.1.0', package_name='portfolio-tools')
def cli():
    """Portfolio Tools CLI - Manage and analyze your investment portfolios."""
    pass


cli.add_command(clear_cache)

# New organized command groups
cli.add_command(ticker)
cli.add_command(watchlist)
cli.add_command(optimization)
cli.add_command(portfolio)


def main():
    cli()


if __name__ == "__main__":
    main()
