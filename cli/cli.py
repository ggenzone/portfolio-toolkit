import click
from cli.commands.composition import composition
from cli.commands.correlation import correlation
from cli.commands.plot import plot
from cli.commands.plot_portfolio import plot_portfolio
from cli.commands.print_positions import print_positions
from cli.commands.export_transactions import export_transactions
from cli.commands.dump_data_frame import dump_data_frame
from cli.commands.clear_cache import clear_cache
from cli.commands.ticker_info import ticker_info
from cli.commands.convert_currency import convert_currency


@click.group()
@click.version_option(version='0.1.0', package_name='portfolio-tools')
def cli():
    """Portfolio Tools CLI - Manage and analyze your investment portfolios."""
    pass


# Add all commands to the main CLI group
cli.add_command(composition)
cli.add_command(correlation)
cli.add_command(plot)
cli.add_command(plot_portfolio)
cli.add_command(print_positions)
cli.add_command(export_transactions)
cli.add_command(dump_data_frame)
cli.add_command(clear_cache)
cli.add_command(ticker_info)
cli.add_command(convert_currency)


def main():
    cli()


if __name__ == "__main__":
    main()
