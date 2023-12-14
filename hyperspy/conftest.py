# -*- coding: utf-8 -*-
# Copyright 2007-2023 The HyperSpy developers
#
# This file is part of HyperSpy.
#
# HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpy. If not, see <https://www.gnu.org/licenses/#GPL>.

from pathlib import Path

try:
    # Set traits toolkit to work in a headless system
    # Capture error when toolkit is already previously set which typically
    # occurs when building the doc locally
    from traits.etsconfig.api import ETSConfig
    ETSConfig.toolkit = "null"
except ValueError:
    # in case ETSConfig.toolkit was already set previously.
    pass

# pytest-mpl 0.7 already import pyplot, so setting the matplotlib backend to
# 'agg' as early as we can is useless for testing.
import matplotlib.pyplot as plt

import pytest
import numpy as np
import matplotlib
import dask.array as da
import hyperspy.api as hs


matplotlib.rcParams['figure.max_open_warning'] = 25
matplotlib.rcParams['interactive'] = False
hs.preferences.Plot.cmap_navigator = 'viridis'
hs.preferences.Plot.cmap_signal = 'viridis'
hs.preferences.Plot.pick_tolerance = 5.0


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace['np'] = np
    doctest_namespace['plt'] = plt
    doctest_namespace['hs'] = hs
    doctest_namespace['da'] = da


@pytest.fixture
def pdb_cmdopt(request):
    return request.config.getoption("--pdb")


def setup_module(mod, pdb_cmdopt):
    if pdb_cmdopt:
        import dask
        dask.set_options(get=dask.local.get_sync)

from matplotlib.testing.conftest import mpl_test_settings


try:
    import pytest_mpl
except ImportError:
    # Register dummy marker to allow running the test suite without pytest-mpl
    def pytest_configure(config):
        config.addinivalue_line(
            "markers",
            "mpl_image_compare: dummy marker registration to allow running "
            "without the pytest-mpl plugin."
        )


def pytest_configure(config):
    # raise an error if the baseline images are not present
    # which is the case when installing from a wheel
    baseline_images_path = Path(__file__).parent / "tests" / "drawing" / "plot_signal"
    if config.getoption("--mpl") and not baseline_images_path.exists():
        raise ValueError(
            "`--mpl` flag can't not be used because the "
            "baseline images are not packaged."
            )
