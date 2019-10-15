# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import os
import pytest
import numpy as np

from ..io.inverse_solution import read_is
from ..source_estimate import read_ris, SourceEstimate
from ..regions_of_interest import RegionsOfInterest
from ..source_space import SourceSpace

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')


def generate_source_space(size):
    """Generate Source space."""
    source_names = [('S' + str(i)) for i in range(0, size)]
    source_coords = np.random.rand(size, 3)
    source_space = SourceSpace(source_names, source_coords)
    return(source_space)


def generate_source_estimate(n_sources, n_times, sfreq):
    """Generate Source Estimate."""
    sources_tc = np.random.rand(n_sources, 3, n_times)
    source_estimate = SourceEstimate(sources_tc, sfreq)
    return(source_estimate)


def generate_rois(n_roi, n_sources):
    """Generate Rois."""
    rois_names = [('R' + str(i)) for i in range(0, n_roi)]
    roi_indices = []
    for i in range(0, n_roi):
        indices = np.random.randint(0, n_sources, size=i+1).tolist()
        roi_indices.append(indices)
    regions_of_interest = RegionsOfInterest(rois_names, roi_indices)
    return(regions_of_interest)


@pytest.mark.skip(reason='Requires large file')
def test_read_is():
    """Test read_is."""
    file_path = os.path.join('test')
    inverse_solution = read_is(file_path)
    if not inverse_solution['is_type'] == 'IS03':
        raise AssertionError()


def test_read_ris():
    """Test read_ris."""
    file_path = os.path.join(data_path, 'sample_test_ris.ris')
    read_ris(file_path)


def test_write_ris():
    """Test write_is."""
    file_path = os.path.join(data_path, 'sample_test_write_ris.ris')
    sources_tc = np.random.rand(5000, 3, 2048).astype('float32')
    sfreq = 512
    subject = 'test_subject'
    source_estimate = SourceEstimate(sources_tc, sfreq, subject=subject)
    source_estimate.save(file_path)
    read_source_estimate = read_ris(file_path)
    if not (read_source_estimate.sources_tc == sources_tc).all():
        raise AssertionError()
    if not read_source_estimate.sfreq == sfreq:
        raise AssertionError()
    if not read_source_estimate.filename == file_path:
        raise AssertionError()


def test_compute_tc():
    """Test SourceEstimate.compute_tc."""
    source_estimate = generate_source_estimate(5000, 2048, 512)
    tc_mean = source_estimate.compute_tc(method='mean')
    tc_med = source_estimate.compute_tc(method='median')
    tc_svd = source_estimate.compute_tc(method='svd')
    print(tc_mean.shape)
    if not tc_mean.shape == (3, 2048):
        raise AssertionError()
    if not tc_med.shape == (3, 2048):
        raise AssertionError()
    if not tc_svd.shape == (1, 2048):
        raise AssertionError()


def test_compute_rois_tc():
    """Test SourceEstimate.compute_rois_tc."""
    source_space = generate_source_space(5000)
    source_estimate = generate_source_estimate(5000, 2048, 512)
    source_estimate.source_space = source_space
    regions_of_interest = generate_rois(32, 5000)
    regions_of_interest.source_space = source_space
    rois_estimates = source_estimate.compute_rois_tc(regions_of_interest)
    if not rois_estimates.sources_tc.shape == (32, 1, 2048):
        raise AssertionError()
    if not rois_estimates.sfreq == 512:
        raise AssertionError()


def test_per_roi():
    """Test SourceEstimate.per_roi"""
    source_space = generate_source_space(5000)
    source_estimate = generate_source_estimate(5000, 2048, 512)
    source_estimate.source_space = source_space
    regions_of_interest = generate_rois(32, 5000)
    regions_of_interest.source_space = source_space
    rois_estimates = source_estimate.per_roi(regions_of_interest)
    if not len(rois_estimates) == 32:
        raise AssertionError()
