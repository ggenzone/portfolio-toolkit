import click
import pandas as pd
from portfolio_tools.data_provider.yf_data_provider import YFDataProvider


@click.command(name='convert-currency')
@click.argument('ticker')
@click.argument('currency')
@click.option('--days', default=5, type=int, 
              help='Number of recent days to show (default: 5)')
def convert_currency(ticker, currency, days):
    """Convert ticker prices to different currency.
    
    TICKER: Ticker symbol (e.g., AAPL, SHOP)
    CURRENCY: Target currency (e.g., EUR, USD, CAD)
    """
    try:
        data_provider = YFDataProvider()
        ticker_symbol = ticker.upper()
        target_currency = currency.upper()
        
        print(f"💱 Converting {ticker_symbol} prices to {target_currency}")
        print("=" * 50)
        
        # Get original currency
        original_currency = data_provider.get_ticker_currency(ticker_symbol)
        print(f"📊 Original currency: {original_currency}")
        
        if original_currency == target_currency:
            print(f"ℹ️  Ticker {ticker_symbol} is already in {target_currency}")
            return
        
        # Get converted prices
        converted_prices = data_provider.get_price_series_converted(ticker_symbol, target_currency, 'Close')
        original_prices = data_provider.get_price_series(ticker_symbol, 'Close')
        
        # Show recent data
        recent_data = pd.DataFrame({
            f'Original ({original_currency})': original_prices.tail(days),
            f'Converted ({target_currency})': converted_prices.tail(days)
        })
        
        print(f"\n📈 Recent {days} days of price data:")
        print(recent_data.round(2))
        
        # Show summary statistics
        print(f"\n📊 Summary Statistics:")
        print(f"Latest price ({original_currency}): {original_prices.iloc[-1]:.2f}")
        print(f"Latest price ({target_currency}): {converted_prices.iloc[-1]:.2f}")
        
        # Calculate percentage change
        if len(converted_prices) > 1:
            pct_change = ((converted_prices.iloc[-1] - converted_prices.iloc[-2]) / converted_prices.iloc[-2]) * 100
            print(f"Daily change: {pct_change:+.2f}%")
        
        print(f"\n✅ Successfully converted {ticker_symbol} from {original_currency} to {target_currency}")
        
    except Exception as e:
        print(f"❌ Error converting currency: {e}")
        print(e.with_traceback())