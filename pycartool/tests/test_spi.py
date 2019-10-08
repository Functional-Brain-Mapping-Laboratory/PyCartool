# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
import numpy as np
from ..source_space import SourceSpace, read_spi, write_spi

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')


def test_read_spi():
    """Test read_spi"""
    file_path = os.path.join(data_path, 'sample_test_spi.spi')
    Source_space = read_spi(file_path)
    if not len(Source_space.names) == 5006:
        raise AssertionError()
    if not Source_space.coordinates.shape == (5006, 3):
        raise AssertionError()


def test_SourceSpace():
    """Test SourceSpace instance and methods"""
    coordinates = np.random.rand(5000, 3)
    names = [('S' + str(i)) for i in range(0, 5000)]
    Source_space = SourceSpace(names, coordinates)

    new_coordinates = np.random.rand(5000, 3)
    Source_space.coordinates = new_coordinates
    if not (Source_space.coordinates == new_coordinates).all():
        raise AssertionError()

    new_names = [('F' + str(i)) for i in range(0, 5000)]
    Source_space.names = new_names
    if not (Source_space.names == new_names):
        raise AssertionError()

    subject = 'test_subject'
    Source_space.subject = subject
    if not (Source_space.subject == subject):
        raise AssertionError()


def test_write_spi():
    """Test write_spi"""
    filename = os.path.join(data_path, 'sample_test_write_spi.spi')
    coordinates = np.random.rand(5000, 3)
    names = [('S' + str(i)) for i in range(0, 5000)]
    Source_space = SourceSpace(names, coordinates)
    write_spi(filename, Source_space)
    Read_Source_space = read_spi(filename)
    if names != Read_Source_space.names:
        raise AssertionError
    if (coordinates != Read_Source_space.coordinates).any():
        raise AssertionError
