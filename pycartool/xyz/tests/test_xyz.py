# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import os

from mne.channels import DigMontage

from ...data import data_path
from ..xyz import read_xyz


def test_read_xyz():
    """Test read_xyz."""
    file_path = os.path.join(data_path, "EGI257.GenevaAverage13.10-10.xyz")
    montage = read_xyz(file_path)
    assert isinstance(montage, DigMontage)
