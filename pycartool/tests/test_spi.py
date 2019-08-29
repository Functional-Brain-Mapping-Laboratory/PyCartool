# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
import pytest

import mne
from ..io.roi import read_roi

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


def test_read_spi():
    file_path = os.path.join(data_path, "sample_test_spi.spi")
    spi = read_roi(file_path)
    assert (len(spi) == 5006)
