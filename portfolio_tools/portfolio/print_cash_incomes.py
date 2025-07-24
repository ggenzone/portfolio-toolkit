from .portfolio import Portfolio


def print_cash_incomes(portfolio: Portfolio, from_date: str, to_date: str):
    """Print cash incomes in the portfolio"""
    print("Cash Incomes:")
    print("-" * 50)

    count = 0
    total_income = 0.0

    for transaction in portfolio.account.transactions:
        # Filter transactions based on type and date range
        if (
            transaction.transaction_date < from_date
            or transaction.transaction_date > to_date
        ):
            continue

        # Only print income transactions
        if transaction.transaction_type == "income":
            count += 1
            total_income += transaction.amount
        else:
            # If you want to print other types of transactions, you can add conditions here
            # For now, we only print income transactions
            continue

    print(f"Total Income Transactions: {count}")
    print(f"Total Income Amount: {total_income}")

    print("-" * 50)
