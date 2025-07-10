from utils.correlation import calculate_correlation
from portfolio.portfolio import Portfolio
from data_provider import YFDataProvider
from datetime import datetime
import sys
from tabulate import tabulate


# Create an instance of YFDataProvider
data_provider = YFDataProvider()

# Constants for tickers
BRENT = "BZ=F"
WTI = "CL=F"
GOLD = "GC=F"
NASDAQ = "^IXIC"
SP500 = "^GSPC"
DOW_JONES = "^DJI"
MERVAL = "^MERV"
BOND_10Y_USA = "^TNX"
DOLLAR_INDEX = "DX-Y.NYB"
VIX = "^VIX"


def print_pretty_df(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))

df = data_provider.get_raw_data("YPF")
print_pretty_df(df)

sys.exit()

# Example usage
ticker1 = "GGAL"
ticker2 = "YPF"

# Calculate returns
returns1 = data_provider.calculate_returns(ticker1)
returns2 = data_provider.calculate_returns(ticker2)

# Calculate correlation
correlation = calculate_correlation(returns1, returns2)
print(f"Correlation between {ticker1} and {ticker2}: {correlation}")

# Plot assets (uncomment and implement if needed)
# plot_assets([prices1, prices2], [ticker1, ticker2])

# Load portfolio from JSON
portfolio_json = Portfolio(json_filepath="portfolio.json", data_provider=data_provider)
portfolio_json.plot_composition()
portfolio_json.plot_ticker_evolution(ticker='JOBY')
portfolio_json.plot_evolution_vs_cost()
portfolio_json.plot_evolution_stacked()
# dates_json, portfolio_value_json = portfolio_json.calculate_value()
# plot_portfolio_evolution(dates_json, portfolio_value_json)

