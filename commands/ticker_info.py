from data_provider.yf_data_provider import YFDataProvider
from tabulate import tabulate

def run(args):
    provider = YFDataProvider()
    info = provider.get_ticker_info(args.ticker)
    if not info:
        print(f"No info found for ticker {args.ticker}")
        return

    def clean_value(v):
        if v is None:
            return ""
        s = str(v).strip()
        if len(s) > 100:
            return s[:97] + "..."
        return s

    # Filter and clean
    table = [(k, clean_value(v)) for k, v in info.items() if v not in [None, "", [], {}] and str(v).strip()]
    print(tabulate(table, headers=["Field", "Value"], tablefmt="psql"))
