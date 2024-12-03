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
Data analysis toolkit for working with riometer data available from UCalgary
Space Remote Sensing.

This portion of the PyUCRio library allows you to easily generate basic plots
for riometer data, and common manipulations.

Example:
    For shorter function calls, you can initialize the tools submodule using like so:

    ```
    import pyucrio
    rio = pyucrio.PyUCRio()
    rt = rio.tools
    ```
"""

# pull in top-level functions
from ._util import set_theme
from ._plot import plot

# pull in classes

# pull in submodules

__all__ = [
    # sub-modules

    # top level functions
    "set_theme",
    "plot",

    # classes
]
