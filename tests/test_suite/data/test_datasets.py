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
def test_list_datasets(rio):
    # list datasets
    datasets = rio.data.list_datasets()
    assert len(datasets) > 0

    # check type
    for d in datasets:
        assert isinstance(d, pyucrio.data.Dataset) is True

    # list datasets, but changing the API url to something bad first
    rio.api_base_url = "https://aurora.phys.ucalgary.ca/api_testing_url"
    with pytest.raises(pyucrio.PyUCRioAPIError) as e_info:
        rio.data.list_datasets()
        assert "Timeout" in str(e_info)


@pytest.mark.data
def test_get_dataset(rio):
    # get dataset
    dataset = rio.data.get_dataset("SWAN_HSR_K0_H5")
    assert isinstance(dataset, pyucrio.data.Dataset)
    assert dataset.name == "SWAN_HSR_K0_H5"

    # get dataset that doesn't exist
    with pytest.raises(pyucrio.PyUCRioError) as e_info:
        dataset = rio.data.get_dataset("SOME_BAD_DATASET")
        assert "Dataset not found" in str(e_info)


@pytest.mark.data
def test_list_datasets_in_table(rio, capsys):
    # list datasets in table
    rio.data.list_datasets_in_table()
    captured_stdout = capsys.readouterr().out
    assert captured_stdout != ""


@pytest.mark.data
def test_is_read_supported(rio):
    # check if read supported
    is_read_supported = rio.data.ucalgary.is_read_supported("SWAN_HSR_K0_H5")
    assert is_read_supported is True


@pytest.mark.data
def test_list_supported_datasets(rio):
    # list supported datasets
    supported_datasets = rio.data.ucalgary.list_supported_read_datasets()
    assert len(supported_datasets) > 0
