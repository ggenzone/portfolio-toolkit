import argparse
from cli.commands.composition import run as run_composition
from cli.commands.correlation import run as run_correlation
from cli.commands.plot import run as run_plot
from cli.commands.print_positions import run as run_print_positions
from cli.commands.export_transactions import run as run_export_transactions
from cli.commands.dump_data_frame import run as run_dump_data_frame
from cli.commands.clear_cache import run as run_clear_cache
from cli.commands.ticker_info import run as run_ticker_info


def main():
    parser = argparse.ArgumentParser(description="Portfolio Tools CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: composition
    parser_composition = subparsers.add_parser('composition', help='Plot the portfolio composition')
    parser_composition.add_argument('-f', '--file', required=True, help='Portfolio file in JSON format')

    # Subcommand: correlation
    parser_correlation = subparsers.add_parser('correlation', help='Calculate correlation between asset pairs')
    parser_correlation.add_argument('-t', '--tickers', required=True, help='Comma-separated list of tickers (e.g. AAPL,MSFT,GOOGL)')

    # Subcommand: plot
    parser_plot = subparsers.add_parser('plot', help='Plot the price evolution of a list of assets')
    parser_plot.add_argument('-t', '--tickers', required=True, help='Comma-separated list of tickers (e.g. AAPL,MSFT,GOOGL)')

    # Subcommand: print-positions
    parser_print_positions = subparsers.add_parser('print-positions', help='Print current portfolio positions as a table')
    parser_print_positions.add_argument('-f', '--file', required=True, help='Portfolio file in JSON format')
    parser_print_positions.add_argument('-d', '--date', help='Target date in YYYY-MM-DD format (optional)')

    # Subcommand: export-transactions
    parser_export_transactions = subparsers.add_parser('export-transactions', help='Export all portfolio transactions in CSV format')
    parser_export_transactions.add_argument('-f', '--file', required=True, help='Portfolio file in JSON format')

    # Subcommand: dump-data-frame
    parser_dump_data_frame = subparsers.add_parser('dump-data-frame', help='Dump portfolio DataFrame for debugging purposes')
    parser_dump_data_frame.add_argument('-f', '--file', required=True, help='Portfolio file in JSON format')

    # Subcommand: clear-cache
    parser_clear_cache = subparsers.add_parser('clear-cache', help='Delete all cache files in temp/*.pkl')

    # Ticker info command
    ticker_info_parser = subparsers.add_parser("ticker-info", help="Show detailed ticker information")
    ticker_info_parser.add_argument("ticker", help="Ticker symbol (e.g., AAPL, SHOP)")

    # Convert currency command
    convert_parser = subparsers.add_parser("convert-currency", help="Convert ticker prices to different currency")
    convert_parser.add_argument("ticker", help="Ticker symbol (e.g., AAPL, SHOP)")
    convert_parser.add_argument("currency", help="Target currency (e.g., EUR, USD, CAD)")
    convert_parser.add_argument("--days", type=int, default=5, help="Number of recent days to show (default: 5)")

    args = parser.parse_args()

    if args.command == 'composition':
        run_composition(args)
    elif args.command == 'correlation':
        run_correlation(args)
    elif args.command == 'plot':
        run_plot(args)
    elif args.command == 'print-positions':
        run_print_positions(args)
    elif args.command == 'export-transactions':
        run_export_transactions(args)
    elif args.command == 'dump-data-frame':
        run_dump_data_frame(args)
    elif args.command == 'clear-cache':
        run_clear_cache(args)
    elif args.command == "ticker-info":
        from cli.commands.ticker_info import run
        run(args)
    elif args.command == "convert-currency":
        from cli.commands.convert_currency import run
        run(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
