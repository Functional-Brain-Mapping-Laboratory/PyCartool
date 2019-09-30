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
    rois : list, shape(n_roi, 2)
        A list of ROIs which each element is a list [roi name, elements]

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
        rois = []
        for _ in range(0, n_roi):
            roi_name = f.readline().strip()
            roi_elem = f.readline().split(' ')[:-1]
            rois.append([roi_name, roi_elem])
        return(rois)
