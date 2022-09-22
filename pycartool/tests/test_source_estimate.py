# -*- coding: utf-8 -*-
# Authors: Victor Férat <victor.ferat@live.fr>
#
# License: BSD (3-clause)
import os

import numpy as np
import pytest

from ..io.inverse_solution import read_is
from ..regions_of_interest import RegionsOfInterest
from ..source_estimate import SourceEstimate, read_ris
from ..source_space import SourceSpace

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


def generate_source_space(size):
    """Generate Source space."""
    source_names = [("S" + str(i)) for i in range(0, size)]
    source_coords = np.random.rand(size, 3)
    source_space = SourceSpace(source_names, source_coords)
    return source_space


def generate_source_estimate(n_sources, n_times, sfreq):
    """Generate Source Estimate."""
    sources_tc = np.random.rand(n_sources, 3, n_times)
    source_estimate = SourceEstimate(sources_tc, sfreq)
    return source_estimate


def generate_rois(n_roi, n_sources):
    """Generate Rois."""
    rois_names = [("R" + str(i)) for i in range(0, n_roi)]
    roi_indices = []
    for i in range(0, n_roi):
        indices = np.random.randint(0, n_sources, size=i + 1).tolist()
        roi_indices.append(indices)
    regions_of_interest = RegionsOfInterest(rois_names, roi_indices)
    return regions_of_interest


sfreq = 1
n_samples = 500
n_sources = 100
n_rois = 10
source_space = generate_source_space(n_sources)

source_estimate = generate_source_estimate(n_sources, n_samples, sfreq)
source_estimate.source_space = source_space

regions_of_interest = generate_rois(n_rois, n_sources)
regions_of_interest.source_space = source_space


@pytest.mark.skip(reason="Requires large file")
def test_read_is():
    """Test read_is."""
    file_path = os.path.join("test")
    inverse_solution = read_is(file_path)
    if not inverse_solution["is_type"] == "IS03":
        raise AssertionError()


def test_read_ris():
    """Test read_ris."""
    file_path = os.path.join(data_path, "sample_test_ris.ris")
    read_ris(file_path)


def test_write_ris():
    """Test write_is."""
    source_estimate.save("test.ris")
    read_source_estimate = read_ris("test.ris")
    assert np.allclose(
        read_source_estimate.sources_tc, source_estimate.sources_tc
    )
    assert read_source_estimate.sfreq == source_estimate.sfreq
    assert read_source_estimate.filename == "test.ris"


def test_compute_tc():
    """Test SourceEstimate.compute_tc."""
    tc_mean = source_estimate.compute_tc(method="mean")
    assert tc_mean.shape == (3, n_samples)

    tc_med = source_estimate.compute_tc(method="median")
    assert tc_med.shape == (3, n_samples)

    tc_svd = source_estimate.compute_tc(method="svd")
    assert tc_svd.shape == (1, n_samples)


def test_compute_rois_tc():
    """Test SourceEstimate.compute_rois_tc."""
    rois_estimates = source_estimate.compute_rois_tc(regions_of_interest)
    assert rois_estimates.sources_tc.shape == (n_rois, 1, n_samples)
    assert rois_estimates.sfreq == source_estimate.sfreq


def test_per_roi():
    """Test SourceEstimate.per_roi"""
    rois_estimates = source_estimate.per_roi(regions_of_interest)
    assert len(rois_estimates) == n_rois
