URLS=[
"pyucrio/index.html",
"pyucrio/exceptions.html",
"pyucrio/data/index.html",
"pyucrio/data/ucalgary/index.html",
"pyucrio/data/ucalgary/read/index.html",
"pyucrio/tools/index.html",
"pyucrio/tools/classes/index.html"
];
INDEX=[
{
"ref":"pyucrio",
"url":0,
"doc":"The PyUCRio package provides data access and analysis support for working with UCalgary Riometer instruments, such as NORSTAR Riometers, and SWAN Hyper Spectral Riometers. For an overview of usage and examples, visit the [UCalgary Space Remote Sensing Open Data Platform](https: data.phys.ucalgary.ca), view the [crib sheets](https: data.phys.ucalgary.ca/working_with_data/index.html crib-sheets), or explore the examples contained in the [Github repository](https: github.com/ucalgary-srs/pyUCRio/tree/main/examples). Installation:   $ pip install pyucrio   Basic usage:   > import pyucrio > rio = pyucrio.PyUCRio()  "
},
{
"ref":"pyucrio.PyUCRio",
"url":0,
"doc":"The  PyUCRio class is the primary entry point for utilizing this library. It is used to initialize a session, capturing details about API connectivity, environment, and more. All submodules are encapsulated within this class, so any usage of the library starts with creating this object.   import pyucrio rio = pyucrio.PyUCRio()   When working with this object, you can set configuration parameters, such as the destination directory for downloaded data, or API special settings (e.g., timeout, HTTP headers, API key). These parameters can be set when instantiating the object, or after instantiating using the self-contained accessible variables. Attributes: download_output_root_path (str): Destination directory for downloaded data. The default for this path is a subfolder in the user's home directory, such as  /home/user/pyucrio_data in Linux. In Windows and Mac, it is similar. api_base_url (str): URL prefix to use when interacting with the UCalgary Space Remote Sensing API. By default this is set to  https: api.phys.ucalgary.ca . This parameter is primarily used by the development team to test and build new functions using the private staging API. api_timeout (int): The timeout used when communicating with the UCalgary SRS API. This value is represented in seconds, and by default is  10 seconds . progress_bar_backend (str): The progress bar backend to use. Valid choices are 'auto', 'standard', or 'notebook'. Default is 'auto'. This parameter is optional. srs_obj (pyucalgarysrs.PyUCalgarySRS): A [PyUCalgarySRS](https: docs-pyucalgarysrs.phys.ucalgary.ca/ pyucalgarysrs.PyUCalgarySRS) object. If not supplied, it will create the object with some settings carried over from the PyUCRio object. Note that specifying this is for advanced users and only necessary a few special use-cases. Raises: pyucrio.exceptions.PyUCRioInitializationError: an error was encountered during initialization of the paths"
},
{
"ref":"pyucrio.PyUCRio.data",
"url":0,
"doc":"Access to the  data submodule from within a PyUCRio object."
},
{
"ref":"pyucrio.PyUCRio.tools",
"url":0,
"doc":"Access to the  tools submodule from within a PyUCRio object."
},
{
"ref":"pyucrio.PyUCRio.api_base_url",
"url":0,
"doc":"Property for the API base URL. See above for details."
},
{
"ref":"pyucrio.PyUCRio.api_headers",
"url":0,
"doc":"Property for the API headers. See above for details."
},
{
"ref":"pyucrio.PyUCRio.api_timeout",
"url":0,
"doc":"Property for the API timeout. See above for details."
},
{
"ref":"pyucrio.PyUCRio.download_output_root_path",
"url":0,
"doc":"Property for the download output root path. See above for details."
},
{
"ref":"pyucrio.PyUCRio.progress_bar_backend",
"url":0,
"doc":"Property for the progress bar backend. See above for details."
},
{
"ref":"pyucrio.PyUCRio.srs_obj",
"url":0,
"doc":"Property for the PyUCalgarySRS object. See above for details."
},
{
"ref":"pyucrio.PyUCRio.pretty_print",
"url":0,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.PyUCRio.purge_download_output_root_path",
"url":0,
"doc":"Delete all files in the  download_output_root_path directory. Since the library downloads data to this directory, over time it can grow too large and the user can risk running out of space. This method is here to assist with easily clearing out this directory. Note that it also deletes all files in the PyUCalgarySRS object's download_output_root_path path as well. Normally, these two paths are the same, but it can be different if the user specifically changes it. Raises: pyucrio.exceptions.PyUCRioPurgeError: an error was encountered during the purge operation",
"func":1
},
{
"ref":"pyucrio.PyUCRio.show_data_usage",
"url":0,
"doc":"Print the volume of data existing in the download_output_root_path, broken down by dataset. Alternatively return the information in a dictionary. This can be a helpful tool for managing your disk space. Args: order (bool): Order results by either  size or  name . Default is  size . return_dict (bool): Instead of printing the data usage information, return the information as a dictionary. Returns: Printed output. If  return_dict is True, then it will instead return a dictionary with the disk usage information. Notes: Note that size on disk may differ slightly from the values determined by this routine. For example, the results here will be slightly different than the output of a 'du' command on  nix systems.",
"func":1
},
{
"ref":"pyucrio.exceptions",
"url":1,
"doc":"Unique exception classes utilized by PyUCRio. These exceptions can be used to help trap specific errors raised by this library. Note that all exceptions are imported at the root level of the library. They can be referenced using [ pyucrio.PyUCRioError ](exceptions.html pyucrio.exceptions.PyUCRioError) or  pyucrio.exceptions.PyUCRioError ."
},
{
"ref":"pyucrio.exceptions.PyUCRioError",
"url":1,
"doc":"Common base class for all non-exit exceptions."
},
{
"ref":"pyucrio.exceptions.PyUCRioInitializationError",
"url":1,
"doc":"Error occurred during library initialization"
},
{
"ref":"pyucrio.exceptions.PyUCRioAPIError",
"url":1,
"doc":"Error occurred during an API call"
},
{
"ref":"pyucrio.exceptions.PyUCRioPurgeError",
"url":1,
"doc":"Error occurred during purging of download working directory"
},
{
"ref":"pyucrio.exceptions.PyUCRioUnsupportedReadError",
"url":1,
"doc":"Unsupported dataset for read function NOTE: this is primarily a PyUCalgarySRS error"
},
{
"ref":"pyucrio.exceptions.PyUCRioDownloadError",
"url":1,
"doc":"Error occurred during downloading of data NOTE: this is primarily a PyUCalgarySRS error"
},
{
"ref":"pyucrio.data",
"url":2,
"doc":"Instrument data downloading and reading module. This module presently has support for data provided by the University of Calgary, such as NORSTAR Riometers, and SWAN Hyper Spectral Riometers (HSR)."
},
{
"ref":"pyucrio.data.DataManager",
"url":2,
"doc":"The DataManager object is initialized within every PyUCRio object. It acts as a way to access the submodules and carry over configuration information in the super class."
},
{
"ref":"pyucrio.data.DataManager.ucalgary",
"url":2,
"doc":"Access to the  ucalgary submodule from within a PyUCRio object."
},
{
"ref":"pyucrio.data.DataManager.list_datasets",
"url":2,
"doc":"List available datasets from all providers Args: name (str): Supply a name used for filtering. If that name is found in the available dataset names received from the API, it will be included in the results. This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A list of [ Dataset ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Dataset) objects. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.DataManager.get_dataset",
"url":2,
"doc":"Get a specific dataset Args: name (str): The dataset name to get. Case is insensitive. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: The found [ Dataset ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Dataset) object. Raises an exception if not found. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.DataManager.list_datasets_in_table",
"url":2,
"doc":"Print available datasets from all providers in a table Args: name (str): Supply a name used for filtering. If that name is found in the available dataset names received from the API, it will be included in the results. This parameter is optional. max_width (int): Maximum width of the table. Default is  200 . This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: Printed table. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.DataManager.list_observatories",
"url":2,
"doc":"List information about observatories utilized by all providers. Args: instrument_array (str): The instrument array to list observatories for. Valid values are: norstar_riometer, and swan_hsr. uid (str): Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID is found in the available observatories received from the API, it will be included in the results. This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A list of [ Observatory ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Observatory) objects. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.DataManager.list_observatories_in_table",
"url":2,
"doc":"Print available observatories for a given instrument array in a table Args: instrument_array (str): The instrument array to list observatories for. Valid values are: norstar_riometer, and swan_hsr. uid (str): Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID is found in the available observatories received from the API, it will be included in the results. This parameter is optional. max_width (int): Maximum width of the table. Default is  200 . This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: Printed table. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary",
"url":3,
"doc":"Data downloading and reading routines for data provided by the University of Calgary."
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager",
"url":3,
"doc":"The UCalgaryManager object is initialized within every PyUCRio object. It acts as a way to access the submodules and carry over configuration information in the super class."
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.readers",
"url":3,
"doc":"Access to the  read submodule from within a PyUCRio object."
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.list_datasets",
"url":3,
"doc":"List available datasets Args: name (str): Supply a name used for filtering. If that name is found in the available dataset names received from the API, it will be included in the results. This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A list of [ Dataset ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Dataset) objects. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.get_dataset",
"url":3,
"doc":"Get a specific dataset Args: name (str): The dataset name to get. Case is insensitive. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: The found [ Dataset ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Dataset) object. Raises an exception if not found. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.list_observatories",
"url":3,
"doc":"List information about observatories Args: instrument_array (str): The instrument array to list observatories for. Valid values are: norstar_riometer, and swan_hsr. uid (str): Supply a observatory unique identifier used for filtering (usually 4-letter site code). If that UID is found in the available observatories received from the API, it will be included in the results. This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A list of [ Observatory ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Observatory) objects. Raises: pyucrio.exceptions.PyUCRioAPIError: An API error was encountered.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.list_supported_read_datasets",
"url":3,
"doc":"List the datasets which have file reading capabilities supported. Returns: A list of the dataset names with file reading support.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.is_read_supported",
"url":3,
"doc":"Check if a given dataset has file reading support. Not all datasets available in the UCalgary Space Remote Sensing Open Data Platform have special readfile routines in this library. This is because some datasets are handled by other libraries (ie. PyAuroraX for ASI data), or are in basic formats such as JPG or PNG, so unique functions aren't necessary. We leave it up to the user to open those basic files in whichever way they prefer. Use the  list_supported_read_datasets() function to see all datasets that have special file reading functionality in this library. Args: dataset_name (str): The dataset name to check if file reading is supported. This parameter is required. Returns: Boolean indicating if file reading is supported.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.download",
"url":3,
"doc":"Download data from the UCalgary Space Remote Sensing Open Data Platform. The parameters  dataset_name ,  start , and  end are required. All other parameters are optional. Args: dataset_name (str): Name of the dataset to download data for. Use the  list_datasets() function to get the possible values for this parameter. One example is \"SWAN_HSR_K0_H5\". Note that dataset names are case sensitive. This parameter is required. start (datetime.datetime): Start timestamp to use (inclusive), expected to be in UTC. Any timezone data will be ignored. This parameter is required. end (datetime.datetime): End timestamp to use (inclusive), expected to be in UTC. Any timezone data will be ignored. This parameter is required. site_uid (str): The site UID to filter for. If specified, data will be downloaded for only the site matching the given value. If excluded, data for all available sites will be downloaded. An example value could be 'gill', meaning all data from the Gillam observatory will be downloaded for the given dataset name, start, and end times. This parameter is optional. n_parallel (int): Number of data files to download in parallel. Default value is 5. Adjust as needed for your internet connection. This parameter is optional. overwrite (bool): By default, data will not be re-downloaded if it already exists locally. Use the  overwrite parameter to force re-downloading. Default is  False . This parameter is optional. progress_bar_disable (bool): Disable the progress bar. Default is  False . This parameter is optional. progress_bar_ncols (int): Number of columns for the progress bar (straight passthrough of the  ncols parameter in a tqdm progress bar). This parameter is optional. See Notes section below for further information. progress_bar_ascii (str): ASCII value to use when constructing the visual aspect of the progress bar (straight passthrough of the  ascii parameter in a tqdm progress bar). This parameter is optional. See Notes section below for further details. progress_bar_desc (str): Description value to use when constructing the visual aspect of the progress bar (straight passthrough of the  desc parameter in a tqdm progress bar). This parameter is optional. See notes section below for further details. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A [ FileDownloadResult ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.FileDownloadResult) object containing details about what data files were downloaded. Raises: pyucrio.exceptions.PyUCRioDownloadError: an error was encountered while downloading a specific file pyucrio.exceptions.PyUCRioAPIError: an API error was encountered Notes:     The  progress_bar_ parameters can be used to enable/disable/adjust the progress bar. Excluding the  progress_bar_disable parameter, all others are straight pass-throughs to the tqdm progress bar function. The  progress_bar_ncols parameter allows for adjusting the width. The  progress_bar_ascii parameter allows for adjusting the appearance of the progress bar. And the  progress_bar_desc parameter allows for adjusting the description at the beginning of the progress bar. Further details can be found on the [tqdm documentation](https: tqdm.github.io/docs/tqdm/ tqdm-objects). Data downloading will use the  download_data_root_path variable within the super class' object ([ PyUCRio ]( / /index.html pyucrio.PyUCRio to determine where to save data to. If you'd like to change this path to somewhere else you can change that variable before your download() call, like so:   import pyucrio rio = pyucrio.PyUCRio() rio.data_download_root_path = \"some_new_path\" rio.data.download(dataset_name, start, end)  ",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.download_using_urls",
"url":3,
"doc":"Download data from the UCalgary Space Remote Sensing Open Data Platform using a FileListingResponse object. This would be used in cases where more customization is needed than the generic  download() function. One example of using this function would start by using  get_urls() to retrieve the list of URLs available for download, then further process this list to fewer files based on some other requirement (ie. time down-sampling such as one file per hour). Lastly using this function to download the new custom set URLs. Args: file_listing_response (FileListingResponse): A [ FileListingResponse ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.FileListingResponse) object returned from a  get_urls() call, which contains a list of URLs to download for a specific dataset. This parameter is required. n_parallel (int): Number of data files to download in parallel. Default value is 5. Adjust as needed for your internet connection. This parameter is optional. overwrite (bool): By default, data will not be re-downloaded if it already exists locally. Use the  overwrite parameter to force re-downloading. Default is  False . This parameter is optional. progress_bar_disable (bool): Disable the progress bar. Default is  False . This parameter is optional. progress_bar_ncols (int): Number of columns for the progress bar (straight passthrough of the  ncols parameter in a tqdm progress bar). This parameter is optional. See Notes section below for further information. progress_bar_ascii (str): ASCII value to use when constructing the visual aspect of the progress bar (straight passthrough of the  ascii parameter in a tqdm progress bar). This parameter is optional. See Notes section below for further details. progress_bar_desc (str): Description value to use when constructing the visual aspect of the progress bar (straight passthrough of the  desc parameter in a tqdm progress bar). This parameter is optional. See notes section below for further details. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A [ FileDownloadResult ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.FileDownloadResult) object containing details about what data files were downloaded. Raises: pyucrio.exceptions.PyUCRioDownloadError: an error was encountered while downloading a specific file pyucrio.exceptions.PyUCRioAPIError: an API error was encountered Notes:     The  progress_bar_ parameters can be used to enable/disable/adjust the progress bar. Excluding the  progress_bar_disable parameter, all others are straight pass-throughs to the tqdm progress bar function. The  progress_bar_ncols parameter allows for adjusting the width. The  progress_bar_ascii parameter allows for adjusting the appearance of the progress bar. And the  progress_bar_desc parameter allows for adjusting the description at the beginning of the progress bar. Further details can be found on the [tqdm documentation](https: tqdm.github.io/docs/tqdm/ tqdm-objects). Data downloading will use the  download_data_root_path variable within the super class' object ([ PyUCRio ]( / /index.html pyucrio.PyUCRio to determine where to save data to. If you'd like to change this path to somewhere else you can change that variable before your download() call, like so:   import pyucrio rio = pyucrio.PyUCRio() rio.data_download_root_path = \"some_new_path\" rio.data.download(dataset_name, start, end)  ",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.get_urls",
"url":3,
"doc":"Get URLs of data files The parameters  dataset_name ,  start , and  end are required. All other parameters are optional. Args: dataset_name (str): Name of the dataset to download data for. Use the  list_datasets() function to get the possible values for this parameter. One example is \"SWAN_HSR_K0_H5\". Note that dataset names are case sensitive. This parameter is required. start (datetime.datetime): Start timestamp to use (inclusive), expected to be in UTC. Any timezone data will be ignored. This parameter is required. end (datetime.datetime): End timestamp to use (inclusive), expected to be in UTC. Any timezone data will be ignored. This parameter is required. site_uid (str): The site UID to filter for. If specified, data will be downloaded for only the site matching the given value. If excluded, data for all available sites will be downloaded. An example value could be 'gill', meaning all data from the Gillam observatory will be downloaded for the given dataset name, start, and end times. This parameter is optional. timeout (int): Represents how many seconds to wait for the API to send data before giving up. The default is 10 seconds, or the  api_timeout value in the super class'  pyucrio.PyUCRio object. This parameter is optional. Returns: A [ FileListingResponse ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.FileListingResponse) object containing a list of the available URLs, among other values. Raises: pyucrio.exceptions.PyUCRioAPIError: an API error was encountered",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.UCalgaryManager.read",
"url":3,
"doc":"Read in data files for a given dataset. Note that only one type of dataset's data should be read in using a single call. Args: dataset (Dataset): The dataset object for which the files are associated with. This parameter is required. file_list (List[str], List[Path], str, Path): The files to read in. Absolute paths are recommended, but not technically necessary. This can be a single string for a file, or a list of strings to read in multiple files. This parameter is required. n_parallel (int): Number of data files to read in parallel using multiprocessing. Default value is 1. Adjust according to your computer's available resources. This parameter is optional. no_metadata (bool): Skip reading of metadata. This is a minor optimization if the metadata is not needed. Default is  False . This parameter is optional. start_time (datetime.datetime): The start timestamp to read data onwards from (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  end_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will assume the start time is the timestamp of the first record in the first file supplied (ie. beginning of the supplied data). This parameter is optional. end_time (datetime.datetime): The end timestamp to read data up to (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  start_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will it will assume the end time is the timestamp of the last record in the last file supplied (ie. end of the supplied data). This parameter is optional. quiet (bool): Do not print out errors while reading data files, if any are encountered. Any files that encounter errors will be, as usual, accessible via the  problematic_files attribute of the returned  Data object. This parameter is optional. Returns: A [ Data ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Data) object containing the data read in, among other values. Raises: pyucrio.exceptions.PyUCRioUnsupportedReadError: an unsupported dataset was used when trying to read files. pyucrio.exceptions.PyUCRioError: a generic read error was encountered",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.Observatory",
"url":3,
"doc":"Representation for an observatory. Attributes: uid (str): The 4-letter unique identifier (traditionally referred to as the site UID) full_name (str): Full location string for the observatory geodetic_latitude (float): Geodetic latitude for the observatory, in decimal format (-90 to 90) geodetic_longitude (float): Geodetic longitude for the observatory, in decimal format (-180 to 180) provider (str): Data provider"
},
{
"ref":"pyucrio.data.ucalgary.Observatory.pretty_print",
"url":3,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.Dataset",
"url":3,
"doc":"A dataset available from the UCalgary Space Remote Sensing API, with possibly support for downloading and/or reading. Attributes: name (str): Dataset name short_description (str): A short description about the dataset long_description (str): A longer description about the dataset data_tree_url (str): The data tree URL prefix. Used for saving data locally with a similar data tree structure compared to the UCalgary Open Data archive. file_listing_supported (bool): Flag indicating if file listing (downloading) is supported for this dataset. file_reading_supported (bool): Flag indicating if file reading is supported for this dataset. file_time_resolution (str): Time resolution of the files for this dataset, represented as a string. Possible values are: 1min, 1hr, 1day, not_applicable. level (str): Dataset level as per L0/L1/L2/etc standards. doi (str): Dataset DOI unique identifier. doi_details (str): Further details about the DOI. citation (str): String to use when citing usage of the dataset. provider (str): Data provider. supported_libraries (List[str]): Libraries that support usage of this dataset."
},
{
"ref":"pyucrio.data.ucalgary.Dataset.pretty_print",
"url":3,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult",
"url":3,
"doc":"Representation of the results from a data download call. Attributes: filenames (List[str]): List of downloaded files, as absolute paths of their location on the local machine. count (int): Number of files downloaded total_bytes (int): Cumulative amount of bytes saved on the local machine. output_root_path (str): The root path of where the data was saved to on the local machine. dataset (Dataset): The  Dataset object for this data."
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.filenames",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.count",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.total_bytes",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.output_root_path",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.dataset",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileDownloadResult.pretty_print",
"url":3,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse",
"url":3,
"doc":"Representation of the file listing response from the UCalgary Space Remote Sensing API. Attributes: urls (List[str]): A list of URLs for available data files. path_prefix (str): The URL prefix, which is sed for saving data locally with a similar data tree structure compared to the UCalgary Open Data archive. count (int): The number of URLs available. dataset (Dataset): The  Dataset object for this data. total_bytes (int): The cumulative amount of bytes for the available URLs."
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.urls",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.path_prefix",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.count",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.dataset",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.total_bytes",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.FileListingResponse.pretty_print",
"url":3,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.Data",
"url":3,
"doc":"Representation of the data read in from a  read call. Attributes: data (Any): The loaded data. This can be one of the following types: ndarray, List[Skymap], List[Calibration]. timestamp (List[datetime.datetime]): List of timestamps for the read in data. metadata (List[Dict]): List of dictionaries containing metadata specific to each timestamp/image/record. problematic_files (List[ProblematicFiles]): A list detailing any files that encountered issues during reading. calibrated_data (Any): A calibrated version of the data. Populated and utilized by data analysis libraries. Has a  None value until calibrated data is inserted manually. dataset (Dataset): The  Dataset object for this data."
},
{
"ref":"pyucrio.data.ucalgary.Data.data",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.timestamp",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.metadata",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.problematic_files",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.calibrated_data",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.dataset",
"url":3,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.Data.pretty_print",
"url":3,
"doc":"A special print output for this class.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.read",
"url":4,
"doc":""
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager",
"url":4,
"doc":"The UCalgaryManager object is initialized within every PyUCRio object. It acts as a way to access the submodules and carry over configuration information in the super class."
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager.list_supported_datasets",
"url":4,
"doc":"List the datasets which have file reading capabilities supported. Returns: A list of the dataset names with file reading support.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager.is_supported",
"url":4,
"doc":"Check if a given dataset has file reading support. Not all datasets available in the UCalgary Space Remote Sensing Open Data Platform have special readfile routines in this library. This is because some datasets are handled by other libraries (ie. PyAuroraX for ASI data), or are in basic formats such as JPG or PNG, so unique functions aren't necessary. We leave it up to the user to open those basic files in whichever way they prefer. Use the  list_supported_read_datasets() function to see all datasets that have special file reading functionality in this library. Args: dataset_name (str): The dataset name to check if file reading is supported. This parameter is required. Returns: Boolean indicating if file reading is supported.",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager.read",
"url":4,
"doc":"Read in data files for a given dataset. Note that only one type of dataset's data should be read in using a single call. Args: dataset (Dataset): The dataset object for which the files are associated with. This parameter is required. file_list (List[str], List[Path], str, Path): The files to read in. Absolute paths are recommended, but not technically necessary. This can be a single string for a file, or a list of strings to read in multiple files. This parameter is required. n_parallel (int): Number of data files to read in parallel using multiprocessing. Default value is 1. Adjust according to your computer's available resources. This parameter is optional. no_metadata (bool): Skip reading of metadata. This is a minor optimization if the metadata is not needed. Default is  False . This parameter is optional. start_time (datetime.datetime): The start timestamp to read data onwards from (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  end_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will assume the start time is the timestamp of the first record in the first file supplied (ie. beginning of the supplied data). This parameter is optional. end_time (datetime.datetime): The end timestamp to read data up to (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  start_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will it will assume the end time is the timestamp of the last record in the last file supplied (ie. end of the supplied data). This parameter is optional. quiet (bool): Do not print out errors while reading data files, if any are encountered. Any files that encounter errors will be, as usual, accessible via the  problematic_files attribute of the returned  Data object. This parameter is optional. Returns: A [ Data ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Data) object containing the data read in, among other values. Raises: pyucrio.exceptions.PyUCRioUnsupportedReadError: an unsupported dataset was used when trying to read files. pyucrio.exceptions.PyUCRioError: a generic read error was encountered",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager.read_norstar_riometer",
"url":4,
"doc":"Read in NORSTAR Riometer data (K0 and K2 ASCII files). Args: file_list (List[str], List[Path], str, Path): The files to read in. Absolute paths are recommended, but not technically necessary. This can be a single string for a file, or a list of strings to read in multiple files. This parameter is required. n_parallel (int): Number of data files to read in parallel using multiprocessing. Default value is 1. Adjust according to your computer's available resources. This parameter is optional. no_metadata (bool): Skip reading of metadata. This is a minor optimization if the metadata is not needed. Default is  False . This parameter is optional. start_time (datetime.datetime): The start timestamp to read data onwards from (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  end_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will assume the start time is the timestamp of the first record in the first file supplied (ie. beginning of the supplied data). This parameter is optional. end_time (datetime.datetime): The end timestamp to read data up to (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  start_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will it will assume the end time is the timestamp of the last record in the last file supplied (ie. end of the supplied data). This parameter is optional. quiet (bool): Do not print out errors while reading data files, if any are encountered. Any files that encounter errors will be, as usual, accessible via the  problematic_files attribute of the returned  Data object. This parameter is optional. dataset (Dataset): The dataset object for which the files are associated with. This parameter is optional. Returns: A [ Data ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Data) object containing the data read in, among other values. Raises: pyucrio.exceptions.PyUCRioError: a generic read error was encountered",
"func":1
},
{
"ref":"pyucrio.data.ucalgary.read.ReadManager.read_swan_hsr",
"url":4,
"doc":"Read in SWAN Hyper Spectral Riometer (HSR) data (K0 H5 files). Args: file_list (List[str], List[Path], str, Path): The files to read in. Absolute paths are recommended, but not technically necessary. This can be a single string for a file, or a list of strings to read in multiple files. This parameter is required. n_parallel (int): Number of data files to read in parallel using multiprocessing. Default value is 1. Adjust according to your computer's available resources. This parameter is optional. no_metadata (bool): Skip reading of metadata. This is a minor optimization if the metadata is not needed. Default is  False . This parameter is optional. start_time (datetime.datetime): The start timestamp to read data onwards from (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  end_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will assume the start time is the timestamp of the first record in the first file supplied (ie. beginning of the supplied data). This parameter is optional. end_time (datetime.datetime): The end timestamp to read data up to (inclusive). This can be utilized to read a portion of a data file, and could be paired with the  start_time parameter. This tends to be utilized for datasets that are hour or day-long files where it is possible to only read a smaller bit of that file. If not supplied, it will it will assume the end time is the timestamp of the last record in the last file supplied (ie. end of the supplied data). This parameter is optional. quiet (bool): Do not print out errors while reading data files, if any are encountered. Any files that encounter errors will be, as usual, accessible via the  problematic_files attribute of the returned  Data object. This parameter is optional. dataset (Dataset): The dataset object for which the files are associated with. This parameter is optional. Returns: A [ Data ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Data) object containing the data read in, among other values. Raises: pyucrio.exceptions.PyUCRioError: a generic read error was encountered",
"func":1
},
{
"ref":"pyucrio.tools",
"url":5,
"doc":"Data analysis toolkit for working with riometer data available from UCalgary Space Remote Sensing. This portion of the PyUCRio library allows you to easily generate basic plots for riometer data, and common manipulations. Example: For shorter function calls, you can initialize the tools submodule using like so:  import pyucrio rio = pyucrio.PyUCRio() rt = rio.tools  "
},
{
"ref":"pyucrio.tools.ToolsManager",
"url":5,
"doc":"The ToolsManager object is initialized within every PyUCRio object. It acts as a way to access the submodules and carry over configuration information in the super class."
},
{
"ref":"pyucrio.tools.ToolsManager.set_theme",
"url":5,
"doc":"A handy wrapper for setting the matplotlib global theme. Common choices are  light ,  dark , or  default . Args: theme (str): Theme name. Common choices are  light ,  dark , or  default . If default, then matplotlib theme settings will be fully reset to their defaults. Additional themes can be found on the [matplotlib documentation](https: matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)",
"func":1
},
{
"ref":"pyucrio.tools.ToolsManager.plot",
"url":5,
"doc":"Plot riometer data as combined line plots, or a stack plot. Used for plotting both single-frequency riometer data and Hyper-Spectral Riometer (HSR) data, either separately or together. Args: rio_data (Data | List[Data]): The data to be plotted, represented as a single, or list, of [ Data ](https: docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html pyucalgarysrs.data.classes.Data) objects containing riometer data. All objects will be plotted according to plot settings. absorption (bool): Plot absorption data, as opposed to raw data. Defaults to False. stack_plot (bool): Render plots into a stack-plot of subplots for each data array. Defaults to False. downsample_seconds (int): The window size for smoothing data before plotting. Default is 1, which is the same as the data temporal resolutions, meaning no smoothing will occur. hsr_bands (int | list[int]): The band indices to be plotted, specifically applicable to HSR data. By default, all HSR bands will be plotted. color (str | list[str]): Matplotlib color name(s) to cycle through when plotting. figsize (list | tuple): The overall figure size. Default is None, determined automatically by matplotlib. title (str): The figure title. Default is no title. date_format (str): The date format to use when plotting, represented as a string. For example, '%H' to format the times as hours, \"%H:%M\" to format as hours and minutes, or \"%Y-%m-%d\" to format as the year-month-day. Default of \"%H\" to format as hours. xtitle (str): The x-axis title. Default is no title. ytitle (str): The y-axis title. Default is no title. xrange (list[datetime.datetime]): The start and end time ranges for x-axis plotting. Default is all x-axis values (full range). yrange (list[int | float]): The [min, max] y-values to use for plotting. linestyle (str | list[str]): Matplotlib linestyle names to cycle through for plotting. returnfig (bool): Instead of displaying the image, return the matplotlib figure object. This allows for further plot manipulation, for example, adding labels or a title in a different location than the default. Remember - if this parameter is supplied, be sure that you close your plot after finishing work with it. This can be achieved by doing  plt.close(fig) . Note that this method cannot be used in combination with  savefig . savefig (bool): Save the displayed image to disk instead of displaying it. The parameter savefig_filename is required if this parameter is set to True. Defaults to  False . savefig_filename (str): Filename to save the image to. Must be specified if the savefig parameter is set to True. savefig_quality (int): Quality level of the saved image. This can be specified if the savefig_filename is a JPG image. If it is a PNG, quality is ignored. Default quality level for JPGs is matplotlib/Pillow's default of 75%. Returns: The displayed plot, by default. If  savefig is set to True, nothing will be returned. If  returnfig is set to True, the plotting variables  (fig, axes) will be returned. Raises: ValueError: issue with supplied parameters.",
"func":1
},
{
"ref":"pyucrio.tools.classes",
"url":6,
"doc":"Class definitions for data analysis objects."
}
]