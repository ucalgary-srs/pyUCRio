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
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_single_site(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # check the plotting routine
    rt.plot(
        rio_k2_data_list[0],
        yrange=(0, 10),
        title="Some title",
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_multiple_sites(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # check the plotting routine
    rt.plot(
        rio_k2_data_list,
        yrange=(0, 10),
        title="Some title",
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_absorption_and_xrange(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # plot the absorption data, with restricting the plotting range to a
    # few hours of data
    rt.plot(
        rio_k2_data_list,
        absorption=True,
        yrange=(0, 5),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_absorption_xrange_downsample(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # down-sampling to 1-minute intervals
    rt.plot(
        rio_k2_data_list,
        absorption=True,
        yrange=(0, 5),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
        downsample_seconds=60,
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_absorption_xrange_downsample_color(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # downsample using 10-minute intervals and changing up the colors
    rt.plot(
        rio_k2_data_list,
        absorption=True,
        yrange=(0, 5),
        xrange=(
            datetime.datetime(2023, 11, 5, 4, 0),
            datetime.datetime(2023, 11, 5, 13, 59),
        ),
        color=["red", "purple", "cyan"],
        downsample_seconds=600,
        title="2023-11-05 (10-min Down-sampling)",
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_stackplot_single(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # make a stack plot
    rt.plot(
        rio_k2_data_list[0],
        xrange=(
            datetime.datetime(2023, 11, 5, 6, 0),
            datetime.datetime(2023, 11, 5, 12, 59),
        ),
        stack_plot=True,
        figsize=(8, 20),
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_stackplot_multiple(mock_show, plot_cleanup, rt, rio_k2_data_list):
    # make a stack plot
    rt.plot(
        rio_k2_data_list,
        xrange=(
            datetime.datetime(2023, 11, 5, 6, 0),
            datetime.datetime(2023, 11, 5, 12, 59),
        ),
        stack_plot=True,
        figsize=(8, 20),
    )
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_riometer_absorption_but_k0(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # try to plot absorption data, but by not passing any in
    with warnings.catch_warnings(record=True) as w:
        rt.plot(
            rio_k0_data_list,
            xrange=(
                datetime.datetime(2023, 11, 5, 6, 0),
                datetime.datetime(2023, 11, 5, 12, 59),
            ),
            absorption=True,
        )
    assert len(w) > 0
    assert issubclass(w[0].category, UserWarning)
    assert "Omitting plotting (no absorption data) for" in str(w[0].message)

    # check plot was shown
    assert mock_show.call_count == 1
