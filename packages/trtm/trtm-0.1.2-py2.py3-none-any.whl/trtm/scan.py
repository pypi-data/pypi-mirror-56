"""Search tools module."""

import os
import re

from .vims import img_id


FILENAME = re.compile(r'[/\\]?(\w)?(\d{10}_\d+(?:_0\d+)?)_(\d+)-(\d+)(_[\w_\-]+)?\.\w')


def parse_filename(fname, omit='_SFCPARMS') -> dict:
    """Parse file name.

    Parameters
    ----------
    fname: str
        Filename to parse.
    omit: str, optional
        Omit a part of the suffix.

    """
    attrs = FILENAME.findall(fname)
    return None if not attrs else {
        'img_id': attrs[0][1],
        'pixel': (int(attrs[0][2]), int(attrs[0][3])),
        'prefix': attrs[0][0],
        'suffix': attrs[0][4].replace(omit, ''),
    }


def scan_folder(folder='', ext='_SFCPARMS.dat') -> list:
    """Scan folder to files ending with a known extension.

    Parameters
    ----------
    folder: str, optional
        Location of the folder to scan. Use local directory by default.
    ext: str, optional
        Expected file extension.

    """
    return sorted([f for f in os.listdir(folder if folder else None) if f.endswith(ext)])


def scan_files(folder=None, ext='_SFCPARMS.dat') -> list:
    """Scan folder to get data list.

    Parameters
    ----------
    folder: str, optional
        Location of the folder to scan. Use local directory by default.
    ext: str, optional
        Expected file extension.

    """
    return {f: attrs for f in scan_folder(folder=folder, ext=ext)
            for attrs in [parse_filename(f)] if attrs}


def scan_cubes(folder=None, ext='_SFCPARMS.dat', cubes=None) -> list:
    """Scan folder to get all the available cubes.

    Parameters
    ----------
    folder: str, optional
        Location of the folder to scan. Use local directory by default.
    ext: str, optional
        Expected file extension.
    cubes: str or list, optional
        Cube(s) ID.

    """
    list_cubes = False if not cubes else \
        [img_id(cubes)] if isinstance(cubes, str) else \
        [img_id(cube) for cube in cubes]

    cubes = {}
    for f in scan_files(folder=folder, ext=ext).values():
        if list_cubes and f['img_id'] not in list_cubes:  # pylint: disable=E1135
            continue

        fname = f'{f["prefix"]}{f["img_id"]}{f["suffix"]}'
        if fname not in cubes:
            cubes[fname] = {
                'img_id': f['img_id'],
                'NS': f['pixel'][0],
                'NL': f['pixel'][1],
                'prefix': f['prefix'],
                'suffix': f['suffix'],
            }
        else:
            if cubes[fname]['NS'] < f['pixel'][0]:
                cubes[fname]['NS'] = f['pixel'][0]

            if cubes[fname]['NL'] < f['pixel'][1]:
                cubes[fname]['NL'] = f['pixel'][1]

    return cubes
