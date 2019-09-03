# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os

from mne.channels.montage import Montage
from ..io.montage import read_xyz


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


def test_xyz_to_montage():
    file_path = os.path.join(data_path, "EGI257.GenevaAverage13.10-10.xyz")
    montage = read_xyz(file_path)
    print(type(montage))
    if not isinstance(montage, Montage):
        raise AssertionError()
