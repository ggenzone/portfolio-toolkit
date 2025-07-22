import click
from portfolio_tools.portfolio.portfolio import Portfolio
from portfolio_tools.position.print_closed_positions import print_closed_positions, print_closed_positions_to_csv, print_closed_positions_summary
from portfolio_tools.position.get_closed_positions import get_closed_positions
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from ..utils import load_json_file


@click.command('tax-report')
@click.argument('file', type=click.Path(exists=True))
@click.argument('year', required=True)
def tax_report(file, year):
    """Generate tax report (gains/losses)"""
    data = load_json_file(file)

    first_day = f"{year}-01-01"
    last_day = f"{year}-12-31"
    click.echo(f"Generating tax report for the year {year} from {first_day} to {last_day}")

    data_provider = YFDataProvider()
    portfolio = Portfolio(json_filepath=file, data_provider=data_provider)
    closed_positions = get_closed_positions(portfolio.assets, from_date=first_day, to_date=last_day)

    print_closed_positions(closed_positions, last_day)
    print_closed_positions_summary(closed_positions, last_day)

