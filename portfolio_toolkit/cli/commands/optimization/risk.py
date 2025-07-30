import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.optimization.compute_var import compute_var
from portfolio_toolkit.optimization.parser import create_optimization_from_json

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def risk(file):
    """Show portfolio risk metrics"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = create_optimization_from_json(data, data_provider=data_provider)

    click.echo(
        f"📊 Portfolio risk metrics for: {portfolio.name} ({portfolio.currency})"
    )

    compute_var(portfolio)

    click.echo("=" * 60)
