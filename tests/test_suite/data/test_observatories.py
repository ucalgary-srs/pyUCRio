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
import pyucrio


@pytest.mark.data
def test_list_observatories(rio):
    # get all sites
    observatories = rio.data.list_observatories("swan_hsr")
    assert len(observatories) > 0

    # check type
    for o in observatories:
        assert isinstance(o, pyucrio.data.Observatory) is True

    # list observatories, but changing the API url to something bad first
    rio.api_base_url = "https://aurora.phys.ucalgary.ca/api_testing_url"
    with pytest.raises(pyucrio.PyUCRioAPIError) as e_info:
        rio.data.list_observatories("norstar_riometer")
        assert "Timeout" in str(e_info)


@pytest.mark.data
def test_list_observatories_in_table(rio, capsys):
    # list observatories in table
    rio.data.list_observatories_in_table("swan_hsr")
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
