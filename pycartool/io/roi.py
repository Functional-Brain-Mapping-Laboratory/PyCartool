# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import csv
import numpy as np


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

    """
    with open(filename) as f:
        RO = f.readline().strip()
        if RO != "RO01":
            print(f"{RO} format not supported")
            raise ValueError
        print(RO)
        n_orig = int(f.readline().strip())
        print(f"Dimension_of_original_data: {n_orig}")
        n_roi = int(f.readline().strip())
        print(f"Number of ROI: {n_roi}")
        rois = []
        for i in range(0, n_roi):
            roi_name = f.readline().strip()
            roi_elem = f.readline().split(" ")[:-1]
            rois.append([roi_name, roi_elem])
        return(rois)
