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

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Union, Optional
from pyucalgarysrs.data import Dataset, Data
from pyucalgarysrs.exceptions import SRSError, SRSUnsupportedReadError
from ....exceptions import PyUCRioError, PyUCRioUnsupportedReadError
if TYPE_CHECKING:
    from ....pyucrio import PyUCRio  # pragma: nocover-ok


class ReadManager:
    """
    The UCalgaryManager object is initialized within every PyUCRio object. It acts as a way 
    to access the submodules and carry over configuration information in the super class.
    """

    def __init__(self, rio_obj):
        self.__rio_obj: PyUCRio = rio_obj

    def list_supported_datasets(self) -> List[str]:
        """
        List the datasets which have file reading capabilities supported.

        Returns:
            A list of the dataset names with file reading support.
        """
        return self.__rio_obj.srs_obj.data.readers.list_supported_datasets()

    def is_supported(self, dataset_name: str) -> bool:
        """
        Check if a given dataset has file reading support. 
        
        Not all datasets available in the UCalgary Space Remote Sensing Open Data Platform 
        have special readfile routines in this library. This is because some datasets are 
        handled by other libraries (ie. PyAuroraX for ASI data), or are in basic formats 
        such as JPG or PNG, so unique functions aren't necessary. We leave it up to the 
        user to open those basic files in whichever way they prefer. Use the 
        `list_supported_read_datasets()` function to see all datasets that have special
        file reading functionality in this library.

        Args:
            dataset_name (str): 
                The dataset name to check if file reading is supported. This parameter 
                is required.
        
        Returns:
            Boolean indicating if file reading is supported.
        """
        return self.__rio_obj.srs_obj.data.readers.is_supported(dataset_name)

    def read(self,
             dataset: Dataset,
             file_list: Union[List[str], List[Path], str, Path],
             n_parallel: int = 1,
             no_metadata: bool = False,
             start_time: Optional[datetime.datetime] = None,
             end_time: Optional[datetime.datetime] = None,
             quiet: bool = False) -> Data:
        """
        Read in data files for a given dataset. Note that only one type of dataset's data
        should be read in using a single call.

        Args:
            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                required.
            
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.
                        
            no_metadata (bool): 
                Skip reading of metadata. This is a minor optimization if the metadata is not needed.
                Default is `False`. This parameter is optional.
            
            start_time (datetime.datetime): 
                The start timestamp to read data onwards from (inclusive). This can be utilized to 
                read a portion of a data file, and could be paired with the `end_time` parameter. 
                This tends to be utilized for datasets that are hour or day-long files where it is 
                possible to only read a smaller bit of that file. If not supplied, it will assume 
                the start time is the timestamp of the first record in the first file supplied (ie. 
                beginning of the supplied data). This parameter is optional.

            end_time (datetime.datetime): 
                The end timestamp to read data up to (inclusive). This can be utilized to read a 
                portion of a data file, and could be paired with the `start_time` parameter. This 
                tends to be utilized for datasets that are hour or day-long files where it is possible 
                to only read a smaller bit of that file. If not supplied, it will it will assume the 
                end time is the timestamp of the last record in the last file supplied (ie. end of the 
                supplied data). This parameter is optional.

            quiet (bool): 
                Do not print out errors while reading data files, if any are encountered. Any files
                that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Data` object. This parameter is optional.
        
        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyucrio.exceptions.PyUCRioUnsupportedReadError: an unsupported dataset was used when
                trying to read files.
            pyucrio.exceptions.PyUCRioError: a generic read error was encountered
        """
        try:
            return self.__rio_obj.srs_obj.data.readers.read(
                dataset,
                file_list,
                n_parallel=n_parallel,
                no_metadata=no_metadata,
                start_time=start_time,
                end_time=end_time,
                quiet=quiet,
            )
        except SRSUnsupportedReadError as e:  # pragma: nocover-ok
            raise PyUCRioUnsupportedReadError(e) from e
        except SRSError as e:  # pragma: nocover-ok
            raise PyUCRioError(e) from e

    def read_norstar_riometer(self,
                              file_list: Union[List[str], List[Path], str, Path],
                              n_parallel: int = 1,
                              no_metadata: bool = False,
                              start_time: Optional[datetime.datetime] = None,
                              end_time: Optional[datetime.datetime] = None,
                              quiet: bool = False,
                              dataset: Optional[Dataset] = None) -> Data:
        """
        Read in NORSTAR Riometer data (K0 and K2 ASCII files).

        Args:
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.
                        
            no_metadata (bool): 
                Skip reading of metadata. This is a minor optimization if the metadata is not needed.
                Default is `False`. This parameter is optional.

            start_time (datetime.datetime): 
                The start timestamp to read data onwards from (inclusive). This can be utilized to 
                read a portion of a data file, and could be paired with the `end_time` parameter. 
                This tends to be utilized for datasets that are hour or day-long files where it is 
                possible to only read a smaller bit of that file. If not supplied, it will assume 
                the start time is the timestamp of the first record in the first file supplied (ie. 
                beginning of the supplied data). This parameter is optional.

            end_time (datetime.datetime): 
                The end timestamp to read data up to (inclusive). This can be utilized to read a 
                portion of a data file, and could be paired with the `start_time` parameter. This 
                tends to be utilized for datasets that are hour or day-long files where it is possible 
                to only read a smaller bit of that file. If not supplied, it will it will assume the 
                end time is the timestamp of the last record in the last file supplied (ie. end of the 
                supplied data). This parameter is optional.

            quiet (bool): 
                Do not print out errors while reading data files, if any are encountered. Any files
                that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Data` object. This parameter is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyucrio.exceptions.PyUCRioError: a generic read error was encountered
        """
        try:
            return self.__rio_obj.srs_obj.data.readers.read_norstar_riometer(
                file_list,
                n_parallel=n_parallel,
                no_metadata=no_metadata,
                start_time=start_time,
                end_time=end_time,
                quiet=quiet,
                dataset=dataset,
            )
        except SRSError as e:  # pragma: nocover-ok
            raise PyUCRioError(e) from e

    def read_swan_hsr(self,
                      file_list: Union[List[str], List[Path], str, Path],
                      n_parallel: int = 1,
                      no_metadata: bool = False,
                      start_time: Optional[datetime.datetime] = None,
                      end_time: Optional[datetime.datetime] = None,
                      quiet: bool = False,
                      dataset: Optional[Dataset] = None) -> Data:
        """
        Read in SWAN Hyper Spectral Riometer (HSR) data (K0 H5 files).

        Args:
            file_list (List[str], List[Path], str, Path): 
                The files to read in. Absolute paths are recommended, but not technically
                necessary. This can be a single string for a file, or a list of strings to read
                in multiple files. This parameter is required.

            n_parallel (int): 
                Number of data files to read in parallel using multiprocessing. Default value 
                is 1. Adjust according to your computer's available resources. This parameter 
                is optional.
                        
            no_metadata (bool): 
                Skip reading of metadata. This is a minor optimization if the metadata is not needed.
                Default is `False`. This parameter is optional.

            start_time (datetime.datetime): 
                The start timestamp to read data onwards from (inclusive). This can be utilized to 
                read a portion of a data file, and could be paired with the `end_time` parameter. 
                This tends to be utilized for datasets that are hour or day-long files where it is 
                possible to only read a smaller bit of that file. If not supplied, it will assume 
                the start time is the timestamp of the first record in the first file supplied (ie. 
                beginning of the supplied data). This parameter is optional.

            end_time (datetime.datetime): 
                The end timestamp to read data up to (inclusive). This can be utilized to read a 
                portion of a data file, and could be paired with the `start_time` parameter. This 
                tends to be utilized for datasets that are hour or day-long files where it is possible 
                to only read a smaller bit of that file. If not supplied, it will it will assume the 
                end time is the timestamp of the last record in the last file supplied (ie. end of the 
                supplied data). This parameter is optional.

            quiet (bool): 
                Do not print out errors while reading data files, if any are encountered. Any files
                that encounter errors will be, as usual, accessible via the `problematic_files` 
                attribute of the returned `Data` object. This parameter is optional.

            dataset (Dataset): 
                The dataset object for which the files are associated with. This parameter is
                optional.

        Returns:
            A [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data) 
            object containing the data read in, among other values.
        
        Raises:
            pyucrio.exceptions.PyUCRioError: a generic read error was encountered
        """
        return self.__rio_obj.srs_obj.data.readers.read_swan_hsr(
            file_list,
            n_parallel=n_parallel,
            no_metadata=no_metadata,
            start_time=start_time,
            end_time=end_time,
            quiet=quiet,
            dataset=dataset,
        )
