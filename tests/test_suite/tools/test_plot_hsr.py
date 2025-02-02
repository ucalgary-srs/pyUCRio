# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import datetime
import warnings
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_single_site(mock_show, rt, hsr_k0_data_list):
    # plot several bands
    hsr_bands = [0, 5]
    rt.plot(
        hsr_k0_data_list[0],
        yrange=(0, 100),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
        hsr_bands=hsr_bands,
        color=["blue", "red"],
        downsample_seconds=10,
        returnfig=True,
    )
    plt.close()


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_multiple_sites(mock_show, rt, hsr_k0_data_list):
    # plot several bands
    hsr_bands = [0, 5]
    rt.plot(
        hsr_k0_data_list,
        yrange=(0, 100),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
        hsr_bands=hsr_bands,
        color=["blue", "red"],
        downsample_seconds=10,
        returnfig=True,
    )
    mock_show.assert_called_once()
    plt.close()


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_multiple_sites_single_band(mock_show, rt, hsr_k0_data_list):
    # plot one band
    hsr_bands = [0]
    rt.plot(
        hsr_k0_data_list,
        yrange=(0, 100),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
        hsr_bands=hsr_bands,
        color=["blue", "red"],
        downsample_seconds=10,
        returnfig=True,
    )
    mock_show.assert_called_once()
    plt.close()


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_stackplot(mock_show, rt, hsr_k0_data_list):
    # make a stack plot
    hsr_bands = [0, 3, 5, 7]
    colors = ["red", "orange", "green", "blue"]
    rt.plot(
        hsr_k0_data_list,
        yrange=(0, 75),
        xrange=(
            datetime.datetime(2023, 11, 5, 6, 0),
            datetime.datetime(2023, 11, 5, 12, 59),
        ),
        hsr_bands=hsr_bands,
        color=colors,
        stack_plot=True,
        figsize=(8, 20),
        returnfig=True,
    )
    mock_show.assert_called_once()
    plt.close()


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_all_bands(mock_show, rt, hsr_k0_data_list):
    # make a stack plot
    rt.plot(
        hsr_k0_data_list,
        yrange=(0, 75),
        xrange=(
            datetime.datetime(2023, 11, 5, 6, 0),
            datetime.datetime(2023, 11, 5, 12, 59),
        ),
        figsize=(8, 20),
        returnfig=True,
    )
    mock_show.assert_called_once()
    plt.close()


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_hsr_absorption_but_k0(mock_show, rt, hsr_k0_data_list):
    # try to plot absorption data, but by not passing any in
    with warnings.catch_warnings(record=True) as w:
        _ = rt.plot(
            hsr_k0_data_list,
            xrange=(
                datetime.datetime(2023, 11, 5, 6, 0),
                datetime.datetime(2023, 11, 5, 12, 59),
            ),
            absorption=True,
            returnfig=True,
        )
        mock_show.assert_called_once()
        plt.close()

        assert len(w) > 0
        assert issubclass(w[0].category, UserWarning)
        assert "Omitting plotting (no absorption data) for" in str(w[0].message)
