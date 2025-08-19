import click

from portfolio_toolkit.account.account import Account
from portfolio_toolkit.asset import PortfolioAsset
from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.portfolio import Portfolio

from ..utils import load_json_file


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Save results to CSV file instead of printing to console",
)
@click.option("--cash", is_flag=True, default=False, help="Cash transactions")
@click.option("--income", is_flag=True, default=False, help="Income transactions")
def transactions(file, output, cash, income):
    """Show portfolio transactions"""
    data = load_json_file(file)
    data_provider = YFDataProvider()
    portfolio = Portfolio.from_dict(data, data_provider=data_provider)

    if cash:
        cash_transactions(portfolio, output, income)
    else:
        asset_transactions(portfolio, output)


def cash_transactions(portfolio, output, income):
    """Show cash transactions"""
    click.echo(
        f"📊 Portfolio transactions for: {portfolio.name} ({portfolio.currency})"
    )
    transactions_df = Account.to_dataframe(portfolio.account)
    # Save to CSV file or display in console
    if output:
        transactions_df.to_csv(output, index=False)
        click.echo(f"✅ Results saved to: {output}")
    else:

        click.echo("\n📊 Account transactions")
        click.echo("=" * 60)
        click.echo(transactions_df.to_string())


def asset_transactions(portfolio, output):
    """Show asset transactions"""
    click.echo("\n📊 Portfolio asset transactions")
    click.echo("=" * 60)
    assets_df = PortfolioAsset.to_dataframe(portfolio.assets)

    # Save to CSV file or display in console
    if output:
        assets_df.to_csv(output, index=False)
        click.echo(f"✅ Results saved to: {output}")
    else:
        click.echo(assets_df.to_string())
        click.echo("=" * 60)
