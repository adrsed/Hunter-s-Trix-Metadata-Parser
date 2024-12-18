# Hunter's Trix Metadata Parser
Metadata Parser for Hunter's Trix

[Hunter's Trix](https://www.facebook.com/GratefulDeadTrix) is a collection of 
incredible Matrix recordings of a bunch of Grateful Dead shows.
They have one problem however: Volumes 1 through 94 lack metadata in the FLAC
files, adding those manually takes a lot of time, which this script aims to solve.
It can also be used to easily adjust existing metadata (e.g. cover art or the 
format of the album title).

This is based on an [already existing parser](https://github.com/shacker/trix) 
with some changes:
1. It omits the conversion to ALAC, since I didn't need it
(although I might add conversion to different formats in the future).
2. It only requires metaflac to be installed.
3. All relevant information is found automatically, but can still be supplied via
the command line.
4. The directory containing the files (and other data) is supplied via the 
command line instead of having to change variables in the file.
5. There is an additional script to process multiple shows at once.

Tested on Windows and Linux.

## Usage
### Requirements
You will need to work with the command line, so a tiny bit of
computer wizardry is required.

The [metaflac](https://xiph.org/flac/documentation_tools_metaflac.html) CLI binary
needs to be installed and working. If you are on Windows, a simple way is to have
the ``metaflac.exe`` in the same directory as ``trix_parser.py``

You can copy ```trix_parser.py``` to some folder in your python path, if you don't
you simply will have to use the full path to the file in step 1.

### Running the parser
1. Torrent a show of your choosing, the directory name should look something 
like ``gd73-06-22.mtx.seamons.ht12.92375.flac16`` after the download is complete.
Don't change that name.
2. In a terminal, run ```python trix_parser.py <path to the directory>```. 
You can use some options here, see [the below section](#command-line-options) 
for that.
3. (If you have renamed the directory or didn't supply it via the command line,
you would have to enter the volume number now.)
4. Wait a few seconds.
5. Enjoy!

#### Command Line Options
There are some command line options you can use with the parser.

- ``-r``, ``--rename`` - Rename the directory to the generated album title 
at the end of the process.

The information for the following options is grabbed automatically, but you
may still use them to provide it manually if grabbing them doesn't work or
you simply want to for some reason.
- ``-m``, ``--metadata`` - Specify a metadata file.
- ``-c``, ``--cover`` - Specify a cover file.
- ``-a``, ``--artist`` - Specify an artist, default is "Grateful Dead" but e.g.
Vol. 105 is a solo Jerry show (ironically the script doesn't work with this one
as the metadata file is formatted differently, but it exists now).
- ``-v``, ``--version`` - Specify a version number.

This is completely unnecessary but it's only one line I like 
over-engineering things.
- ``-g``, ``--genre`` - Specify a different genre, default value is "Rock".

### Processing multiple shows at once

Using ``bulk_parser.py`` you can process multiple shows at once. This only really works
if you don't rename anything and just pass the torrents directly into this.

Simply run ```python bulk_parser.py <path_to_directory>``` where ``<path_to_directory>``
is the directory containing the downloaded shows. The script only processes the 
directories with the naming scheme they use by default 
(e.g. "gd73-06-22.mtx.seamons.ht12.92375.flac16").

You can also use ``-r`` or ``--rename`` to automatically rename the directories.

