# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os

from ..io.sef import read_sef, write_sef

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")

datasef = os.path.join(data_path, "sample-sef.sef")


def test_read_sef():
    read_sef(datasef)
    return ()


def test_write_sef():
    sef = read_sef(datasef)
    write_sef("test.sef", sef)
    return ()
