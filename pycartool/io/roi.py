# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)


def read_roi(filename):
    """Read Cartool region of interest (.rois) files.

    Parameters
    ----------
    filename : str
        The roi file to read

    Returns
    -------
    Rois : dict of str
        The Rois info info. Keys are:
            names : list of str
                the rois names.
            elements :list of int
                the indices of elements belonging to each rois (indice start to 1).

    Warning
    -------
    Indexes start from 1, not 0 as Cartools does. When using
    with combination of source space, you way need to tranform
    to 0 base indices.

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
            rois_name.append(roi_name)
            rois_elements.append(roi_elem)
        Rois = {'names': rois_name,
                'elements': rois_elements}
        return(Rois)
