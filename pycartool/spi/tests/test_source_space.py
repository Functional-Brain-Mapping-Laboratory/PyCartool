# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import os

import numpy as np

from ...data import data_path
from ..source_space import SourceSpace, read_spi, write_spi


def test_read_spi():
    """Test read_spi"""
    file_path = os.path.join(data_path, "sample_test_spi.spi")
    Source_space = read_spi(file_path)
    assert len(Source_space.names) == 5006
    assert Source_space.coordinates.shape == (5006, 3)


def test_SourceSpace():
    """Test SourceSpace instance and methods"""
    coordinates = np.random.rand(5000, 3)
    names = [("S" + str(i)) for i in range(0, 5000)]
    Source_space = SourceSpace(names, coordinates)

    new_coordinates = np.random.rand(5000, 3)
    Source_space.coordinates = new_coordinates
    assert np.allclose(Source_space.coordinates, new_coordinates)

    new_names = [("F" + str(i)) for i in range(0, 5000)]
    Source_space.names = new_names
    assert Source_space.names == new_names

    subject = "test_subject"
    Source_space.subject = subject
    assert Source_space.subject == subject


def test_SourceSpace_get_center_of_mass():
    coordinates = np.random.rand(5000, 3)
    mean = np.mean(coordinates, axis=0)
    med = np.median(coordinates, axis=0)
    names = [("S" + str(i)) for i in range(0, 5000)]
    source_space = SourceSpace(names, coordinates)
    assert np.allclose(source_space.get_center_of_mass(method="mean"), mean)
    assert np.allclose(source_space.get_center_of_mass(method="median"), med)


def test_write_spi():
    """Test write_spi"""
    filename = os.path.join(data_path, "sample_test_write_spi.spi")
    coordinates = np.random.rand(5000, 3)
    names = [("S" + str(i)) for i in range(0, 5000)]
    Source_space = SourceSpace(names, coordinates)
    write_spi(filename, Source_space)
    Read_Source_space = read_spi(filename)
    assert names == Read_Source_space.names
    assert np.allclose(coordinates, Read_Source_space.coordinates)
