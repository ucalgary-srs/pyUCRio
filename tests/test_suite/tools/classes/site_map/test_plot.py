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
import warnings
import os
import string
import random
import cartopy.crs
from matplotlib import pyplot as plt
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    rio_map.plot([-145, -65, 35, 80])
    assert mock_show.call_count == 1


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_args(mock_show, plot_cleanup, rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    rio_map.plot([-145, -65, 35, 80],
                 label=False,
                 figsize=(10, 7),
                 land_color="red",
                 land_edgecolor="green",
                 borders_color="orange",
                 borders_disable=True,
                 title="some title",
                 ocean_color="white")

    assert mock_show.call_count == 1


@pytest.mark.tools
def test_returnfig_savefig(rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    with pytest.raises(ValueError) as e_info:
        rio_map.plot([-145, -65, 35, 80], returnfig=True, savefig=True)
    assert "Only one of returnfig or savefig can be set to True" in str(e_info)


@pytest.mark.tools
def test_returnfig_warnings(rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rio_map.plot([-145, -65, 35, 80], returnfig=True, savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rio_map.plot([-145, -65, 35, 80], returnfig=True, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)

    # check both
    with warnings.catch_warnings(record=True) as w:
        fig, _ = rio_map.plot([-145, -65, 35, 80], returnfig=True, savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The figure will be returned, but a savefig option parameter was supplied" in str(w[-1].message)
    plt.close(fig)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_savefig_warnings(mock_show, rt, plot_cleanup):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    # check savefig_filename
    with warnings.catch_warnings(record=True) as w:
        rio_map.plot([-145, -65, 35, 80], savefig_filename="some_filename")
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check savefig_quality
    with warnings.catch_warnings(record=True) as w:
        rio_map.plot([-145, -65, 35, 80], savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check both
    with warnings.catch_warnings(record=True) as w:
        rio_map.plot([-145, -65, 35, 80], savefig_filename="some_filename", savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "A savefig option parameter was supplied, but the savefig parameter is False" in str(w[-1].message)

    # check plots
    assert mock_show.call_count == 3


@pytest.mark.tools
def test_savefig(rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    # check filename missing
    with pytest.raises(ValueError) as e_info:
        rio_map.plot([-145, -65, 35, 80], savefig=True)
    assert "The savefig_filename parameter is missing, but required since savefig was set to True" in str(e_info)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    rio_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # regular savefig
    output_filename = "/tmp/pyaurorax_testing_%s.jpg" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    rio_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

    # savefig with quality and not a jpg (will show warning)
    output_filename = "/tmp/pyaurorax_testing_%s.png" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    with warnings.catch_warnings(record=True) as w:
        rio_map.plot([-145, -65, 35, 80], savefig=True, savefig_filename=output_filename, savefig_quality=90)
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert "The savefig_quality parameter was specified, but is only used for saving JPG files" in str(w[-1].message)
    assert os.path.exists(output_filename)
    os.remove(output_filename)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_with_data_availability(mock_show, rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj,
                                     instrument_array='swan_hsr',
                                     site_uid_list=['mean'],
                                     color=[['red']],
                                     sym_size=[[5]],
                                     symbol=[['o']])

    # Plot and enforce data availability without actually adding data availability
    with pytest.raises(ValueError) as e_info:
        rio_map.plot([-145, -65, 35, 80], enforce_data_availability=True)

    assert ("Before plotting FOV object with enforce_data_availability=True, " +
            "FOVData.add_availability(...) must be called for all included FOVData objects.") in str(e_info)


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_with_contours(mock_show, rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    # Add some magnetic and geomagnetic contours
    rio_map.add_geo_contours(lats=[60.0, 60.0, 60.0],
                             lons=[-130.0, -125.0, -120.0],
                             constant_lats=[55.0],
                             constant_lons=[-150.0],
                             color="red",
                             linewidth=2,
                             linestyle="--",
                             marker="o",
                             bring_to_front=True)

    rio_map.plot([-145, -65, 35, 80])

    assert mock_show.call_count == 1
