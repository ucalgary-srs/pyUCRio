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

import shutil
import os
import random
import string
import pytest
import platform
import pyucrio
#import warnings
from pathlib import Path


@pytest.mark.top_level
def test_top_level_class_instantiation_noparams():
    # instantiate
    rio = pyucrio.PyUCRio()

    # check paths
    assert os.path.exists(rio.download_output_root_path)

    # change download root path
    new_path = str("%s/rio_data_download_testing_%s" % (
        Path.home(),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
    ))
    rio.download_output_root_path = new_path
    assert rio.download_output_root_path == new_path
    assert os.path.exists(new_path)
    shutil.rmtree(new_path, ignore_errors=True)

    # check str and repr methods
    assert isinstance(str(rio), str) is True
    assert isinstance(repr(rio), str) is True


@pytest.mark.top_level
def test_top_level_class_instantiation_usingparams():
    # instantiate object
    testing_url = "https://testing-url.com"
    testing_download_path = str("%s/rio_data_download_testing_%s" % (
        Path.home(),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
    ))
    testing_api_timeout = 5
    testing_api_headers = {"some_key": "some value"}
    rio = pyucrio.PyUCRio(
        api_base_url=testing_url,
        download_output_root_path=testing_download_path,
        api_timeout=testing_api_timeout,
        api_headers=testing_api_headers,
    )
    assert rio.download_output_root_path == testing_download_path
    assert rio.api_base_url == testing_url
    assert rio.api_timeout == testing_api_timeout
    assert rio.api_headers == testing_api_headers
    assert os.path.exists(testing_download_path)

    # cleanup
    shutil.rmtree(testing_download_path, ignore_errors=True)


@pytest.mark.top_level
def test_bad_paths_noparams(rio):
    # test bad paths
    #
    # NOTE: we only do this check on Linux since I don't know a bad
    # path to check on Mac. Good enough for now.
    if (platform.system() == "Linux"):
        new_path = "/dev/bad_path"
        with pytest.raises(pyucrio.PyUCRioInitializationError) as e_info:
            rio.download_output_root_path = new_path
        assert "Error during output path creation" in str(e_info)


# @pytest.mark.top_level
# def test_api_headers(rio):
#     # set flag
#     default_headers = rio.api_headers
#     rio.api_headers = None
#     assert rio.api_headers == default_headers

#     # check warning
#     with warnings.catch_warnings(record=True) as w:
#         warnings.simplefilter("always")  # cause all warnings to always be triggered.
#         rio.api_headers = {"user-agent": "some other value"}
#         assert len(w) == 1
#         assert issubclass(w[-1].category, UserWarning)
#         assert "Cannot override default" in str(w[-1].message)


@pytest.mark.top_level
def test_api_timeout(rio):
    # set flag
    default_timeout = rio.api_timeout
    rio.api_timeout = 5
    assert rio.api_timeout == 5
    rio.api_timeout = None
    assert rio.api_timeout == default_timeout


@pytest.mark.top_level
def test_purge_download_path(rio):
    # set up object
    #
    # NOTE: we set the path to something with a random string in it
    # so that our github actions for linux/mac/windows, which fire off
    # simultaneously on the same machine, work without stepping on the
    # toes of each other.
    new_path = str("%s/pyucrio_data_purge_download_testing_%s" % (
        Path.home(),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
    ))
    rio.download_output_root_path = new_path
    assert rio.download_output_root_path == new_path
    assert os.path.exists(rio.download_output_root_path)

    # create some dummy files and folders
    os.makedirs("%s/testing1" % (rio.download_output_root_path), exist_ok=True)
    os.makedirs("%s/testing2" % (rio.download_output_root_path), exist_ok=True)
    os.makedirs("%s/testing2/testing3" % (rio.download_output_root_path), exist_ok=True)
    Path("%s/testing.txt" % (rio.download_output_root_path)).touch()
    Path("%s/testing1/testing.txt" % (rio.download_output_root_path)).touch()

    # check purge function
    rio.purge_download_output_root_path()
    assert len(os.listdir(rio.download_output_root_path)) == 0

    # cleanup
    shutil.rmtree(rio.download_output_root_path, ignore_errors=True)
