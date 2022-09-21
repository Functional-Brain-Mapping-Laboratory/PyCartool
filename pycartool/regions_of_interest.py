# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
from .source_space import SourceSpace
from .utils._logs import logger, verbose


@verbose
def read_roi(filename, source_space=None, verbose=None):
    """Read Cartool region of interest (.rois) files.

    Parameters
    ----------
    filename : str or file-like
        The Regions Of Interest (.roi) file to read.

    source_space : pycartool.source_space.SourceSpace
        The SourceSpace corresponding to the regions of interest.

    Returns
    -------
    regions_of_interest : pycartool.regions_of_interest.RegionsOfInterest
        The regions of interest.

    Note
    -------
    Indices are broadcast to 0 based as expected in Python. In file, indices
    are saved starting from 1 as expected in Cartool.

    """
    with open(filename) as f:
        Roi_type = f.readline().strip()
        if Roi_type != "RO01":
            raise ValueError(f"{Roi_type} format not supported")
        logger.info(Roi_type)
        n_orig = int(f.readline().strip())
        logger.info(f"Dimension_of_original_data: {n_orig}")
        n_roi = int(f.readline().strip())
        logger.info(f"Number of ROI: {n_roi}")
        rois_name = []
        rois_elements = []
        for _ in range(0, n_roi):
            roi_name = f.readline().strip()
            roi_elem = f.readline().split(" ")[:-1]
            # Use python 0base indices instead of Cartool 1 based indices
            roi_elem = [int(elem) - 1 for elem in roi_elem]
            rois_name.append(roi_name)
            rois_elements.append(roi_elem)
    if source_space is not None:
        if n_orig != source_space.n_sources:
            raise ValueError(
                f"Dimension of original data for roi file data is"
                f" {n_orig}, but source space contains "
                f"{source_space.n_sources} sources."
            )
    regions_of_interest = RegionsOfInterest(
        rois_name, rois_elements, source_space=source_space, filename=filename
    )
    return regions_of_interest


def _check_groups_of_indexes(groups_of_indexes):
    if not isinstance(groups_of_indexes, list):
        raise TypeError(f"groups_of_indexes must be a list of list")
    for e, elem in enumerate(groups_of_indexes):
        if not isinstance(elem, list):
            raise TypeError(
                f"groups_of_indexes must be a list of list but"
                f" the {e} element is a {type(elem)}"
            )


def _compute_number_of_sources(groups_of_indexes):
    groups_of_indexes_max = [max(elem) for elem in groups_of_indexes]
    maximum = max(groups_of_indexes_max)
    return maximum


class RegionsOfInterest(object):
    """Container for regions of interest.

    Parameters
    ----------
    names : :obj:`list` of :obj:`str`
        The regions of interest names.
    groups_of_indexes : :obj:`list` of :obj:`list` of :obj:`int`
        The sources indices belonging to each region of interest.
    source_space : pycartool.source_space.SourceSpace
        The source space associated to the regions of interest.
    filename : str or file-like
        The Regions Of Interest file (.roi) from which
        the data has been extracted.

    Attributes
    ----------
    names : :obj:`list` of :obj:`str`
        The regions of interest names.
    groups_of_indexes : :obj:`list` of :obj:`list` of :obj:`int`
        The sources indices belonging to each region of interest.
    source_space : pycartool.source_space.SourceSpace
        The source space associated to the regions of interest.
    filename : str or file-like
        The Regions Of Interest file (.roi) from which
        the data has been extracted.

    """

    def __init__(
        self, names, groups_of_indexes, source_space=None, filename=None
    ):
        _check_groups_of_indexes(groups_of_indexes)
        maximum = _compute_number_of_sources(groups_of_indexes)
        # Check that groups_of_indexes correspond to source space.
        if source_space is not None:
            if not isinstance(source_space, SourceSpace):
                raise TypeError(
                    f"sourcespace must be an instance" f" of SourceSpace."
                )
            if source_space.n_sources < maximum:
                raise ValueError(
                    f"Indice {maximum} found in groups_of_indexes"
                    f" but SourceSpace contains only"
                    f" {source_space.n_sources} sources."
                )

        self.names = names
        self.groups_of_indexes = groups_of_indexes
        self.source_space = source_space
        self.filename = filename

    def __repr__(self):  # noqa: D401
        """String representation."""
        s = f"{len(self.names)} Rois"
        if self.filename is not None:
            s += f", filename : {self.filename}"
        return f"<RegionsOfInterest or {s}>"
