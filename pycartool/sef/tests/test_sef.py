# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os

from ...data import data_path
from ..sef import read_sef, write_sef

datasef = os.path.join(data_path, "sample-sef.sef")


def test_read_sef():
    read_sef(datasef)


def test_write_sef():
    sef = read_sef(datasef)
    write_sef("test.sef", sef)
