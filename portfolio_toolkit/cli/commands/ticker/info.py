import click

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider


@click.command()
@click.argument("symbol")
def info(symbol):
    """Show detailed ticker information.

    TICKER: Ticker symbol (e.g., AAPL, SHOP)
    """
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

        # Display key information
        key_fields = [
            ("longName", "🏢 Company Name"),
            ("sector", "🏭 Sector"),
            ("industry", "🔧 Industry"),
            ("country", "🌍 Country"),
            ("marketCap", "💹 Market Cap"),
            ("currentPrice", "💵 Current Price"),
            ("previousClose", "📉 Previous Close"),
            ("beta", "📊 Beta"),
            ("trailingPE", "📈 P/E Ratio"),
            ("dividendYield", "💰 Dividend Yield"),
            ("52WeekLow", "📉 52W Low"),
            ("52WeekHigh", "📈 52W High"),
        ]

        print()
        for field, label in key_fields:
            value = info.get(field, "N/A")
            if value != "N/A" and field == "marketCap":
                # Format market cap in billions/millions
                if value >= 1e9:
                    value = f"${value/1e9:.1f}B"
                elif value >= 1e6:
                    value = f"${value/1e6:.1f}M"
                else:
                    value = f"${value:,.0f}"
            elif value != "N/A" and field in [
                "currentPrice",
                "previousClose",
                "52WeekLow",
                "52WeekHigh",
            ]:
                value = f"{value:.2f} {currency}"
            elif value != "N/A" and field == "dividendYield":
                value = f"{value*100:.2f}%" if value else "N/A"
            elif value != "N/A" and field == "trailingPE":
                value = f"{value:.2f}" if value else "N/A"
            elif value != "N/A" and field == "beta":
                value = f"{value:.2f}" if value else "N/A"

            print(f"{label:<20}: {value}")

        print(f"\n✅ Information retrieved and cached for {ticker_symbol}")

    except Exception as e:
        print(f"❌ Error getting ticker information: {e}")
