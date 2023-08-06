"""Titan radiative transfer model output data module."""

import os

import numpy as np

from .export import export, load, npy_filename
from .scan import scan_cubes
from .vims import img_id


class TRTM:
    """Titan radiative transfer model output data object.

    Parameters
    ----------
    img_id: str or pyvims.VIMS
        VIMS cube ID
    root: str, optional
        Data root folder location.
        Default is the current working directory.
    prefix: str, optional
        Filename prefix.
    suffix: str, optional
        Filename suffix.

    """

    def __init__(self, cube, root='', prefix='C', suffix='', create=True):
        self.img_id = img_id(cube)
        self.root = root
        self.prefix = prefix
        self.suffix = suffix

        self.fname, self.filename = npy_filename(self.img_id, root=root,
                                                 prefix=prefix, suffix=suffix)

        self.is_file(create)
        self.__data = None
        self.__keys = None
        self.__size = None

    def __str__(self):
        return f'{self.fname}'

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __contains__(self, key):
        return key in self.keys()

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) == 2:
                item, wvln = item
                return self.get_wvln(self[item], wvln)

            if len(item) == 3:
                item, s, l = item
                return self.get_pixel(self[item], s, l)

            if len(item) == 4:
                item, s, l, wvln = item
                return self.get_pixel(self.get_wvln(self[item], wvln), s, l)

        if item in self:
            if item in self.data:
                return self.data[item]

            for key in self.data.keys():
                if isinstance(self.data[key], dict) and item in self.data[key]:
                    return self.data[key][item]

        raise KeyError(f'Key: `{item}` is not available. ')

    def is_file(self, create):
        """Check if numpy file exists and create it if necessary."""
        if not os.path.exists(self.filename):
            if create:
                cubes = scan_cubes(folder=self.root, cubes=self.img_id)
                if cubes:
                    cube = list(cubes.values())[0]
                    export(cube['img_id'], cube['NS'], cube['NL'], root=self.root,
                           prefix=cube['prefix'], suffix=cube['suffix'])

            else:
                raise FileNotFoundError(
                    f'File `{self.filename}` does not exists. '
                    f'Run `trtm_export` in `{self.root}` folder to export '
                    'the data in numpy format.')

    @property
    def data(self):
        """Data content dictionnary."""
        if self.__data is None:
            self.__data = load(self.filename)
        return self.__data

    def keys(self):
        """List of keys availables."""
        if self.__keys is None:
            keys = []
            for key in self.data.keys():
                if isinstance(self.data[key], dict):
                    keys += self.data[key].keys()

            self.__keys = list(self.data.keys()) + keys

        return self.__keys

    @property
    def size(self):
        """Cube size (NB, NL, NS)."""
        if self.__size is None:
            self.__size = self.data['cube']['I_F'].shape
        return self.__size

    @property
    def ns(self):
        """Number of samples."""
        return self.size[2]

    @property
    def nl(self):
        """Number of lines."""
        return self.size[1]

    @property
    def wvlns(self):
        """Wavelength grid."""
        return self.data['wvlns']

    def index_wvln(self, wvln) -> int:
        """Get wavelength index."""
        self.check_wvln(wvln)
        return np.argmin(np.abs(wvln - self.wvlns))

    def check_wvln(self, wvln):
        """Check is wavelength is in a acceptable range."""
        if wvln < self.wvlns.min():
            raise ValueError(
                f'Wavelength `{wvln}` must be larger than {self.wvlns.min()}.')

        if wvln > self.wvlns.max():
            raise ValueError(
                f'Wavelength `{wvln}` must be smaller than {self.wvlns.max()}.')

    def check_pixel(self, s, l):
        """Check is pixel is in a acceptable range."""
        if s < 1:
            raise ValueError(
                f'Pixel sample `{s}` must be larger or equal to 1.')

        if s > self.ns:
            raise ValueError(
                f'Pixel sample `{s}` must be smaller or equal to {self.ns}.')

        if l < 1:
            raise ValueError(
                f'Pixel line `{l}` must be larger or equal to 1.')

        if l > self.nl:
            raise ValueError(
                f'Pixel line `{l}` must be smaller or equal to {self.nl}.')

    def get_wvln(self, data, wvln):
        """Data for a specific wavelength.

        Parameters
        ----------
        data: numpy.ndarray
            Input data array.
        s: float
            Wavelength value.

        Raises
        ------
        ValueError
            If the provided array is not 3D.

        """
        if np.ndim(data) != 3:
            raise ValueError('Wavelength query can only be achieved on 3D data array.')

        if isinstance(wvln, slice):
            start = self.index_wvln(wvln.start) if wvln.start else None
            stop = (self.index_wvln(wvln.stop) + 1) if wvln.stop else None
            return np.mean(data[slice(start, stop), :, :], axis=0)

        return data[self.index_wvln(wvln), :, :]

    def get_pixel(self, data, s, l):
        """Data for a specific pixel.

        Parameters
        ----------
        data: numpy.ndarray
            Input data array.
        s: int
            Sample index (1-NS).
        l: int
            Line index (1-NL).

        Raises
        ------
        ValueError
            If the provided array is not 2D or 3D.

        """
        self.check_pixel(s, l)

        if np.ndim(data) == 2:
            return data[int(l) - 1, int(s) - 1]

        if np.ndim(data) == 3:
            return data[:, int(l) - 1, int(s) - 1]

        raise ValueError('Pixel query can only be achieved on 2D/3D data array.')
