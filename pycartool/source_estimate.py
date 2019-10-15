# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import struct
import numpy as np
from .source_space import write_spi, SourceSpace


def _check_method(method):
    if method not in ['svd', 'mean', 'median']:
        raise ValueError('Method must be either svd, mean, or median')


def _check_sources_tc(sources_tc):
    if not isinstance(sources_tc, np.ndarray):
        raise TypeError(f'sources_tc must be an instance of numpy.ndarray')
    if sources_tc.ndim != 3:
        raise ValueError(f'sources_tc must be of shape'
                         f'(n_solutionpoints, n_dim, n_timeframes)')
    if sources_tc.shape[1] not in [1, 3]:
        raise ValueError(f'sources_tc.shape[1] must be either 1 ( scalar) '
                         f'or 3 (vectorial)')
    return(sources_tc)


def read_ris(filename, source_space=None, subject=None):
    """Read Cartool Results of Inverse Solution computation (.ris) file.

    Parameters
    ----------
    filename : str
        the ris file to read.
    source_space : pycartool.source_space.SourceSpace
        The SourceSpace corresponding to the source estimate.
    subject : str
        The subject used to create the source estimate.
    Returns
    -------
    source_estimate : pycartool.source_estimate.source_estimate
        The SourceEstimate extracted from ris file.
    """
    with open(filename, 'rb') as f:
        print(f'Reading {filename}')
        print(f'Reading Header...')
        ris_type = [struct.unpack('c', f.read(1))[0].decode('utf-8')
                    for i in range(4)]
        ris_type = ''.join(ris_type)
        if ris_type not in ["RI01"]:
            raise ValueError(f'{ris_type} : Invalid RI type, please check that'
                             f' input file is a Result of Inverse Solution '
                             f' computation')
        print(f'IS type: {ris_type}')
        n_solutionpoints = struct.unpack('I', f.read(4))[0]
        print(f'n_solutionpoints: {n_solutionpoints}')
        n_timeframes = struct.unpack('I', f.read(4))[0]
        print(f'n_timeframes: {n_timeframes}')
        s_freq = struct.unpack('f', f.read(4))[0]
        print(f'Samplimg frequency: {s_freq}')
        isinversescalar = struct.unpack('c', f.read(1))[0]
        if isinversescalar == '0':
            n_dim = 1
            print(f'Result of Inverse Solution computation is Scalar')
        else:
            print(f'Result of Inverse Solution computation is Vectorial')
            n_dim = 3

        buf = f.read(n_dim * n_solutionpoints * n_timeframes * 4)
        data = np.frombuffer(buf, dtype=np.float32)
        data = data.reshape(n_timeframes, n_dim, n_solutionpoints)
        source_estimate = SourceEstimate(data.T, s_freq,
                                         source_space=source_space,
                                         subject=subject,
                                         filename=filename)
        return(source_estimate)


def write_ris(source_estimate, filename):
    """Write SourceEstimate instance to file.

    Parameters
    ----------
    filename : str
        filename of the exported inverse solution computation.
    source_estimate : pycartool.source_estimate.source_estimate
        The SourceEstimate to save as a ris file.
    """
    data = source_estimate.sources_tc.T
    sfreq = source_estimate.sfreq
    if not isinstance(data, np.ndarray):
        raise TypeError('Input data must be a ndarray')
    if data.ndim != 3:
        raise ValueError('Input data must be a 3D array')
    if data.shape[1] == 1:
        isinversescalar = '0'
    elif data.shape[1] == 3:
        isinversescalar = '1'
    else:
        raise ValueError('Input data must have shape (_,1,_) (scalar)'
                         ' or (_,3,_) (vectorial)')
    ris_type = 'RI01'
    n_timeframes = data.shape[0]
    n_solutionpoints = data.shape[2]
    f = open(filename, 'wb')
    f.write(ris_type.encode('utf-8'))
    f.write(struct.pack('I', n_solutionpoints))
    f.write(struct.pack('I', n_timeframes))
    f.write(struct.pack('f', sfreq))
    f.write(isinversescalar.encode('utf-8'))
    data = data.astype(np.float32)
    data.tofile(f)
    f.close()


class SourceEstimate(object):
    """Container for source estimate data.

    Parameters
    ----------
    sources_tc : numpy.ndarray, shape (n_solutionpoints, n_dim, n_timeframes)
        The sources time courses. Can be either scalar (ndim=1) or
         vectorial (ndim=3).
    sfreq : float
        The sampling frequency.
    source_space : pycartool.source_space.SourceSpace
        The SourceSpace corresponding to the source estimate.
    subject : str
        The subject used to create the source estimate.
    filename : str
        filename from wich the source estimate was imported.

    Attributes
    ----------
    is_scalar : bool
        True if estimate is scalar, False is estimate is vectorial.
    n_sources : int
        Number of sources.
    sources_tc : numpy.ndarray, shape (n_solutionpoints, n_dim, n_timeframes)
        The sources time courses. Can be either scalar (ndim=1) or
         vectorial (ndim=3).
    source_space : pycartool.source_space.SourceSpace
        The SourceSpace corresponding to the source estimate.
    subject : str
        The subject used to create the source estimate.
    filename : str
        filename from wich the source estimate was imported.

    """

    def __init__(self, sources_tc, sfreq,
                 source_space=None, subject=None, filename=None):
        _check_sources_tc(sources_tc)
        # Check that source estimate correspond to source space
        if source_space is not None:
            if not isinstance(source_space, SourceSpace):
                raise TypeError(f'sourcespace must be an instance'
                                f' of SourceSpace.')
            if not len(source_space.names) == sources_tc.shape[0]:
                raise ValueError(f'Expect {len(source_space.names)} time '
                                 f' courses from Source space, but found only '
                                 f'{sources_tc.shape[0]} in sources_tc')
        if sources_tc.shape[1] == 1:
            self.is_scalar = True
        elif sources_tc.shape[1] == 3:
            self.is_scalar = False

        self.n_sources = sources_tc.shape[0]
        self.sources_tc = sources_tc
        self.source_space = source_space
        self.sfreq = sfreq
        self.subject = subject
        self.filename = filename

    def __repr__(self):
        if self.is_scalar is True:
            s = f'Scalar, '
        else:
            s = f'Vectorial, '
        s += f'{self.n_sources} sources, sfreq : {self.sfreq}'

        if self.subject is not None:
            s += f', subject : {self.subject}'
        if self.filename is not None:
            s += f', filename : {self.filename}'
        return(f'<SourceEstimate | {s}>')

    def save(self, filename, export_spi=False):
        """Write SourceEstimate to Cartool ris file.

        Parameters
        ----------
        filename : str
            The ris file to write.
        export_spi : bool
            If True, also export the corresponding source space as ris file.
        """
        write_ris(self, filename)
        if export_spi is True:
            if self.source_space is not None:
                write_spi(filename[:-3] + '.spi', self)
            else:
                raise ValueError('Cannot save source space to file, source '
                                 'space is not defined')

    def per_roi(self, region_of_interest):
        """Short summary.

        Parameters
        ----------
        region_of_interest : pycartool.region_of_interest.RegionOfInterest
            The region of interest used to split the source estimate.

        Returns
        -------
        rois_source_estimate : list of pycartool.source_estimate.SourceEstimate
            A list of Source estimate instance restricted to a Region of
            interest

        """
        # Check is SourceSpace are the equals.
        if self.source_space is None:
            raise ValueError('Source spaces must be defined')
        if region_of_interest.source_space is None:
            raise ValueError('Source spaces must be defined')
        if self.source_space != region_of_interest.source_space:
            raise ValueError('Source estimate and Regions of interest must '
                             'share the same source space')

        rois_source_estimate = []
        rois_names = region_of_interest.names
        for r, _ in enumerate(rois_names):
            indices = region_of_interest.groups_of_indexes[r]
            roi_sources_tc = self.sources_tc[indices, :, :]
            roi_sources_pos = self.source_space.coordinates[indices]
            roi_sources_names = [self.source_space.names[i] for i in indices]
            source_space = SourceSpace(roi_sources_names, roi_sources_pos)
            source_estimate = SourceEstimate(roi_sources_tc, self.sfreq,
                                             source_space=source_space,
                                             subject=self.subject,
                                             filename=None)
            rois_source_estimate.append(source_estimate)
        return(rois_source_estimate)

    def compute_tc(self, method='svd'):
        """Short summary.

        Parameters
        ----------
        method : str
            the method use to compute the time course. Can be either 'mean',
            'median' or 'svd'. Default to 'svd'.

        Returns
        -------
        tc : np.ndarray, shape(n_dim, n_times)
            The global source estimate time course. Can be either Vectorial or
             Scalar depending of the source estimate and the method.

        """
        _check_method(method)
        if method == 'median':
            tc = np.median(self.sources_tc, axis=0)
        elif method == 'mean':
            tc = np.mean(self.sources_tc, axis=0)
        elif method == 'svd':
            n_times = self.sources_tc.shape[-1]
            sources_tc_flat = self.sources_tc.reshape(-1, n_times)
            U, s, V = np.linalg.svd(sources_tc_flat, full_matrices=False)
            scale = np.linalg.norm(s) / np.sqrt(len(sources_tc_flat))
            tc = np.array([scale * V[0]])
            pos = self.source_space.new_coordinates
            pos_flat = self.sources_tc.reshape(-1)
            v = np.multiply(U[:, 0], pos_flat).reshape(-1, 3).mean(axis=0)
            v = v/np.linalg.norm(v)
            print(v)
        return(tc)

    def compute_rois_tc(self, region_of_interest, method='svd'):
        """Short summary.

        Parameters
        ----------
        region_of_interest : pycartool.region_of_interest.RegionOfInterest
            The region of interest used to split the source estimate.
        method : str
            the method use to compute the time course. Can be either 'mean',
            'median' or 'svd'. Default to 'svd'.

        Returns
        -------
        Roi_source_estimate : pycartool.source_space.SourceEstimate
            A source estimate instance where each source correspond to a region
            of interest.

        """
        rois_names = region_of_interest.names
        rois_estimates = self.per_roi(region_of_interest)
        rois_tc = np.array([roi.compute_tc() for roi in rois_estimates])
        rois_coordinates = np.array([estimate.source_space.get_center_of_mass()
                                     for estimate in rois_estimates])
        Roi_source_space = SourceSpace(rois_names, rois_coordinates)
        Roi_source_estimate = SourceEstimate(rois_tc, self.sfreq,
                                             source_space=Roi_source_space)
        return(Roi_source_estimate)
