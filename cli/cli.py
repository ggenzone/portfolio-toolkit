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
    parser = argparse.ArgumentParser(description="CLI for financial portfolio analysis and visualization")
    parser.add_argument('-v', '--version', action='version', version='Finanzas CLI 1.0')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

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

    # Subcommand: ticker-info
    parser_ticker_info = subparsers.add_parser('ticker-info', help='Show detailed info for a ticker')
    parser_ticker_info.add_argument('-t', '--ticker', required=True, help='Ticker symbol (e.g. AAPL)')

    # You can add more subcommands in the future

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
    elif args.command == 'ticker-info':
        run_ticker_info(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
