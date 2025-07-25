import glob
import os

import click


@click.command(name="clear-cache")
def clear_cache():
    """Delete all cache files in temp/*.pkl."""
    cache_dir = "/tmp/portfolio_tools_cache"

    if not os.path.exists(cache_dir):
        print(f"Cache directory {cache_dir} does not exist.")
        return

    # Clear historical data cache files
    historical_files = glob.glob(f"{cache_dir}/*_historical_data.pkl")

    # Clear ticker info cache files
    info_files = glob.glob(f"{cache_dir}/*_info.pkl")

    all_files = historical_files + info_files

    if not all_files:
        print("No cache files found to delete.")
        return

    print(f"Found {len(all_files)} cache files to delete:")
    print(f"  - {len(historical_files)} historical data files")
    print(f"  - {len(info_files)} ticker info files")

    for file in all_files:
        os.remove(file)
        print(f"Deleted: {os.path.basename(file)}")

    print(f"\n✅ Successfully cleared {len(all_files)} cache files.")
