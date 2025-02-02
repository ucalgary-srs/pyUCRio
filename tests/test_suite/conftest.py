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

import glob
import shutil
import copy
import pytest
import datetime
import pyucalgarysrs
import pyucrio
from pathlib import Path
from matplotlib import pyplot as plt


def pytest_addoption(parser):
    parser.addoption("--api-url", action="store", default="https://api-staging.phys.ucalgary.ca", help="A specific API URL to use")


@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture(scope="function")
def srs(api_url):
    return pyucalgarysrs.PyUCalgarySRS(api_base_url=api_url)


@pytest.fixture(scope="function")
def rio(api_url):
    return pyucrio.PyUCRio(api_base_url=api_url)


@pytest.fixture(scope="function")
def rt(api_url):
    rio = pyucrio.PyUCRio(api_base_url=api_url)
    return rio.tools


@pytest.fixture(scope="session")
def all_datasets(api_url):
    srs = pyucrio.PyUCRio(api_base_url=api_url)
    return srs.data.list_datasets()


@pytest.fixture(scope="session")
def rio_k0_data_list(api_url):
    # init
    rio = pyucrio.PyUCRio(api_base_url=api_url)

    # download and read in a day of riometer data from a couple sites
    start_dt = datetime.datetime(2023, 11, 5, 0, 0)
    end_dt = datetime.datetime(2023, 11, 5, 23, 59)
    dataset_name = "NORSTAR_RIOMETER_K0_TXT"
    site_uid = ["chur", "daws", "rabb"]
    rio_data_list = []
    for site in site_uid:
        # download the data
        r = rio.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site, progress_bar_disable=True)

        # read the data
        data = rio.data.ucalgary.read(r.dataset, r.filenames, n_parallel=2)

        # we'll add the read data into a larger list we'll use later on
        rio_data_list.append(data)

    # return
    return rio_data_list


@pytest.fixture(scope="session")
def rio_k2_data_list(api_url):
    # init
    rio = pyucrio.PyUCRio(api_base_url=api_url)

    # download and read in a day of riometer data from a couple sites
    start_dt = datetime.datetime(2023, 11, 5, 0, 0)
    end_dt = datetime.datetime(2023, 11, 5, 23, 59)
    dataset_name = "NORSTAR_RIOMETER_K2_TXT"
    site_uid = ["chur", "daws", "rabb"]
    rio_data_list = []
    for site in site_uid:
        # download the data
        r = rio.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site, progress_bar_disable=True)

        # read the data
        data = rio.data.ucalgary.read(r.dataset, r.filenames, n_parallel=2)

        # we'll add the read data into a larger list we'll use later on
        rio_data_list.append(data)

    # return
    return rio_data_list


@pytest.fixture(scope="session")
def hsr_k0_data_list(api_url):
    # init
    rio = pyucrio.PyUCRio(api_base_url=api_url)

    # download a few hours of SWAN HSR data from two sites
    start_dt = datetime.datetime(2023, 11, 5, 4, 0)
    end_dt = datetime.datetime(2023, 11, 5, 13, 59)
    dataset_name = "SWAN_HSR_K0_H5"
    site_uid = ["medo", "russ"]
    hsr_data_list = []
    for site in site_uid:
        # download the data
        r = rio.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site, progress_bar_disable=True)

        # read the data
        data = rio.data.ucalgary.read(r.dataset, r.filenames, n_parallel=2)

        # append to a list that we'll use later
        hsr_data_list.append(data)

    # return
    return hsr_data_list


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    glob_str = "%s/pyucrio_data_*testing*" % (str(Path.home()))
    path_list = sorted(glob.glob(glob_str))
    for p in path_list:
        shutil.rmtree(p)

    plt.close("all")


def find_dataset(datasets, dataset_name):
    for d in datasets:
        if (d.name == dataset_name):
            return copy.deepcopy(d)
    return None
