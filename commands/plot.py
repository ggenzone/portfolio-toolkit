from data_provider.yf_data_provider import YFDataProvider
from plot.plot_assets import plot_assets

def run(args):
    data_provider = YFDataProvider()
    tickers = [t.strip() for t in args.tickers.split(',') if t.strip()]
    series = [data_provider.get_price_series(ticker) for ticker in tickers]
    plot_assets(series, tickers)
