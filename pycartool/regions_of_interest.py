def read_roi(filename, source_space=None):
    """Read Cartool region of interest (.rois) files.

    Parameters
    ----------
    filename : str
        The roi file to read
    source_space : pycartool.source_space.SourceSpace
        The SourceSpace corresponding to the regions of interest.

    Returns
    -------
    regions_of_interest : pycartool.regions_of_interest.RegionOfInterest
        The regions of interest.

    Note
    -------
    Indices are broadcast to 0 based as expected in Python. In file, indices
    are saved starting from 1 as expected in Cartool.

    """
    with open(filename) as f:
        Roi_type = f.readline().strip()
        if Roi_type != 'RO01':
            print(f'{Roi_type} format not supported')
            raise ValueError
        print(Roi_type)
        n_orig = int(f.readline().strip())
        print(f'Dimension_of_original_data: {n_orig}')
        n_roi = int(f.readline().strip())
        print(f'Number of ROI: {n_roi}')
        rois_name = []
        rois_elements = []
        for _ in range(0, n_roi):
            roi_name = f.readline().strip()
            roi_elem = f.readline().split(' ')[:-1]
            # Use python 0base indices instead of Cartool 1 based indices
            roi_elem = [int(elem) - 1 for elem in roi_elem]
            rois_name.append(roi_name)
            rois_elements.append(roi_elem)
    if source_space is not None:
        if n_orig != source_space.n_sources:
            raise ValueError(f'Dimension of original data for roi file data is'
                             f' {n_orig}, but source space contains '
                             f'{source_space.n_sources} sources.')
    regions_of_interest = RegionsOfInterest(rois_name, rois_elements,
                                            source_space=source_space,
                                            filename=filename)
    return(regions_of_interest)


def _check_groups_of_indexes(groups_of_indexes):
    if not isinstance(groups_of_indexes, list):
        raise TypeError(f'groups_of_indexes must be a list of list')
    for e, elem in enumerate(groups_of_indexes):
        if not isinstance(elem, list):
            raise TypeError(f'groups_of_indexes must be a list of list but'
                            f' the {e} element is a {type(elem)}')


def _compute_number_of_sources(groups_of_indexes):
    groups_of_indexes_max = [max(elem) for elem in groups_of_indexes]
    maximum = max(groups_of_indexes_max)
    return(maximum)


class RegionsOfInterest():
    def __init__(self, names, groups_of_indexes,
                 source_space=None, filename=None):
        _check_groups_of_indexes(groups_of_indexes)
        max = _compute_number_of_sources(groups_of_indexes)
        # Check that groups_of_indexes correspond to source space.
        if source_space is not None:
            if not isinstance(source_space, Sourcespace):
                raise TypeError(f'sourcespace must be an instance'
                                f' of SourceSpace.')
            if source_space.n_sources < max:
                raise ValueError(f'Indice {max} found in groups_of_indexes but'
                                 f' SourceSpace contain only'
                                 f' {source_space.n_sources} sources.')

        self.names = names
        self.groups_of_indexes = groups_of_indexes
        self.source_space = source_space
        self.filename = filename

    def __repr__(self):
        s = f'{len(self.names)} Rois'
        if self.filename is not None:
            s += f', filename : {self.filename}'
        return(f'<RegionsOfInterest | {s}>')
