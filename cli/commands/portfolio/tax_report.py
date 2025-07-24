import click
from portfolio_tools.portfolio.load_portfolio_json import load_portfolio_json
from portfolio_tools.position.get_open_positions import get_open_positions
from portfolio_tools.position.print_closed_positions import print_closed_positions, print_closed_positions_summary
from portfolio_tools.position.get_closed_positions import get_closed_positions
from portfolio_tools.portfolio.print_cash_incomes import print_cash_incomes
from portfolio_tools.position.get_valuation import get_valuation
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.position.print_open_positions import print_open_positions
from tests import portfolio
from ..utils import load_json_file


@click.command('tax-report')
@click.argument('file', type=click.Path(exists=True))
@click.argument('year', required=True)
def tax_report(file, year):
    """Generate tax report (gains/losses)"""
    data = load_json_file(file)

    previous_year = int(year) - 1
    previous_last_day = f"{previous_year}-12-31"

    first_day = f"{year}-01-01"
    last_day = f"{year}-12-31"
    click.echo(f"Generating tax report for the year {year} from {first_day} to {last_day}")

    data_provider = YFDataProvider()
    portfolio = load_portfolio_json(json_filepath=file, data_provider=data_provider)
    closed_positions = get_closed_positions(portfolio.assets, from_date=first_day, to_date=last_day)

    print_closed_positions(closed_positions, last_day)
    print_closed_positions_summary(closed_positions, last_day)

    last_open_positions = get_open_positions(portfolio.assets, previous_last_day)
    open_positions = get_open_positions(portfolio.assets, last_day)


    # Print initial and final valuation
    print("-" * 50)
    initial_valuation = get_valuation(last_open_positions)
    click.echo(f"Initial Valuation: {initial_valuation:.2f}")
    final_valuation = get_valuation(open_positions)
    click.echo(f"Final Valuation: {final_valuation:.2f}")

    # Print open positions at the end of the report
    print("-" * 50)
    print_open_positions(open_positions)
    print("-" * 50)

    print_cash_incomes(portfolio, from_date=first_day, to_date=last_day)


