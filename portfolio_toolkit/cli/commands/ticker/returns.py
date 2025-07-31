import click
import pandas as pd

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.utils.log_returns import calculate_log_returns


@click.command()
@click.argument("symbols")
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Save results to CSV file instead of printing to console",
)
@click.option(
    "--period",
    type=str,
    default="1y",
    help="Time period for data retrieval (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
)
def returns(symbols, output, period):
    """Show daily returns for multiple symbols

    SYMBOLS: Comma-separated list of ticker symbols (e.g., AAPL,MSFT,GOOGL)
    """
    # Parse symbols from comma-separated string
    symbol_list = [symbol.strip().upper() for symbol in symbols.split(",")]

    data_provider = YFDataProvider()
    returns_data = {}

    click.echo(
        f"📈 Calculating daily returns for: {', '.join(symbol_list)} (Period: {period})"
    )

    # Calculate returns for each symbol
    for symbol in symbol_list:
        try:
            prices = data_provider.get_price_series(
                symbol, columna="Close", period=period
            )
            daily_returns = calculate_log_returns(prices)
            returns_data[symbol] = daily_returns
            click.echo(f"✅ Processed {symbol}")
        except Exception as e:
            click.echo(f"❌ Error processing {symbol}: {e}")
            continue

    if not returns_data:
        click.echo("❌ No data could be retrieved for any symbols")
        return

    # Create DataFrame with dates as rows and tickers as columns
    returns_df = pd.DataFrame(returns_data)

    # Sort by date index
    returns_df = returns_df.sort_index()

    # Calculate and display mean returns for each ticker
    click.echo("\n📊 Returns Summary:")
    click.echo("=" * 80)
    click.echo(
        f"{'Ticker':>6} | {'Daily Mean':>10} | {'Daily Std':>10} | {'Monthly':>10} | {'Annual':>10}"
    )
    click.echo("-" * 80)

    for symbol in returns_df.columns:
        # Drop NaN values (first value is typically NaN) and zeros if any
        clean_returns = returns_df[symbol].dropna()
        if len(clean_returns) > 0:
            # Daily statistics (log returns)
            daily_mean = clean_returns.mean()
            daily_std = clean_returns.std()

            # Convert log returns to simple returns for annualization
            # For log returns: simple_return ≈ exp(log_return) - 1 for small values
            # Or more precisely: simple_return = exp(log_return) - 1
            simple_daily_mean = (clean_returns.apply(lambda x: x + 1).mean()) - 1

            # Annualize using trading days (approximately 21 trading days per month, 252 per year)
            monthly_return = (1 + simple_daily_mean) ** 21 - 1
            annual_return = (1 + simple_daily_mean) ** 252 - 1

            click.echo(
                f"{symbol:>6} | {daily_mean:>10.4f} | {daily_std:>10.4f} | {monthly_return:>9.2%} | {annual_return:>9.2%}"
            )
        else:
            click.echo(
                f"{symbol:>6} | {'No data':>10} | {'No data':>10} | {'No data':>10} | {'No data':>10}"
            )

    # Handle output
    if output:
        returns_df.to_csv(output)
        click.echo(f"\n✅ Daily returns saved to: {output}")
        click.echo(
            f"📊 Data shape: {returns_df.shape[0]} dates, {returns_df.shape[1]} symbols"
        )
    else:
        click.echo("\n📊 Daily Returns DataFrame:")
        click.echo("=" * 60)
        click.echo(returns_df.to_string())
        click.echo(
            f"\nData shape: {returns_df.shape[0]} dates, {returns_df.shape[1]} symbols"
        )
