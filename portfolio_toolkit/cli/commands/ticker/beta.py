import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider


@click.command()
@click.argument("symbol")
def beta(symbol):
    """Show beta relative to benchmark"""
    try:
        data_provider = YFDataProvider()
        ticker_symbol = symbol.upper()

        print(f"📊 Ticker Information: {ticker_symbol}")
        print("=" * 50)

        # Get currency
        currency = data_provider.get_ticker_currency(ticker_symbol)
        print(f"💰 Currency: {currency}")

        # Get detailed info
        info = data_provider.get_ticker_info(ticker_symbol)
        print(f"📊  Beta: {info['beta']}")

        print(f"\n✅ Information retrieved and cached for {ticker_symbol}")

    except Exception as e:
        print(f"❌ Error getting ticker information: {e}")
