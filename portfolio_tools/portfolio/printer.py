def print_current_positions(df_portfolio, target_date=None):
    """
    Prints a table of current positions: Ticker | Current Price | Cost | Quantity | Value | Return (%)

    Args:
        df_portfolio (pd.DataFrame): Structured DataFrame with the portfolio evolution.
        target_date (str, optional): Date in YYYY-MM-DD format. If None, uses the most recent date.
    """
    if df_portfolio is None or df_portfolio.empty:
        print("No data available to display current positions.")
        return

    # If target_date is provided, use it; otherwise find the most recent suitable date
    if target_date:
        from datetime import datetime
        try:
            target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
            # Check if the target date exists in the DataFrame
            available_dates = df_portfolio['Date'].dt.date.unique()
            if target_datetime.date() not in available_dates:
                # Find the closest earlier date
                earlier_dates = [d for d in available_dates if d <= target_datetime.date()]
                if not earlier_dates:
                    print(f"No data available for date {target_date} or earlier.")
                    return
                closest_date = max(earlier_dates)
                target_datetime = datetime.combine(closest_date, datetime.min.time())
                print(f"No data for {target_date}, using closest earlier date: {closest_date}")
            
            last_date = target_datetime
        except ValueError:
            print(f"Invalid date format: {target_date}. Please use YYYY-MM-DD format.")
            return
    else:
        # Find the most recent date that has data for all tickers with positions
        # First, find tickers that have any quantity > 0 at any point
        tickers_with_positions = set(df_portfolio[df_portfolio['Quantity'] > 0]['Ticker'].unique())
        
        # Find the most recent date where all these tickers have data
        last_date = None
        for date in sorted(df_portfolio['Date'].unique(), reverse=True):
            df_date = df_portfolio[df_portfolio['Date'] == date]
            tickers_in_date = set(df_date['Ticker'].unique())
            
            if tickers_with_positions.issubset(tickers_in_date):
                last_date = date
                break
        
        if last_date is None:
            print("No suitable date found with data for all tickers.")
            return
    
    # Filter by the selected date
    df_current = df_portfolio[df_portfolio['Date'] == last_date]

    # Group by ticker and sum values
    summary = df_current.groupby('Ticker').agg({
        'Price': 'last',
        'Price_Base': 'last',
        'Cost': 'sum',
        'Quantity': 'sum',
        'Value': 'sum',
        'Value_Base': 'sum'
    }).reset_index()

    # Filter out tickers with zero quantity
    summary = summary[summary['Quantity'] > 0]

    # For non-cash tickers, calculate current market value in base currency
    # Cash tickers (__EUR, etc.) already have correct Value_Base
    for idx, row in summary.iterrows():
        if not row['Ticker'].startswith('__'):
            # For real assets, we need to convert current market price to base currency
            # Get the current market price and convert it
            current_price = row['Price']  # Current market price in original currency
            quantity = row['Quantity']
            
            # We need to get the current exchange rate to convert to base currency
            # For now, we'll use a simplified approach using the Value_Base from the DataFrame
            # The correct Value_Base should already be calculated in the preprocessing
            pass  # Value_Base is already correctly calculated in preprocesador.py

    # Calculate return percentage using Value_Base
    summary['Return (%)'] = ((summary['Value_Base'] - summary['Cost']) / summary['Cost']) * 100
    summary['Return (%)'] = summary['Return (%)'].replace([float('inf'), float('-inf')], 0).fillna(0)

    # Calculate total portfolio value in base currency
    total_value_base = summary['Value_Base'].sum()
    total_cost = summary['Cost'].sum()
    total_return = ((total_value_base - total_cost) / total_cost) * 100 if total_cost > 0 else 0

    print(f"Current positions as of {last_date.date()}:")
    print(f"{'| Ticker':<10}| {'Price Base':<12}| {'Cost':<12}| {'Quantity':<10}| {'Value Base':<12}| {'Return (%)':<12}|")
    print("|" + "-"*9 + "|" + "-"*11 + "|" + "-"*11 + "|" + "-"*9 + "|" + "-"*11 + "|" + "-"*11 + "|")
    for _, row in summary.iterrows():
        # For display, show the market price converted to base currency
        if row['Ticker'].startswith('__'):
            display_price = row['Price_Base']  # Cash always 1.0 in base currency
        else:
            # Calculate current market price in base currency for display
            display_price = row['Value_Base'] / row['Quantity'] if row['Quantity'] > 0 else 0
        
        print(f"| {row['Ticker']:<8}| {display_price:<11.2f}| {row['Cost']:<11.2f}| {row['Quantity']:<8.2f}| {row['Value_Base']:<10.2f}| {row['Return (%)']:<10.2f}|")
    
    print("|" + "-"*9 + "|" + "-"*11 + "|" + "-"*11 + "|" + "-"*9 + "|" + "-"*11 + "|" + "-"*11 + "|")
    print(f"| {'TOTAL':<8}| {'':<11}| {total_cost:<11.2f}| {'':<8}| {total_value_base:<10.2f}| {total_return:<10.2f}|")

def print_transactions_csv(assets):
    """
    Prints all transactions in CSV format, ordered by date and not grouped by ticker.
    
    Args:
        assets (list): List of asset dictionaries containing transactions.
    """
    # Collect all transactions from all assets
    all_transactions = []
    
    for asset in assets:
        ticker = asset["ticker"]
        for transaction in asset["transactions"]:
            # Create a copy of the transaction and add the ticker
            tx = transaction.copy()
            tx["ticker"] = ticker
            all_transactions.append(tx)
    
    # Sort by date
    all_transactions.sort(key=lambda x: x["date"])
    
    if not all_transactions:
        print("No transactions available.")
        return
    
    # Print CSV header
    print("Date,Ticker,Type,Quantity,Price,Currency,Total,Exchange Rate,Subtotal Base,Fees Base,Total Base")
    
    # Print each transaction
    for tx in all_transactions:
        print(f"{tx.get('date', '')},{tx.get('ticker', '')},"
              f"{tx.get('type', '')},{tx.get('quantity', 0):.2f},"
              f"{tx.get('price', 0):.2f},{tx.get('currency', '')},"
              f"{tx.get('total', 0):.2f},{tx.get('exchange_rate', 0):.2f},"
              f"{tx.get('subtotal_base', 0):.2f},{tx.get('fees_base', 0):.2f},"
              f"{tx.get('total_base', 0):.2f}")
