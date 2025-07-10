def print_current_positions(df_portfolio):
    """
    Prints a table of current positions: Ticker | Current Price | Cost | Quantity | Value | Return (%)

    Args:
        df_portfolio (pd.DataFrame): Structured DataFrame with the portfolio evolution.
    """
    if df_portfolio is None or df_portfolio.empty:
        print("No data available to display current positions.")
        return

    # Filter by the latest available date
    last_date = df_portfolio['Date'].max()
    df_current = df_portfolio[df_portfolio['Date'] == last_date]

    # Group by ticker and sum values
    summary = df_current.groupby('Ticker').agg({
        'Price': 'last',
        'Cost': 'sum',
        'Quantity': 'sum',
        'Value': 'sum'
    }).reset_index()

    # Filter out tickers with zero quantity
    summary = summary[summary['Quantity'] > 0]

    # Calculate return percentage
    summary['Return (%)'] = ((summary['Value'] - summary['Cost']) / summary['Cost']) * 100
    summary['Return (%)'] = summary['Return (%)'].replace([float('inf'), float('-inf')], 0).fillna(0)

    print(f"{'| Ticker':<10}| {'Current Price':<15}| {'Cost':<12}| {'Quantity':<10}| {'Value':<12}| {'Return (%)':<12}|")
    print("|" + "-"*9 + "|" + "-"*14 + "|" + "-"*11 + "|" + "-"*9 + "|" + "-"*11 + "|" + "-"*11 + "|")
    for _, row in summary.iterrows():
        print(f"| {row['Ticker']:<8}| {row['Price']:<13.2f}| {row['Cost']:<11.2f}| {row['Quantity']:<8.2f}| {row['Value']:<10.2f}| {row['Return (%)']:<10.2f}|")
