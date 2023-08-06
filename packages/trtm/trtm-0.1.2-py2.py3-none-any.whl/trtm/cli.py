"""Command Line Interface."""

import argparse
import os

from .scan import scan_cubes
from .export import export


def cli(argv=None):
    """Scan and export TRTM data file to numpy file."""
    parser = argparse.ArgumentParser(
        description='Scan and export TRTM data file to numpy file.')

    parser.add_argument('cubes', nargs='*', help='Input cube id(s).', metavar='CUBE_ID')
    parser.add_argument('-f', '--folder', default='', metavar='PATH/TO/OUTOUT/DATA',
                        help='Data folder location. Default: current directory')
    parser.add_argument('-s', '--suffix', default='', help='Data suffix.')
    parser.add_argument('-e', '--ext', default='_SFCPARMS.dat',
                        help='File extension.  Default: `_SFCPARMS.dat`')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet output')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        default=False, help='Enable overwrite if the file exists.')

    argv = argv if argv is not None else os.sys.argv[1:]

    args, _ = parser.parse_known_args(argv)

    ext = (args.suffix + args.ext) if args.suffix else args.ext

    cubes = scan_cubes(folder=args.folder, ext=ext, cubes=args.cubes)

    cubes_processed = []
    if cubes:
        for cube in cubes.values():
            try:
                export(cube['img_id'], cube['NS'], cube['NL'], root=args.folder,
                       prefix=cube['prefix'], suffix=cube['suffix'],
                       verbose=(not args.quiet), overwrite=args.overwrite)

                cubes_processed.append(cube['img_id'])

            except FileExistsError as err:
                print(f'[Skipped] {str(err).split(".")[0]}.')
    else:
        print('No output data files found in '
              + ("the local directory." if args.folder is None else f'`{args.folder}`.'))

    return cubes_processed if args.quiet else None
