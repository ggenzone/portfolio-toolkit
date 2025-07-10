from portfolio_tools.data_provider.yf_data_provider import YFDataProvider
from portfolio_tools.utils.correlation import calculate_correlation
from portfolio_tools.utils.log_returns import calculate_log_returns

def run(args):
    data_provider = YFDataProvider()
    tickers = [t.strip() for t in args.tickers.split(',') if t.strip()]
    prices = {ticker: data_provider.get_price_series(ticker) for ticker in tickers}
    returns = {ticker: calculate_log_returns(prices[ticker]) for ticker in tickers}
    print("|" + "-"*37 + "|")
    print(f"{'| Ticker 1':<12}| {'Ticker 2':<10}| {'Correlation':<12}|")
    print("|" + "-"*11 + "|" + "-"*11 + "|" + "-"*13 + "|")
    for i in range(len(tickers)):
        for j in range(i+1, len(tickers)):
            corr = calculate_correlation(returns[tickers[i]], returns[tickers[j]])
            print(f"| {tickers[i]:<10}| {tickers[j]:<10}| {corr:<12.4f}|")
    print("|" + "-"*37 + "|")
