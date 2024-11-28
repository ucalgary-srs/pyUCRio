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
import shutil
import humanize
import pyucalgarysrs
from texttable import Texttable
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from . import __version__
from .exceptions import PyUCRioInitializationError, PyUCRioPurgeError
from .data import DataManager
from . import tools as tools_module


class PyUCRio:
    """
    The `PyUCRio` class is the primary entry point for utilizing
    this library. It is used to initialize a session, capturing details
    about API connectivity, environment, and more. All submodules are 
    encapsulated within this class, so any usage of the library starts 
    with creating this object.

    ```python
    import pyucrio
    rio = pyucrio.PyUCRio()
    ```

    When working with this object, you can set configuration parameters, such 
    as the destination directory for downloaded data, or API special settings 
    (e.g., timeout, HTTP headers, API key). These parameters can be set when 
    instantiating the object, or after instantiating using the self-contained 
    accessible variables.
    """

    __DEFAULT_API_BASE_URL = "https://api.phys.ucalgary.ca"
    __DEFAULT_API_TIMEOUT = 10
    __DEFAULT_API_HEADERS = {
        "content-type": "application/json",
        "user-agent": "python-pyucrio/%s" % (__version__),
    }  # NOTE: these MUST be lowercase so that the decorator logic cannot be overridden

    def __init__(self,
                 download_output_root_path: Optional[str] = None,
                 api_base_url: Optional[str] = None,
                 api_timeout: Optional[int] = None,
                 api_headers: Optional[Dict] = None,
                 srs_obj: Optional[pyucalgarysrs.PyUCalgarySRS] = None):
        """
        Attributes:
            download_output_root_path (str): 
                Destination directory for downloaded data. The default for this path is a 
                subfolder in the user's home directory, such  as `/home/user/pyucrio_data` 
                in Linux. In Windows and Mac, it is similar.

            api_base_url (str): 
                URL prefix to use when interacting with the UCalgary Space Remote Sensing API. By
                default this is set to `https://api.phys.ucalgary.ca`. This parameter is primarily
                used by the development team to test and build new functions using the private staging
                API.

            api_timeout (int): 
                The timeout used when communicating with the UCalgary SRS API. This value is represented in 
                seconds, and by default is `10 seconds`.
            
            api_headers (Dict): 
                HTTP headers used when communicating with the UCalgary SRS API. The default for this value 
                consists of several standard headers. Any changes to this parameter are in addition to 
                the default standard headers.
        
            srs_obj (pyucalgarysrs.PyUCalgarySRS): 
                A [PyUCalgarySRS](https://docs-pyucalgarysrs.phys.ucalgary.ca/#pyucalgarysrs.PyUCalgarySRS) object. 
                If not supplied, it will create the object with some settings carried over from the PyUCRio 
                object. Note that specifying this is for advanced users and only necessary a few special use-cases.

        Raises:
            pyucrio.exceptions.PyUCRioInitializationError: an error was encountered during initialization 
                of the paths
        """
        # initialize path parameters
        self.__download_output_root_path = download_output_root_path

        # initialize api parameters
        self.__api_base_url = api_base_url
        if (api_base_url is None):
            self.__api_base_url = self.__DEFAULT_API_BASE_URL
        self.__api_headers = api_headers
        if (api_headers is None):
            self.__api_headers = self.__DEFAULT_API_HEADERS
        self.__api_timeout = api_timeout
        if (api_timeout is None):
            self.__api_timeout = self.__DEFAULT_API_TIMEOUT

        # initialize paths
        self.__initialize_paths()

        # initialize PyUCalgarySRS object
        if (srs_obj is None):
            self.__srs_obj = pyucalgarysrs.PyUCalgarySRS(
                api_headers=self.__api_headers,
                api_timeout=self.__api_timeout,
                download_output_root_path=self.download_output_root_path,
            )
        else:
            self.__srs_obj = srs_obj

        # initialize sub-modules
        self.__data = DataManager(self)
        self.__tools = tools_module

    # ------------------------------------------
    # properties for submodule managers
    # ------------------------------------------
    @property
    def data(self):
        """
        Access to the `data` submodule from within a PyUCRio object.
        """
        return self.__data

    @property
    def tools(self):
        """
        Access to the `tools` submodule from within a PyUCRio object.
        """
        return self.__tools

    # ------------------------------------------
    # properties for configuration parameters
    # ------------------------------------------
    @property
    def api_base_url(self):
        """
        Property for the API base URL. See above for details.
        """
        return self.__api_base_url

    @api_base_url.setter
    def api_base_url(self, value: str):
        if (value is None):
            self.__api_base_url = self.__DEFAULT_API_BASE_URL
        else:
            self.__api_base_url = value
            self.__srs_obj.api_base_url = value

    @property
    def api_headers(self):
        """
        Property for the API headers. See above for details.
        """
        return self.__api_headers

    @api_headers.setter
    def api_headers(self, value: Dict):
        self.__srs_obj.api_headers = value
        self.__api_headers = self.__srs_obj.api_headers

    @property
    def api_timeout(self):
        """
        Property for the API timeout. See above for details.
        """
        return self.__api_timeout

    @api_timeout.setter
    def api_timeout(self, value: int):
        new_timeout = self.__DEFAULT_API_TIMEOUT
        if (value is not None):
            new_timeout = value
        self.__api_timeout = new_timeout
        self.__srs_obj.api_timeout = new_timeout

    @property
    def download_output_root_path(self):
        """
        Property for the download output root path. See above for details.
        """
        return str(self.__download_output_root_path)

    @download_output_root_path.setter
    def download_output_root_path(self, value: str):
        self.__download_output_root_path = value
        self.__initialize_paths()
        self.__srs_obj.download_output_root_path = self.__download_output_root_path

    @property
    def srs_obj(self):
        """
        Property for the PyUCalgarySRS object. See above for details.
        """
        return self.__srs_obj

    @srs_obj.setter
    def srs_obj(self, new_obj: pyucalgarysrs.PyUCalgarySRS):
        self.__srs_obj = new_obj

    # -----------------------------
    # special methods
    # -----------------------------
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return ("PyUCRio(download_output_root_path='%s', api_base_url='%s', api_headers=%s, api_timeout=%s, srs_obj=PyUCalgarySRS(...))" % (
            self.__download_output_root_path,
            self.api_base_url,
            self.api_headers,
            self.api_timeout,
        ))

    # -----------------------------
    # private methods
    # -----------------------------
    def __initialize_paths(self):
        """
        Initialize the `download_output_root_path` directory.

        Raises:
            pyucrio.exceptions.PyUCRioInitializationError: an error was encountered during
                initialization of the paths
        """
        if (self.__download_output_root_path is None):
            self.__download_output_root_path = Path("%s/pyucrio_data" % (str(Path.home())))
        try:
            os.makedirs(self.download_output_root_path, exist_ok=True)
        except IOError as e:  # pragma: nocover
            raise PyUCRioInitializationError("Error during output path creation: %s" % str(e)) from e

    # -----------------------------
    # public methods
    # -----------------------------
    def purge_download_output_root_path(self):
        """
        Delete all files in the `download_output_root_path` directory. Since the
        library downloads data to this directory, over time it can grow too large
        and the user can risk running out of space. This method is here to assist
        with easily clearing out this directory.

        Note that it also deletes all files in the PyUCalgarySRS object's 
        download_output_root_path path as well. Normally, these two paths are the 
        same, but it can be different if the user specifically changes it. 

        Raises:
            pyucrio.exceptions.PyUCRioPurgeError: an error was encountered during the purge operation
        """
        try:
            # purge pyucrio path
            for item in os.listdir(self.download_output_root_path):
                item = Path(self.download_output_root_path) / item
                if (os.path.isdir(item) is True and self.srs_obj.read_tar_temp_path not in str(item)):
                    shutil.rmtree(item)
                elif (os.path.isfile(item) is True):
                    os.remove(item)

            # purge pyucalgarysrs path
            self.__srs_obj.purge_download_output_root_path()
        except Exception as e:  # pragma: nocover
            raise PyUCRioPurgeError("Error while purging download output root path: %s" % (str(e))) from e

    def show_data_usage(self, order: Literal["name", "size"] = "size", return_dict: bool = False) -> Any:
        """
        Print the volume of data existing in the download_output_root_path, broken down
        by dataset. Alternatively return the information in a dictionary.
        
        This can be a helpful tool for managing your disk space.

        Args:
            order (bool): 
                Order results by either `size` or `name`. Default is `size`.

            return_dict (bool): 
                Instead of printing the data usage information, return the information as a dictionary.

        Returns:
            Printed output. If `return_dict` is True, then it will instead return a dictionary with the
            disk usage information.
        
        Notes:
            Note that size on disk may differ slightly from the values determined by this 
            routine. For example, the results here will be slightly different than the output
            of a 'du' command on *nix systems.
        """
        # init
        total_size = 0
        download_pathlib_path = Path(self.download_output_root_path)

        # get list of dataset paths
        dataset_paths = []
        for f in os.listdir(download_pathlib_path):
            path_f = download_pathlib_path / f
            if (os.path.isdir(path_f) is True and str(path_f) != self.srs_obj.read_tar_temp_path):
                dataset_paths.append(path_f)

        # get size of each dataset path
        dataset_dict = {}
        longest_path_len = 0
        for dataset_path in dataset_paths:
            # get size
            dataset_size = 0
            for dirpath, _, filenames in os.walk(dataset_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if (os.path.isfile(filepath) is True):
                        dataset_size += os.path.getsize(filepath)

            # check if this is the longest path name
            path_basename = os.path.basename(dataset_path)
            if (longest_path_len == 0):
                longest_path_len = len(path_basename)
            elif (len(path_basename) > longest_path_len):
                longest_path_len = len(path_basename)

            # set dict
            dataset_dict[path_basename] = {
                "path_obj": dataset_path,
                "size_bytes": dataset_size,
                "size_str": humanize.naturalsize(dataset_size),
            }

            # add to total
            total_size += dataset_size

        # return dictionary
        if (return_dict is True):
            return dataset_dict

        # print table
        #
        # order into list
        order_key = "size_bytes" if order == "size" else order
        ordered_list = []
        for path, p_dict in dataset_dict.items():
            this_dict = p_dict
            this_dict["name"] = path
            ordered_list.append(this_dict)
        if (order == "size"):
            ordered_list = reversed(sorted(ordered_list, key=lambda x: x[order_key]))
        else:
            ordered_list = sorted(ordered_list, key=lambda x: x[order_key])

        # set column data
        table_names = []
        table_sizes = []
        for item in ordered_list:
            table_names.append(item["name"])
            table_sizes.append(item["size_str"])

        # set header values
        table_headers = ["Dataset name", "Size"]

        # print as table
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t"] * len(table_headers))
        table.set_header_align(["l"] * len(table_headers))
        table.set_cols_align(["l"] * len(table_headers))
        table.header(table_headers)
        for i in range(0, len(table_names)):
            table.add_row([table_names[i], table_sizes[i]])
        print(table.draw())

        print("\nTotal size: %s" % (humanize.naturalsize(total_size)))
