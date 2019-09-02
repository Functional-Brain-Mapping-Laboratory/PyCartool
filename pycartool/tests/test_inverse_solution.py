# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
from ..io.inverse_solution import read_is

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")

"""
def test_read_is():
    file_path = os.path.join(r"C:\Users\Victor Ferat\Desktop\MNI152.NlinAsym09c.257.5000.2019", "MNI152.NlinAsym09c.257.5000.2019.Loreta.is")
    inverse_solution = read_is(file_path)
    if not inverse_solution["is_type"] == "IS03":
        raise AssertionError()
"""
