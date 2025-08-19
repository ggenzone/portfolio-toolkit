import click
from tabulate import tabulate

from portfolio_toolkit.data_provider.yf_data_provider import YFDataProvider
from portfolio_toolkit.portfolio import Portfolio

from ..utils import load_json_file


@click.command("tax-report")
@click.argument("file", type=click.Path(exists=True))
@click.argument("year", required=True)
def tax_report(file, year):
    """Generate tax report (gains/losses)"""
    data = load_json_file(file)

    previous_year = int(year) - 1
    previous_last_day = f"{previous_year}-12-31"

    first_day = f"{year}-01-01"
    last_day = f"{year}-12-31"
    click.echo(
        f"Generating tax report for the year {year} from {first_day} to {last_day}"
    )

    data_provider = YFDataProvider()
    portfolio = Portfolio.from_dict(data, data_provider=data_provider)

    stats = portfolio.get_stats(year)

    closed_positions_df = stats.closed_positions
    open_positions_df = stats.open_positions
    transactions_df = stats.transactions

    output = f"{year}-tax_report.md"
    with open(output, "w", encoding="utf-8") as f:
        f.write(f"# Tax Report for {portfolio.name} ({year})\n")
        f.write("\n\n")

        f.write(f"## 📊 Portfolio overview for {year}\n\n")

        f.write("### Portfolio Valuation\n\n")
        valuation_data = [
            [
                "Valuation",
                f"{stats.initial_valuation:.2f}",
                f"{stats.final_valuation:.2f}",
            ],
            [
                "Cash",
                f"{stats.initial_cash:.2f}",
                f"{stats.final_cash:.2f}",
            ],
            [
                "Return",
                "",
                (
                    f"{(stats.final_valuation - stats.initial_valuation) / stats.initial_valuation:.2%}"
                    if stats.initial_valuation > 0
                    else "N/A"
                ),
            ],
        ]

        headers = ["", previous_last_day, last_day]

        f.write(
            tabulate(valuation_data, headers=headers, tablefmt="github", floatfmt=".2f")
        )
        f.write("\n\n")

        f.write("### Financial Summary\n\n")

        summary_data = [
            ["Valuation", f"{stats.final_valuation:.2f}"],
            ["Profit", f"{stats.realized_profit:.2f}"],
            ["Unrealized Profit", f"{stats.unrealized_profit:.2f}"],
            ["Deposits", f"{stats.deposits:.2f}"],
            ["Withdrawals", f"{stats.withdrawals:.2f}"],
            ["Incomes", f"{stats.incomes:.2f}"],
        ]

        headers = ["", last_day]

        f.write(
            tabulate(summary_data, headers=headers, tablefmt="github", floatfmt=".2f")
        )
        f.write("\n\n")

        f.write(f"## 📊 Open positions at {last_day}\n\n")

        f.write(
            tabulate(
                open_positions_df, headers="keys", tablefmt="github", floatfmt=".2f"
            )
        )
        f.write("\n\n")

        f.write(f"## 📊 Cash transactions at {last_day}\n\n")

        f.write("### Cash Incomes\n\n")

        incomes = transactions_df[(transactions_df["type"] == "income")]

        f.write(tabulate(incomes, headers="keys", tablefmt="github", floatfmt=".2f"))
        f.write("\n\n")

        f.write("### Cash Deposits\n\n")

        deposits = transactions_df[(transactions_df["type"] == "deposit")]

        f.write(tabulate(deposits, headers="keys", tablefmt="github", floatfmt=".2f"))
        f.write("\n\n")

        f.write("### Cash Withdrawals\n\n")

        withdrawals = transactions_df[(transactions_df["type"] == "withdrawal")]

        f.write(
            tabulate(withdrawals, headers="keys", tablefmt="github", floatfmt=".2f")
        )
        f.write("\n\n")

        f.write(f"## 📊 Closed positions at {last_day}\n\n")

        f.write(
            tabulate(
                closed_positions_df, headers="keys", tablefmt="github", floatfmt=".2f"
            )
        )
        f.write("\n\n")

    print("-" * 50)
