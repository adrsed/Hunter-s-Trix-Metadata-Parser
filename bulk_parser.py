import argparse
import os
import re
import subprocess
import sys
from subprocess import call

parser = argparse.ArgumentParser()

parser.add_argument("dir", nargs="?")
parser.add_argument("-r", "--rename", action="store_true", help="Rename the directory to the album title.")

args = parser.parse_args()

if args.dir is None:
    print("No input directory given. Exiting.")
    sys.exit(1)

# Get any matching directories.
# Directories are named like "gd73-06-22.mtx.seamons.ht12.92375.flac16", we only want to process these, as they
# should provide all the files and information needed automatically.
dirs = [d for d in os.listdir(args.dir) if re.match(r".*\.mtx\.seamons\.[hj]t[0-9]+\.[0-9]+\.", d)]

# "dir" will be replaced by the actual directory
exec_args = ["python3", "trix_parser.py", "dir"]

# Pass through for the rename flag.
if args.rename:
    exec_args.append("-r")

# Keep track of errors.
error_count = 0
error_list = []

for album_dir in dirs:
    print(f"Processing {album_dir}")

    album_path = os.path.join(args.dir, album_dir)
    exec_args[2] = album_path

    # Execute trix_parser.py without output.
    res = call(exec_args, stdout=subprocess.DEVNULL)

    if res != 0:
        error_count += 1
        error_list.append(album_dir)

print()
completed = len(dirs) - error_count
print(f"Completed {completed}/{len(dirs)}.")

if error_count > 0:
    print("Errors occurred in the following directories:")
    for d in error_list:
        print(d)