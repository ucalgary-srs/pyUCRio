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
import datetime


@pytest.mark.data
def test_download(rio):
    # download
    dataset_name = "NORSTAR_RIOMETER_K0_TXT"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 2, 23, 59)
    r = rio.data.ucalgary.download(dataset_name, start_dt, end_dt)
    assert isinstance(r, pyucrio.data.ucalgary.FileDownloadResult)
    assert r.count > 0


@pytest.mark.data
def test_download_using_urls(rio):
    # get urls
    dataset_name = "NORSTAR_RIOMETER_K0_TXT"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 2, 23, 59)
    r = rio.data.ucalgary.get_urls(dataset_name, start_dt, end_dt)
    assert isinstance(r, pyucrio.data.ucalgary.FileListingResponse)
    assert r.count > 0

    # download
    r = rio.data.ucalgary.download_using_urls(r)
    assert isinstance(r, pyucrio.data.ucalgary.FileDownloadResult)
    assert r.count > 0
