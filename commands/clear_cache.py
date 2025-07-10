import os
import glob

def run(args):
    files = glob.glob('temp/*.pkl')
    if not files:
        print("No cache files found in temp/.")
        return
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    print("Cache cleared.")
