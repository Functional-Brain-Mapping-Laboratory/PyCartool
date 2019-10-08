# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)

import os
import pytest
import numpy as np

from ..io.inverse_solution import read_is
from ..source_estimate import read_ris, write_ris, SourceEstimate


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
    source_estimate = read_ris(file_path)


def test_write_ris():
    """ Test write_is."""
    file_path = os.path.join(data_path, 'sample_test_write_ris.ris')
    sources_tc = np.random.rand(5000, 3, 2048)
    sfreq = 512
    subject = 'test_subject'
    source_estimate = SourceEstimate(sources_tc, sfreq, subject=subject)
    source_estimate.save(file_path)
    read_source_estimate = read_ris(file_path)
    if not (read_source_estimate.sources_tc == sources_tc.astype('float32')).all():
        raise AssertionError()
    if not read_source_estimate.sfreq == sfreq:
        raise AssertionError()
    if not read_source_estimate.filename == file_path:
        raise AssertionError()
