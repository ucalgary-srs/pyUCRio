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
import pytest
import pyucrio
from ...conftest import find_dataset

# globals
DATA_DIR = "%s/../../../test_data/data/ucalgary/read" % (os.path.dirname(os.path.realpath(__file__)))


@pytest.mark.data
def test_list_supported_datasets(rio):
    # list supported datasets
    supported_datasets = rio.data.ucalgary.readers.list_supported_datasets()
    assert len(supported_datasets) > 0


@pytest.mark.data
def test_is_supported(rio):
    # check if supported
    is_supported = rio.data.ucalgary.readers.is_supported("NORSTAR_RIOMETER_K0_TXT")
    assert is_supported is True


@pytest.mark.data
def test_read_swan_hsr(rio, all_datasets):
    # get dataset
    dataset = find_dataset(all_datasets, "SWAN_HSR_K0_H5")

    # read a file using the general reader
    filename = "%s/read_swan_hsr/20240203_mean-hsr_k0_v01.h5" % (DATA_DIR)
    data = rio.data.ucalgary.read(dataset, filename)
    assert isinstance(data, pyucrio.data.ucalgary.Data)


@pytest.mark.data
def test_read_swan_hsr_readers(rio, all_datasets):
    # read a file using the specific reader
    filename = "%s/read_swan_hsr/20240203_mean-hsr_k0_v01.h5" % (DATA_DIR)
    data = rio.data.ucalgary.readers.read_swan_hsr(filename)
    assert isinstance(data, pyucrio.data.ucalgary.Data)


@pytest.mark.data
def test_read_norstar_riometer(rio, all_datasets):
    # get dataset
    dataset = find_dataset(all_datasets, "NORSTAR_RIOMETER_K0_TXT")

    # read a file using the general reader
    filename = "%s/read_norstar_riometer/norstar_k0_rio-fsim_20180503_v01.txt" % (DATA_DIR)
    data = rio.data.ucalgary.read(dataset, filename)
    assert isinstance(data, pyucrio.data.ucalgary.Data)


@pytest.mark.data
def test_read_norstar_riometer_readers(rio, all_datasets):
    # read a file using the specific reader
    filename = "%s/read_norstar_riometer/20240203_mean-hsr_k0_v01.h5" % (DATA_DIR)
    data = rio.data.ucalgary.readers.read_norstar_riometer(filename)
    assert isinstance(data, pyucrio.data.ucalgary.Data)
