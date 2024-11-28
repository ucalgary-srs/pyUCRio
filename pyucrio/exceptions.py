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
"""
Unique exception classes utilized by PyUCRio. These exceptions can be used 
to help trap specific errors raised by this library.

Note that all exceptions are imported at the root level of the library. They
can be referenced using [`pyucrio.PyUCRioError`](exceptions.html#pyucrio.exceptions.PyUCRioError) 
or `pyucrio.exceptions.PyUCRioError`.
"""


class PyUCRioError(Exception):

    def __init__(self, *args, **kwargs):
        super(PyUCRioError, self).__init__(*args, **kwargs)  # pragma: no cover


class PyUCRioInitializationError(PyUCRioError):
    """
    Error occurred during library initialization
    """
    pass


class PyUCRioAPIError(PyUCRioError):
    """
    Error occurred during an API call
    """
    pass


class PyUCRioPurgeError(PyUCRioError):
    """
    Error occurred during purging of download working directory
    """
    pass


class PyUCRioUnsupportedReadError(PyUCRioError):
    """
    Unsupported dataset for read function

    NOTE: this is primarily a PyUCalgarySRS error
    """
    pass


class PyUCRioDownloadError(PyUCRioError):
    """
    Error occurred during downloading of data

    NOTE: this is primarily a PyUCalgarySRS error
    """
    pass
