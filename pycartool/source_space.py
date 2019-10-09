import numpy as np
import csv
import copy


def _checkcoordinates(coordinates):
    if not isinstance(coordinates, np.ndarray):
        raise TypeError(f'coordinates must be a numpy array')
    if not coordinates.ndim == 2:
        raise ValueError(f'coordinates must have 2 dimension (ndim=2)')
    if not coordinates.shape[1] == 3:
        raise ValueError(f'coordinates must be of shape '
                         f'(n_solutions_points, 3)')
    return (coordinates)


def _checknames(names):
    if not isinstance(names, list):
        raise TypeError(f'names must be a list of string')
    return(names)


def _checksubject(subject):
    if subject is not None:
        if not isinstance(subject, str):
            raise ValueError(f'Subject must be a string but type '
                             f'{type(subject)} was found.')
    return(subject)


def read_spi(filename, subject=None):
    """Create a SourceSpace instance from Cartool spi file.

    Parameters
    ----------
    filename : str
        The spi file to read.
    subject :
        The subject used to create the source space.
    Returns
    -------
    SourceSpace : pycartool.source_space.SourceSpace
        The SourceSpace.
    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        d = list(reader)
        names = [elem[-1] for elem in d]
        coord = [elem[:-1] for elem in d]
        coord = np.array(coord)
        coord = coord.astype(np.float)
        Source_Space = SourceSpace(names, coord,
                                   filename=filename,
                                   subject=subject)
    return(Source_Space)


def write_spi(filename, SourceSpace):
    """Write Cartool spi file.

    Parameters
    ----------
    filename : str
        The spi file to write.
    SourceSpace : pycartool.source_space.SourceSpace
        The SourceSpace to save.
    """
    names = SourceSpace.get_names()
    x, y, z = SourceSpace.get_coordinates().T
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for s in enumerate(zip(x, y, z, names)):
            writer.writerow(s[1])


class SourceSpace(object):
    """Container for source space data.

    Parameters
    ----------
    names : list of str, lenght (n_sources)
        The solutions point names.
    coordinates : ndarray, shape (n_sources, 3)
        The solutions point names coordinates.
    subject : str
        Subject from who the source space was created.
    filename : str
        If loaded from a file, the corresponding filename.

    Attributes
    ----------
    n_sources : int
        Number of sources.
    names : list of str, lenght (n_sources)
        The solutions point names.
    coordinates : ndarray, shape (n_sources, 3)
        The solutions point names coordinates.
    subject : str
        Subject from who the source space was created.
    filename : str
        If loaded from a file, the corresponding filename.

    """
    def __init__(self, names, coordinates, subject=None, filename=None):
        _checkcoordinates(coordinates)
        _checknames(names)
        if not len(names) == coordinates.shape[0]:
            raise ValueError(f'coordinates and names dimesions must match'
                             f' but found {len(names)} names and '
                             f'{coordinates.shape[0]} solution points'
                             f' coordinates')
        else:
            self.n_sources = len(names)

        self.subject = subject
        self.names = names
        self.coordinates = coordinates
        self.filename = filename

    def __repr__(self):
        s = f'{self.n_sources} sources'
        if self.subject is not None:
            s += f', subject : {self.subject}'
        if self.filename is not None:
            s += f', filename : {self.filename}'
        return(f'<SourceSpace | {s}>')

    def get_coordinates(self):
        """Return a copy of sources coordinates."""
        return (copy.deepcopy(self.coordinates))

    def get_names(self):
        """Return a copy of sources names."""
        return(copy.deepcopy(self.names))

    def save(self, filename):
        """Write SourceSpace to Cartool spi file.

        Parameters
        ----------
        filename : str
            The spi file to write.

        """
        write_spi(filename, self)

    def get_center_of_mass(self, method='mean'):
        if method == 'mean':
            center_of_mass = np.mean(self.coordinates, axis=0)
        elif method == 'median':
            center_of_mass = np.median(self.coordinates, axis=0)
        return(center_of_mass)
