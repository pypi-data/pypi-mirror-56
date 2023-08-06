"""Cassini VIMS toolbox."""

import re


def img_id(cube: str) -> str:
    """Parse cube id.

    Parameters
    ----------
    cube: str or pyvims.VIMS
        Filename or VIMS object.

    Raises
    ------
    ValueError
        If the provided VIMS cube id is invalid.

    """
    img_id = re.findall(r'\d{10}_\d+(?:_0\d+)?', str(cube))

    if not img_id:
        raise ValueError(f'Cube `{cube}` name does not match '
                         'the correct VIMS cube pattern.')

    return img_id[0]
