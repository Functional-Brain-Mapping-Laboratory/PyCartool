# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
import numpy as np
from ..io.source_space import read_spi, write_spi

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')


def test_read_spi():
    """Test read_spi"""
    file_path = os.path.join(data_path, 'sample_test_spi.spi')
    solution_points = read_spi(file_path)
    if not len(solution_points['names']) == 5006:
        raise AssertionError()
    if not solution_points['coordinates'].shape[0] == 5006:
        raise AssertionError()


def test_write_spi():
    """Test write_spi"""
    filename = os.path.join(data_path, 'sample_test_write_spi.spi')
    coordinates = np.random.rand(5000, 3)
    names = [('S' + str(i)) for i in range(0, 5000)]
    write_solution_points = {'names': names,
                             'coordinates': coordinates}
    write_spi(filename, write_solution_points)
    read_solution_points = read_spi(filename)
    if names != read_solution_points['names']:
        raise AssertionError
    if (coordinates != read_solution_points['coordinates']).any():
        raise AssertionError
