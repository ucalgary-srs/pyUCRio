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
import datetime
import pyucrio
from pathlib import Path


@pytest.mark.top_level
def test_top_level_class_instantiation_noparams(capsys):
    # instantiate
    rio = pyucrio.PyUCRio()

    # check paths
    rio.initialize_paths()
    assert os.path.exists(rio.download_output_root_path)

    # change download root path
    new_path = str("%s/pyucrio_data_download_testing_%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    rio.download_output_root_path = new_path
    assert rio.download_output_root_path == new_path
    assert os.path.exists(new_path)
    shutil.rmtree(new_path, ignore_errors=True)

    # check __str__ and __repr__ for PyUCRio type
    print_str = str(rio)
    assert print_str != ""
    assert isinstance(str(rio), str) is True
    assert isinstance(repr(rio), str) is True
    rio.pretty_print()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.top_level
def test_top_level_class_instantiation_usingparams():
    # instantiate object
    testing_url = "https://testing-url.com"
    testing_download_path = str("%s/pyucrio_data_download_testing_%s" %
                                (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))

    testing_api_timeout = 5
    rio = pyucrio.PyUCRio(
        api_base_url=testing_url,
        download_output_root_path=testing_download_path,
        api_timeout=testing_api_timeout,
    )
    assert rio.download_output_root_path == testing_download_path
    assert rio.api_base_url == testing_url
    assert rio.api_headers != {} and "user-agent" in rio.api_headers and "python-pyucrio" in rio.api_headers["user-agent"]
    assert rio.api_timeout == testing_api_timeout
    assert os.path.exists(testing_download_path) is False


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
            rio.initialize_paths()
        assert "Error during output path creation" in str(e_info)


@pytest.mark.top_level
def test_api_base_url(rio):
    # set flag
    rio.api_base_url = "https://something"
    assert rio.api_base_url == "https://something"
    rio.api_base_url = None
    assert rio.api_base_url != "https://something"

    # check that trailing slash is removed
    rio.api_base_url = "https://something/"
    assert rio.api_base_url == "https://something"

    # check invalid URL
    with pytest.raises(pyucrio.PyUCRioInitializationError) as e_info:
        rio.api_base_url = "something invalid"
    assert "API base URL is an invalid URL" in str(e_info)


@pytest.mark.top_level
def test_api_timeout(rio):
    # set flag
    default_timeout = rio.api_timeout
    rio.api_timeout = 5
    assert rio.api_timeout == 5
    rio.api_timeout = None
    assert rio.api_timeout == default_timeout


@pytest.mark.top_level
def test_progress_bar_backend(rio):
    # save default for later
    progress_bar_backend = rio.progress_bar_backend

    # set flag (standard)
    rio.progress_bar_backend = "standard"
    assert rio.progress_bar_backend == "standard"

    # set flag (notebook)
    rio.progress_bar_backend = "notebook"
    assert rio.progress_bar_backend == "notebook"

    # set flag (auto)
    rio.progress_bar_backend = "auto"
    assert rio.progress_bar_backend == "auto"

    # set flag (back to default)
    rio.progress_bar_backend = None
    assert rio.progress_bar_backend == progress_bar_backend

    # check invalid value
    with pytest.raises(pyucrio.PyUCRioInitializationError) as e_info:
        rio.progress_bar_backend = "something invalid"
    assert "Invalid progress bar backend" in str(e_info)


@pytest.mark.top_level
def test_purge_download_path(rio):
    # set up object
    #
    # NOTE: we set the path to something with a random string in it
    # so that our github actions for linux/mac/windows, which fire off
    # simultaneously on the same machine, work without stepping on the
    # toes of each other.
    new_path = str("%s/pyucrio_data_purge_download_testing_%s" % (Path.home(), ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))))
    rio.download_output_root_path = new_path
    assert rio.download_output_root_path == new_path
    rio.initialize_paths()
    assert os.path.exists(rio.download_output_root_path) is True

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


@pytest.mark.top_level
def test_show_data_usage(rio, capsys):
    # download a bit of data for several datasets
    for dataset_name in ["SWAN_HSR_K0_H5", "NORSTAR_RIOMETER_K0_TXT"]:
        start_dt = datetime.datetime(2023, 1, 1, 0, 0)
        end_dt = datetime.datetime(2023, 1, 1, 23, 59)
        rio.data.ucalgary.download(dataset_name, start_dt, end_dt, progress_bar_disable=True)

    # check default params
    print(rio.show_data_usage())
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check return_dict=True
    print(rio.show_data_usage(return_dict=True))
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""

    # check order being name
    print(rio.show_data_usage(order="name"))
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""
