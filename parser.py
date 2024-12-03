import argparse
import datetime
import os
import re
import sys
from subprocess import call

# CONSTANTS
artist = "Grateful Dead"
genre = "Rock"

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
# filename looks like "gd73-06-22.mtx.seamons.txt"
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
show = date.strftime("%y-%m-%d") # used for predicting filenames
date = date.strftime("%Y-%m-%d")

# Album title
# 1973-06-22 - P.N.E. Coliseum (Hunter's Trix Vol. 12)
album = f"{date} - {venue} (Hunter's Trix Vol. {vol})"
print(album)


# filter metadata file for tracks
# Track lines look like "d1t01 - Bertha"
lines = [line for line in lines if " - " in line and line[0] == 'd']

for line in lines:
    print(f"Track specifier from Metadata: {line}")

    # Identifier is "d1t01"
    identifier = re.search(r"^d[0-9]t[0-9]*", line).group(0)

    # the number after the 'd' is the disc number
    disc = identifier[1] # this wouldn't work if there are over 9 discs, but there probably won't be

    # Track number is anything after the 't', remove that and any leading 0s
    track = re.search(r"t[0-9]*", identifier).group(0).lstrip("t").lstrip("0")

    # Title is anything after the " - "
    title = re.search(r"\ -\ .*$", line).group(0).lstrip(" - ")

    print(f"Identifier: {identifier}, Disc: {disc}, Track: {track}, Title: {title}")

    # Files are named "gd73-06-22d1t01"
    filename = f"gd{show}{identifier}.flac"
    print(f"Predicted filename: {filename}")

    if not os.path.isfile(filename):
        print("Could not find predicted filename. Exiting.")
        sys.exit()

    # metaflac doesn't overwrite metadata, remove any old data
    print(f"Removing old metadata from {filename}.")
    call(["metaflac", "--remove-all-tags", filename])

    print("Writing new metadata.")
    call(["metaflac", f"--set-tag=ARTIST={artist}", filename])
    call(["metaflac", f"--set-tag=DISCNUMBER={disc}", filename])
    call(["metaflac", f"--set-tag=TRACKNUMBER={track}", filename])
    call(["metaflac", f"--set-tag=TITLE={title}", filename])
    call(["metaflac", f"--set-tag=ALBUM={album}", filename])
    call(["metaflac", f"--set-tag=ALBUMARTIST={artist}", filename])
    call(["metaflac", f"--set-tag=DATE={date}", filename])
    call(["metaflac", f"--set-tag=YEAR={year}", filename])
    call(["metaflac", f"--set-tag=GENRE={genre}", filename])
    call(["metaflac", f"--import-picture-from={cover}", filename])

    print()

print("Done.")


