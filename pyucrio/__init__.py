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
The PyUCRio package provides data access and analysis support for working 
with UCalgary Riometer instruments, such as NORSTAR Riometers, and SWAN Hyper
Spectral Riometers.

For an overview of usage and examples, visit the
[UCalgary Space Remote Sensing Open Data Platform](https://data.phys.ucalgary.ca), 
view the [crib sheets](https://data.phys.ucalgary.ca/working_with_data/index.html#crib-sheets),
or explore the examples contained in the [Github repository](https://github.com/ucalgary-srs/pyUCRio/tree/main/examples).

Installation:
```console
$ pip install pyucrio
```

Basic usage:
```python
> import pyucrio
> rio = pyucrio.PyUCRio()
```
"""

# versioning info
__version__ = "1.6.0"

# documentation excludes
__pdoc__ = {"pyucrio": False}
__all__ = ["PyUCRio"]

# pull in top level class
from .pyucrio import PyUCRio

# pull in top-level submodules
#
# NOTE: we do this only so that we can access classes within the
# submodules. Without this, they are selectively addressable, such
# as within ipython, but not vscode. Currently, this is ONLY included
# for VSCode's sake. Will take more testing to explore other use-cases.
from . import data
from . import tools

# pull in exceptions
from .exceptions import (
    PyUCRioError,
    PyUCRioInitializationError,
    PyUCRioAPIError,
    PyUCRioPurgeError,
    PyUCRioUnsupportedReadError,
    PyUCRioDownloadError,
)
