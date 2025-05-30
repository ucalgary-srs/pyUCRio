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
import cartopy.crs


@pytest.mark.tools
def test_simple(rt, capsys):

    center_lat = -100.0
    center_lon = 55.0
    projection_obj = cartopy.crs.NearsidePerspective(central_longitude=center_lat, central_latitude=center_lon)

    # Create the SiteMap object
    rio_map = rt.site_map.create_map(projection_obj, instrument_array='swan_hsr', site_uid_list=['mean'], color='red', sym_size=5)

    # check __str__ and __repr__ for Keogram type
    print_str = str(rio_map)
    assert print_str != ""
    assert isinstance(str(rio_map), str) is True
    assert isinstance(repr(rio_map), str) is True
    rio_map.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
