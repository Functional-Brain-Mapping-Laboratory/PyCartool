# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
from ..io.source_space import read_spi

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


def test_read_spi():
    file_path = os.path.join(data_path, "sample_test_spi.spi")
    spi = read_spi(file_path)
    assert (len(spi[0]) == 5006)
    assert (len(spi[1]) == 5006)
