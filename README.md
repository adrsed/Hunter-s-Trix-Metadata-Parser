# Hunter's Trix Metadata Parser
Metadata Parser for Hunter's Trix

[Hunter's Trix](https://www.facebook.com/GratefulDeadTrix) is a collection of 
incredible Matrix recordings of a bunch of Grateful Dead shows.
They have one problem however: Volumes 1 through 94 lack metadata in the FLAC
files, adding those manually takes a lot of time, which this script aims to solve.

This is based on an [already existing parser](https://github.com/shacker/trix) 
with some changes:
1. It omits the conversion to ALAC, since I didn't need it
(although I might add conversion to different formats in the future).
2. It only requires metaflac to be installed.
3. Metadata and cover art files don't need to be manually specified, they are
simply found straight out of the torrent directory (They can still be supplied
via the command line).
4. The directory containing the files is supplied via the command line instead of
having to change variables in the file.

Tested on Windows and Linux.

## Usage
### Requirements
You will need to work with the command line (for now), so a tiny bit of
computer magic is required.

The [metaflac](https://xiph.org/flac/documentation_tools_metaflac.html) CLI binary
needs to be installed and working. If you are on Windows, a simple way is to have
the ``metaflac.exe`` in the same directory as ``trix_parser.py``

You can copy ```trix_parser.py``` to some folder in your python path, if you don't
you simply will have to use the full path to the file in step 2.

### Running the parser
1. Torrent a volume of your choosing, the directory name should look something 
like ``gd73-06-22.mtx.seamons.ht12.92375.flac16`` after the download is complete.
2. In a terminal, run ```python trix_parser.py <path to the directory>```. You can use
some options here:
    - -m, --metadata - specifies a metadata file
    - -c, --cover -  specifies a cover art file
   
    If these are not given, the files are located automatically, so they shouldn't
really be necessary.
3. If you have renamed the directory, the volume number can't be automatically
extracted, so you would have to enter it now.
4. Wait.
5. Enjoy.

#### Command Line Options
There are some command line options you can use with the parser:
- ``-m``, ``--metadata`` - Specify a metadata file
- ``-c``, ``--cover`` - Specify a cover file

These two are leftovers from an earlier version that did not automatically
grab those files, I still left them in in case anyone wants to use them.
Both can be specified as full paths or just the filenames.

- ``-a``, ``--artist`` - Specify an artist, default is "Grateful Dead" but e.g.
Vol. 105 is a solo Jerry show
- ``-g``, ``--genre`` - Specify a different genre, default is "Rock"

