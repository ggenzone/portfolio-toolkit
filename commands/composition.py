from portfolio.portfolio import Portfolio
from data_provider.yf_data_provider import YFDataProvider

def run(args):
    data_provider = YFDataProvider()
    cartera = Portfolio(json_filepath=args.file, data_provider=data_provider)
    cartera.plot_composition()
