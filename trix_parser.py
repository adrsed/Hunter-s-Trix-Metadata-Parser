import argparse
import datetime
import os
import re
import sys
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("dir", nargs='?')  # album directory
parser.add_argument("-m", "--metadata", help="File containing the metadata")  # metadata file
parser.add_argument("-c", "--cover", help="Album Cover")  # album cover
parser.add_argument("-a", "--artist")
parser.add_argument("-v", "--volume")
parser.add_argument("-g", "--genre", default="Rock")
parser.add_argument("-r", "--rename", action="store_true")

args = parser.parse_args()

if args.dir is None:
    print("No input directory given. Exiting.")
    sys.exit(1)

genre = args.genre

album_dir = args.dir

# Search for metadata file or take from arguments if provided.
# Filename looks like "gd73-06-22.mtx.seamons.txt".
if args.metadata is not None:
    metadata = args.metadata
    if not os.path.isfile(metadata):
        print(f"Provided metadata file is can not be found. Exiting.")
        sys.exit(1)

    metadata = os.path.split(metadata)[1]  # remove directory prefix, as it would break the script later on
else:
    metadata = [f for f in os.listdir(album_dir) if re.match(r".*\.mtx\.seamons\.txt", f)]
    if len(metadata) == 0:
        print("Failed to locate metadata file, place it in the correct directory or provide a path using -m flag. "
              "Exiting.")
        sys.exit(1)

    metadata = metadata[0]

print(f"Metadata file: {metadata}")

# Locate cover file or take from arguments if provided.
# Cover image is usually named something like "gd730622_front1.jpg".
# Sometimes there are more than one image, use the first one found in that case.
if args.cover is not None:
    cover = args.cover
    if not os.path.isfile(cover):
        print(f"Provided cover file is can not be found. Exiting.")
        sys.exit(1)

    cover = os.path.split(cover)[1]  # remove directory prefix, as it would break the script later on
else:
    cover = [f for f in os.listdir(album_dir) if re.match(r".*_front*.\.jpg", f)]
    if len(cover) == 0:
        print("Failed to locate cover image, place it in the correct directory or provide a path using -c flag. "
              "Exiting.")
        sys.exit(1)

    cover = cover[0]

print(f"Cover file: {cover}")
cover = os.path.join(album_dir, cover)

# Extract volume number from directory name.
# If unchanged, the directory name looks something like "gd73-06-22.mtx.seamons.ht12.92375.flac16" with the "ht12".
# denoting the volume number, Volumes 82-94 were labeled as "Jubal's Trix", so the notation is with a "j" instead.
if args.volume is not None:
    vol = args.volume
else:
    vol = re.search(r"\.[hj]t[0-9]*\.", album_dir)
    if vol is None:
        vol = input("Could not extract Volume from directory name, please enter: ")
    else:
        vol = re.sub('[.hjt]', '', vol.group(0))

print()

# ======================================================================================================================
# Read Metadata file

# First four lines of the metadat file look something like this:
# Grateful Dead
# P.N.E. Coliseum
# Vancouver, BC, Canada
# June 22, 1973
lines = [line.strip() for line in open(os.path.join(album_dir, metadata), "rt")]

# Take artist from command or the file
if args.artist is not None:
    artist = args.artist
else:
    artist = lines[0]

venue = lines[1]
loc = lines[2]
date = lines[3]

date = datetime.datetime.strptime(date, "%B %d, %Y")
year = date.year
show = date.strftime("%y-%m-%d")  # used for predicting filenames
date = date.strftime("%Y-%m-%d")

# Album title
# 1973-06-22 - P.N.E. Coliseum (Hunter's Trix Vol. 12)
album = f"{date} - {venue} (Hunter's Trix Vol. {vol})"
print(album)
print()

# Filter metadata file for tracks
# Track lines look like "d1t01 - Bertha"
lines = [line for line in lines if " - " in line and line[0] == 'd']

for line in lines:
    print(f"Track specifier from Metadata: {line}")

    # Identifier is "d1t01"
    identifier = re.search(r"^d[0-9]t[0-9]*", line).group(0)

    # The number after the 'd' is the disc number
    disc = identifier[1]  # this wouldn't work if there are over 9 discs, but there probably won't be

    # Track number is anything after the 't', remove that and any leading 0s
    track = re.search(r"t[0-9]*", identifier).group(0).lstrip("t").lstrip("0")

    # Title is anything after the " - "
    title = re.search(r" - .*$", line).group(0).lstrip(" - ")

    print(f"Identifier: {identifier}, Disc: {disc}, Track: {track}, Title: {title}")

    # Files are named "gd73-06-22d1t01"
    filename = f"gd{show}{identifier}.flac"
    print(f"Predicted filename: {filename}")
    filepath = os.path.join(album_dir, filename)

    if not os.path.isfile(filepath):
        print("Could not find predicted filename. Exiting.")
        sys.exit()

    # metaflac doesn't overwrite metadata, remove any old data
    print(f"Removing old metadata from {filename}.")
    call(["metaflac", "--remove-all-tags", filepath])

    print(f"Writing new metadata to {filename}")
    call(["metaflac", f"--set-tag=ARTIST={artist}",
                      f"--set-tag=DISCNUMBER={disc}",
                      f"--set-tag=TRACKNUMBER={track}",
                      f"--set-tag=TITLE={title}",
                      f"--set-tag=ALBUM={album}",
                      f"--set-tag=ALBUMARTIST={artist}",
                      f"--set-tag=DATE={date}",
                      f"--set-tag=YEAR={year}",
                      f"--set-tag=GENRE={genre}",
                      f"--import-picture-from={cover}", filepath])

    print()

if args.rename:
    print(f"Renaming directory to {album}.")
    prefix = os.path.split(album_dir)[0]
    new_dir = os.path.join(prefix, album)
    os.rename(album_dir, new_dir)

print("Done.")
