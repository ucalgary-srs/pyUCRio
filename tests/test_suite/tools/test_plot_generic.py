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

import os
import random
import string
import pytest
import warnings
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_dark_mode(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # set plot theme to dark mode
    rt.set_theme("dark")

    # let's see the plot again
    rt.plot(rio_k0_data_list, yrange=(0, 10), title="Some title")
    assert mock_show.call_count == 1

    # change back to light mode
    rt.set_theme("light")


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_warnings1(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # returnfig=True, savefig_filename supplied
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rt.plot(rio_k0_data_list, returnfig=True, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied." in str(w[-1].message)
    plt.close(fig)

    # returnfig=True, savefig_quality supplied
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rt.plot(rio_k0_data_list, returnfig=True, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied." in str(w[-1].message)
    plt.close(fig)

    # returnfig=True, savefig_filename and savefig_quality supplied
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rt.plot(rio_k0_data_list, returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied." in str(w[-1].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_warnings2(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # savefig=False, savefig_filename supplied
    with warnings.catch_warnings(record=True) as w:
        rt.plot(rio_k0_data_list, savefig=False, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False." in str(w[-1].message)

    # savefig not specified, savefig_filename supplied
    with warnings.catch_warnings(record=True) as w:
        rt.plot(rio_k0_data_list, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False." in str(w[-1].message)

    # savefig not specified, savefig_quality supplied
    with warnings.catch_warnings(record=True) as w:
        rt.plot(rio_k0_data_list, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False." in str(w[-1].message)

    # savefig not supplied, savefig_filename and savefig_quality supplied
    with warnings.catch_warnings(record=True) as w:
        rt.plot(rio_k0_data_list, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False." in str(w[-1].message)

    # check that four plots were shown
    assert mock_show.call_count == 4


@pytest.mark.tools
def test_plot_savefig_returnfig(rt, rio_k0_data_list):
    with pytest.raises(ValueError) as e_info:
        rt.plot(rio_k0_data_list, returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_plot_multiple_types(rt, rio_k0_data_list, hsr_k0_data_list):
    # try to plot both riometer and HSR data
    all_data = rio_k0_data_list + hsr_k0_data_list
    with pytest.raises(ValueError) as e_info:
        rt.plot(all_data)
    assert "Cannot plot multiple data-types on the same axis" in str(e_info)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_title(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # regular plot mode
    rt.plot(rio_k0_data_list[0], yrange=(0, 10), title="Some title")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_title_stack(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # stack plot mode
    rt.plot(rio_k0_data_list, stack_plot=True, yrange=(0, 10), title="Some title")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_xtitle(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # regular plot mode
    rt.plot(rio_k0_data_list[0], xtitle="Some label")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_xtitle_stack(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # stack plot mode
    rt.plot(rio_k0_data_list, stack_plot=True, xtitle="Some label")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_ytitle(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # regular plot mode
    rt.plot(rio_k0_data_list[0], ytitle="Some label")
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_ytitle_stack(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # stack plot mode
    rt.plot(rio_k0_data_list[0], stack_plot=True, ytitle="Some label")
    assert mock_show.call_count == 1


@pytest.mark.tools
def test_plot_savefig_no_filename(plot_cleanup, rt, rio_k0_data_list):
    # savefig but with no filename
    with pytest.raises(ValueError) as e_info:
        rt.plot(rio_k0_data_list, savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)


@pytest.mark.tools
def test_plot_savefig_png(plot_cleanup, rt, rio_k0_data_list):
    # savefig
    filename = "/tmp/pyucrio_test_savefig_%s.png" % (''.join(random.choices(string.ascii_lowercase, k=8)))
    rt.plot(rio_k0_data_list, savefig=True, savefig_filename=filename)

    # cleanup
    os.remove(filename)


@pytest.mark.tools
def test_plot_savefig_png_quality_warning(plot_cleanup, rt, rio_k0_data_list):
    # savefig
    filename = "/tmp/pyucrio_test_savefig_%s.png" % (''.join(random.choices(string.ascii_lowercase, k=8)))
    with warnings.catch_warnings(record=True) as w:
        rt.plot(rio_k0_data_list, savefig=True, savefig_filename=filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files." in str(w[-1].message)

    # cleanup
    os.remove(filename)


@pytest.mark.tools
def test_plot_savefig_jpg(plot_cleanup, rt, rio_k0_data_list):
    # savefig
    filename = "/tmp/pyucrio_test_savefig_%s.jpg" % (''.join(random.choices(string.ascii_lowercase, k=8)))
    rt.plot(rio_k0_data_list, savefig=True, savefig_filename=filename)

    # cleanup
    os.remove(filename)
