"""Export model outputs module."""

import os

import numpy as np

from .dat_file import DatFile


def check_values(values, df_values, msg):
    """Get value from data file if None or check all equals.

    Parameters
    ----------
    values: any
        None or stored values to compare.
    df_values: any
        Data file values.
    msg: str
        Message to raise if values does not match.

    Returns
    -------
    any
        Data file values.

    Raises
    ------
    ValueError
        If any of the values does not match.

    """
    if values is None:
        return df_values

    if isinstance(df_values, np.ndarray):
        if any(values != df_values):
            raise ValueError(f'{msg} is not consistant with previous pixels.')
    elif values != df_values:
        raise ValueError(f'{msg} is not consistant with previous pixels.')

    return df_values


def extract(img_id, ns, nl, root='', prefix='C', suffix='', ext='dat') -> dict:
    """Extract all output pixels for a cube.

    Parameters
    ----------
    cube: str or pyvims.VIMS
        VIMS cube ID
    ns: int
        Number of samples.
    nl: int
        Number of lines.
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.
    ext: str, optional
        Filename extension.

    Raises
    ------
    ValueError
        If the setup change from one file to the other.
    ValueError
        If the wavelength grid change from one file to the other.

    """
    setup = None
    wvlns = None
    outputs = None
    cube = None
    for s in range(1, ns + 1):
        for l in range(1, nl + 1):
            try:
                df = DatFile(img_id, s, l, root=root, ext=ext,
                             prefix=prefix, suffix=suffix)
            except FileNotFoundError:
                continue

            setup = check_values(setup, df.setup, f'Setup on pixel {s, l}')
            wvlns = check_values(wvlns, df.wvlns, f'Wavelength grid on pixel {s, l}')

            if outputs is None:
                outputs = {key: np.nan * np.zeros((nl, ns)) for key in df.outputs.keys()}

            for key in outputs.keys():
                outputs[key][l - 1, s - 1] = df.outputs[key]

            if cube is None:
                cube = {key: np.nan * np.zeros((len(wvlns), nl, ns))
                        for key in df.data.dtype.names}

            for key in cube.keys():
                cube[key][:, l - 1, s - 1] = df.data[key]

    return {
        'setup': setup,
        'wvlns': wvlns,
        'outputs': outputs,
        'cube': cube,
    }


def save(filename, data):
    """Save dict into a numpy array."""
    np.save(filename, [data])


def load(filename) -> dict:
    """Load dict from a saved numpy array."""
    return np.load(filename, allow_pickle=True)[0]


def npy_filename(img_id, root='', prefix='C', suffix='') -> str:
    """Get numpy fname and filename based on cube inputs.

    Parameters
    ----------
    cube: str or pyvims.VIMS
        VIMS cube ID
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.

    """
    if suffix and not suffix.startswith('_'):
        suffix = '_' + suffix

    fname = f'{prefix}{img_id}{suffix}'
    filename = os.path.join(root, f'{fname}.npy')

    return fname, filename


def export(img_id, ns, nl, root='', prefix='C', suffix='', ext='dat',
           verbose=True, overwrite=False):
    """Extract and save all output files into a single numpy array.

    Parameters
    ----------
    cube: str or pyvims.VIMS
        VIMS cube ID
    ns: int
        Number of samples.
    nl: int
        Number of lines.
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.
    ext: str, optional
        Filename extension.
    verbose: bool, optional
        Enable verbose output.
    overwrite: bool, optional
        Enable numpy file overwrite if it already exists.

    Raises
    ------
    FileExistsError
        If the file already exists and ``overwrite``
        is set to ``False``.

    """
    fname, filename = npy_filename(img_id, root=root,
                                   prefix=prefix, suffix=suffix)

    if os.path.exists(filename) and not overwrite:
        raise FileExistsError(
            f'The file `{fname}` already exists. Add `overwrite=True` to overwrite it.')

    if verbose:
        print(f'Extracting data of {fname}…')

    data = extract(img_id, ns, nl, root=root, prefix=prefix, suffix=suffix, ext=ext)
    save(filename, data)

    if verbose:
        print(f'Data saved in `{filename}`.')
