"""Titan radiative transfer model output data file module."""

import os
import re

import numpy as np

from .vims import img_id


def filename(img_id, s: int, l: int, root='', prefix='C', suffix='', ext='dat') -> str:
    """Radiative transfer output data filename.

    The function also check if the file exists.

    Parameters
    ----------
    img_id: str
        VIMS cube ID
    s: int
        Pixel sample (1 to NS).
    l: int
        Pixel line (1 to NL).
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.
    ext: str, optional
        Filename extension.

    Returns
    -------
    str
        Radiative transfer output filename.

    Raises
    ------
    FileNotFoundError
        If the file does not exists.

    """
    if suffix and not suffix.startswith('_'):
        suffix = '_' + suffix

    fname = os.path.join(root, f'{prefix}{img_id}_{s}-{l}{suffix}.{ext}')

    if not os.path.exists(fname):
        raise FileNotFoundError(f'{fname} not found.')

    return fname


def _parse(value):
    """Parse header value."""
    if ' ' in value.strip():
        return [_parse(v) for v in value.split()]
    if '.' in value:
        return float(value)
    if re.match(r'^\d+$', value):
        return int(value)
    if value == 'T':
        return True
    if value == 'F':
        return False
    return value.strip()


class DatFile:
    """RT output data file.

    Parameters
    ----------
    cube: str or pyvims.VIMS
        VIMS cube ID
    s: int
        Pixel sample(1 to NS).
    l: int
        Pixel line(1 to NL).
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.
    ext: str, optional
        Filename extension.

    """

    KEY_VALUE = re.compile(r'#\s([\w\(\)\:\,\s\=]*)\-+:\s*(.*)')

    OUTPUTS = ['SOLARFLUX', 'FH', 'FC', 'X2']
    SKIP = ['phase', 'emi', 'inc', 'SOLARMU', 'MUOUT', 'PHIOUT']

    I_F = ['wavelength', 'I_F', 'I_F_diff']
    ALBEDO = ['wavelength', 'albedo_corr', 'albedo_end', 'sfcparms',
              'albedo_surf', 'fhsuralb_err', 'albedo_err', 'total_err']

    def __init__(self, cube, s: int, l: int, root='', prefix='C', suffix='', ext='dat'):
        self.img_id = img_id(cube)
        self.s, self.l = s, l
        self.root = root

        self.f_i_f = filename(self.img_id, s, l, root=root,
                              prefix=prefix, suffix=suffix, ext=ext)
        self.f_alb = filename(self.img_id, s, l, root=root,
                              prefix=prefix, suffix=(suffix + '_SFCPARMS'), ext=ext)

        self.__header = None
        self.__i_f = None
        self.__alb = None

    def __str__(self):
        return f'{self.img_id}-S{self.s}-L{self.l}'

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __getitem__(self, item):
        if item in self.I_F:
            return self.i_f[item]

        if item in self.ALBEDO:
            return self.albedo[item]

        if item in self.header:
            return self.header[item]

        raise KeyError(f'Item: `{item}` unknown.')

    @property
    def header(self) -> dict:
        """Get I/F file header."""
        if self.__header is None:
            with open(self.f_i_f, 'r') as f:
                lines = f.readlines()

            self.__header = {key.strip(): _parse(value) for line in lines
                             if '#' in line and '-:' in line
                             for key, value in self.KEY_VALUE.findall(line)}
        return self.__header

    @property
    def outputs(self) -> dict:
        """Pixel outputs from I/F file header."""
        return {key: self.header[key] for key in self.OUTPUTS}

    @property
    def setup(self) -> dict:
        """Radiative transfer setup from I/F file header."""
        return {key: self.header[key] for key in self.header.keys()
                if key not in self.OUTPUTS and key not in self.SKIP}

    @staticmethod
    def _load_data(fname, header: list, dtype=float) -> np.ndarray:
        """Load file data.

        Parameters
        ----------
        header: list
            Header key list.
        dtype: type
            Data type.

        Returns
        -------
        numpy.array
            Formatted data array.

        See Also
        --------
        :py:func:`fname`

        """
        with open(fname, 'r') as f:
            lines = f.readlines()

        ncols = len(header)
        data = [tuple(line.split()[:ncols]) for line in lines if '#' not in line]

        return np.array(data, dtype={'names': header, 'formats': ncols * [dtype]})

    @property
    def i_f(self) -> np.ndarray:
        """I/F data from output file."""
        if self.__i_f is None:
            self.__i_f = self._load_data(self.f_i_f, header=self.I_F)
        return self.__i_f

    @property
    def albedo(self) -> np.ndarray:
        """Albedo data from output file."""
        if self.__alb is None:
            self.__alb = self._load_data(self.f_alb, header=self.ALBEDO)
        return self.__alb

    @property
    def wvlns(self) -> np.ndarray:
        """Wavelength grid."""
        if any(self.i_f['wavelength'] != self.albedo['wavelength']):
            raise ValueError(
                'Wavelength grid is not the same between I/F and the albedo files.')
        return self.i_f['wavelength'] * 1e6

    @property
    def data(self) -> np.ndarray:
        """I/F and albedo content for a single pixel."""
        names = self.I_F[1:] + self.ALBEDO[1:]
        return np.array([
            tuple(row) for row in np.transpose([
                self.i_f[key] for key in self.I_F[1:]
            ] + [
                self.albedo[key] for key in self.ALBEDO[1:]
            ])], dtype={'names': names, 'formats': len(names) * [float]})
