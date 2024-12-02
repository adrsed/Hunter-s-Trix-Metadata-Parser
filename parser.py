import argparse
import datetime
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("dir", nargs='*') # album directory
parser.add_argument("-m", "--metadata", help="File containing the metadata") # metadata file
parser.add_argument("-c", "--cover", help="Album Cover") # album cover

args = parser.parse_args()

if args.dir == []:
    print("No input directory given. Exiting.")
    sys.exit()

dir = args.dir[0] # TODO handle multiple directories properly
os.chdir(dir)

# search for metadata file
# Metadata file looks like "gd73-06-22.mtx.seamons.txt"
metadata = [f for f in os.listdir(dir) if re.match(r".*\.mtx\.seamons\.txt", f)]

if len(metadata) == 0:
    if args.metadata is None:
        print("Failed to locate metadata file, place it in the correct directory or provide a path using -m flag. "
              "Exiting")
        sys.exit()
    else:
        metadata = args.metadata
else:
    metadata = metadata[0]

print(f"Metadata file: {metadata}")

# locate cover file
# Cover image is usually named something like "gd730622_front1.jpg"
# sometimes there are more than one image, use the first one found in that case
cover = [f for f in os.listdir(dir) if re.match(r".*_front*.\.jpg", f)]

if len(cover) == 0:
    if args.cover is None:
        print("Failed to locate cover image, place it in the correct directory or provide a path using -c flag. "
              "Exiting.")
        sys.exit()
    else:
        cover = args.cover
else:
    cover = cover[0]

print(f"Cover file: {cover}")

# extract volume number from directory name
# if unchanged, the directory name looks something like "gd73-06-22.mtx.seamons.ht12.92375.flac16" with the "ht12"
# denoting the volume number, Volumes 82-94 were labeled as "Jubal's Trix", so the notation is with a "j" instead of "h"
vol = re.search(r"\.[hj]t[0-9]*\.", dir)
if vol is None:
    vol = input("Could not extract Volume from directory name, please enter: ")
else:
    vol = re.sub('[.hjt]', '', vol.group(0))

print()

# ==========================================================
# Read Metadata file

# First four lines of the metadat file look something like this:
# Grateful Dead
# P.N.E. Coliseum
# Vancouver, BC, Canada
# June 22, 1973
lines = [line.strip() for line in open(metadata, "rt")]
venue = lines[1]
loc = lines[2]
date = lines[3]

date = datetime.datetime.strptime(date, "%B %d, %Y")
year = date.year
date = date.strftime("%Y-%m-%d")

# Album title
# 1973-06-22 - P.N.E. Coliseum (Hunter's Trix Vol. 12)
album = f"{date} - {venue} (Hunter's Trix Vol. {vol})"
print(album)


