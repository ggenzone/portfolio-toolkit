import os
import glob

def run(args):
    cache_dir = "/tmp/portfolio_tools_cache"
    files = glob.glob(f'{cache_dir}/*.pkl')
    if not files:
        print(f"No cache files found in {cache_dir}/.")
        return
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    print("Cache cleared.")
