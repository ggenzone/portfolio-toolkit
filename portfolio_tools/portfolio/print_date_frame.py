from portfolio_tools.portfolio.portfolio import Portfolio


def print_data_frame(portfolio: Portfolio):
    """
    Prints the portfolio DataFrame in a readable format for debugging purposes.
    """
    print(
        f"Portfolio '{portfolio.name}' initialized with {len(portfolio.assets)} assets."
    )
    print(f"Portfolio currency: {portfolio.currency}")
    if portfolio.df_portfolio is not None:
        temp = portfolio.df_portfolio.sort_values(by=["Date"], ascending=True)
        print(temp.to_string())
        print(
            f"Portfolio DataFrame initialized with {len(portfolio.df_portfolio)} records."
        )
    else:
        print("No DataFrame available - portfolio not properly initialized.")
