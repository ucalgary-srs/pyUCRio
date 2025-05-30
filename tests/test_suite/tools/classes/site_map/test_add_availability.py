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
import cartopy.crs
from unittest.mock import patch

@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_simple(mock_show, plot_cleanup, rt):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    start = datetime.datetime(2024, 1, 1, 0, 0)
    end = datetime.datetime(2024, 1, 1, 23, 59)

    # Create the SiteMap object - omit the site_uid_list so all sites will be plotted
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='norstar_riometer', color='blue', sym_size=5)

    # Now all the add_availibility function
    rio_map.add_availability(dataset_name="NORSTAR_RIOMETER_K0_TXT", start=start, end=end)

    rio_map.plot([-145, -65, 35, 80], enforce_data_availability=True, label=True, upper_label=True)
    assert mock_show.call_count == 1

def test_errors(rt):
    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    start = datetime.datetime(2024, 1, 1, 0, 0)
    end = datetime.datetime(2024, 1, 1, 23, 59)

    # Create the SiteMap object - omit the site_uid_list so all sites will be plotted
    rio_map = rt.site_map.create_map(projection_obj, color='blue', instrument_array="norstar_riometer", sym_size=5)

    # improperly try to add availibility without matching dataset
    with pytest.raises(ValueError) as e_info:
        rio_map.add_availability(dataset_name="some_dataset", start=start, end=end)
    
    assert ("does not match the instrument_array:" in str(e_info))