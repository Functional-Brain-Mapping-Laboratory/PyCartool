# -*- coding: utf-8 -*-
# Authors: Tanguy Vivier <tanguy.viv@gmail.com>
#          Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import csv
import numpy as np


def read_spi(filename):
    """Read Cartool spi file.

    Parameters
    ----------
    filename : str
        The spi file to read.

    Returns
    -------
    coord : ndarray, shape (n_sources, 3)
        the source coordinates.
    names : list, shape (n_sources)

    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        d = list(reader)
        names = [elem[-1] for elem in d]
        coord = [elem[:-1] for elem in d]
        coord = np.array(coord)
        coord = coord.astype(np.float)
    return(coord, names)
