# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
import pytest
import numpy as np

from ..io.inverse_solution import read_is, read_ris, write_ris

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')


@pytest.mark.skip(reason='Requires large file')
def test_read_is():
    """ Test read_is."""
    file_path = os.path.join(r'C:\Users\Victor Ferat\Desktop\MNI152.NlinAsym09c.257.5000.2019", "MNI152.NlinAsym09c.257.5000.2019.Loreta.is')
    inverse_solution = read_is(file_path)
    if not inverse_solution['is_type'] == 'IS03':
        raise AssertionError()


def test_read_ris():
    """ Test read_ris."""
    file_path = os.path.join(data_path, 'sample_test_ris.ris')
    inverse_solution_computation = read_ris(file_path)
    if not inverse_solution_computation['ris_type'] == 'RI01':
        raise AssertionError()


def test_write_ris():
    """ Test write_is."""
    file_path = os.path.join(data_path, 'sample_test_write_ris.ris')
    inverse_solution_computation = np.random.rand(2048, 3, 5000)
    sfreq = 512
    write_ris(file_path, inverse_solution_computation, sfreq)
    read_results = read_ris(file_path)
    if not read_results['ris_type'] == 'RI01':
        raise AssertionError()
    if not (read_results['data'] == inverse_solution_computation.astype('float32')).all():
        raise AssertionError()
    if not read_results['sfreq'] == sfreq:
        raise AssertionError()
