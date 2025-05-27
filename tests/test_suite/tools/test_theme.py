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
from unittest.mock import patch


@pytest.mark.tools
@patch("matplotlib.pyplot.show")
def test_plot_dark_mode(mock_show, plot_cleanup, rt, rio_k0_data_list):
    # set plot theme to dark mode
    rt.set_theme("dark")
    rt.plot(rio_k0_data_list)

    # set plot theme to light mode
    rt.set_theme("light")
    rt.plot(rio_k0_data_list)

    # set plot theme to default mode
    rt.set_theme("default")
    rt.plot(rio_k0_data_list)

    # set plot theme to another available mode
    rt.set_theme("ggplot")
    rt.plot(rio_k0_data_list)

    # check number of plots
    assert mock_show.call_count == 4
