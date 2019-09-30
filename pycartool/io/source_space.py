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
        solution_points = {'names': names,
                           'coordinates' = coord}

    return(solution_points)


def write_spi(filename, solution_points):
    """Write Cartool spi file.

    Parameters
    ----------
    filename : str
        The spi file to write.
    solution_points : dict of str
        The solution points info. Keys are:
            names : list of str
                the solutions point names.
            coordinates : np.array, shape (n_solutions_points, 3)
                the x,y,z coordinates of each solution point.
    """
    names = solution_points['names']
    x, y, z = solution_points['coordinates']
    with open(filename) as f:
        writer = csv.writer(f, delimiter='\t')
        for i in range(0, len(names)):
            writer.writerow([name[i], x[i], y[i], z[i]])
