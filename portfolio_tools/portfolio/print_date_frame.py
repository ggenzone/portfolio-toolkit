from portfolio_tools.portfolio.time_series_portfolio import TimeSeriesPortfolio


def print_data_frame(portfolio: TimeSeriesPortfolio):
    """
    Prints the portfolio DataFrame in a readable format for debugging purposes.
    """
    print(
        f"Portfolio '{portfolio.name}' initialized with {len(portfolio.assets)} assets."
    )
    print(f"Portfolio currency: {portfolio.currency}")
    if portfolio.portfolio_timeseries is not None:
        temp = portfolio.portfolio_timeseries.sort_values(by=["Date"], ascending=True)
        print(temp.to_string())
        print(
            f"Portfolio DataFrame initialized with {len(portfolio.portfolio_timeseries)} records."
        )
    else:
        print("No DataFrame available - portfolio not properly initialized.")
