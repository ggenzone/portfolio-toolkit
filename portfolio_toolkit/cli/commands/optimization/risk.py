import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.optimization import Optimization

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
def risk(file):
    """Show portfolio risk metrics"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = Optimization.from_dict(data, data_provider=data_provider)

    click.echo(
        f"📊 Portfolio risk metrics for: {portfolio.name} ({portfolio.currency})"
    )

    portfolio.get_var()

    click.echo("=" * 60)
