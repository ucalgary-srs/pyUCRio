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

# pull in classes (none yet)

# imports for this file
import datetime
from pyucalgarysrs.data.classes import Data
from ._util import set_theme as func_set_theme
from ._plot import plot as func_plot

# pull in submodules
from .site_map import SiteMapManager

# typing imports
from typing import Optional, Tuple, Union, Any, List

__all__ = [
    "ToolsManager",
]


class ToolsManager:
    """
    The ToolsManager object is initialized within every PyUCRio object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    # ------------------------------------------
    # functions available at this manager level
    # ------------------------------------------
    def __init__(self, ucrio_obj):
        self.__ucrio_obj = ucrio_obj

        # initialize sub-modules
        self.__site_map = SiteMapManager(self.__ucrio_obj)

    # ------------------------------------------
    # properties for submodule managers
    # ------------------------------------------
    @property
    def site_map(self):
        """
        Access to the `site_map` submodule from within a PyAuroraX object.
        """
        return self.__site_map

    def set_theme(self, theme: str) -> None:
        """
        A handy wrapper for setting the matplotlib global theme. Common choices are `light`, 
        `dark`, or `default`.

        Args:
            theme (str): 
                Theme name. Common choices are `light`, `dark`, or `default`. If default, then
                matplotlib theme settings will be fully reset to their defaults.

                Additional themes can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
        """
        return func_set_theme(theme)

    def plot(self,
             rio_data: Union[Data, List[Data]],
             absorption: bool = False,
             stack_plot: bool = False,
             downsample_seconds: int = 1,
             hsr_bands: Optional[Union[int, List[int]]] = None,
             color: Optional[Union[str, List[str]]] = None,
             figsize: Optional[Tuple[int, int]] = None,
             title: Optional[str] = None,
             date_format: Optional[str] = None,
             xtitle: Optional[str] = None,
             ytitle: Optional[str] = None,
             xrange: Optional[Tuple[datetime.datetime, datetime.datetime]] = None,
             yrange: Optional[Union[Tuple[float, float], Tuple[int, int]]] = None,
             linestyle: Optional[Union[str, List[str]]] = '-',
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Plot riometer data as combined line plots, or a stack plot. Used for plotting both single-frequency
        riometer data and Hyper-Spectral Riometer (HSR) data, either separately or together. 

        Args:
            rio_data (Data | List[Data]): 
                The data to be plotted, represented as a single, or list, of 
                [`Data`](https://docs-pyucalgarysrs.phys.ucalgary.ca/data/classes.html#pyucalgarysrs.data.classes.Data)
                objects containing riometer data. All objects will be plotted according to plot settings.

            absorption (bool): 
                Plot absorption data, as opposed to raw data. Defaults to False.

            stack_plot (bool): 
                Render plots into a stack-plot of subplots for each data array. Defaults to False. 

            downsample_seconds (int): 
                The window size for smoothing data before plotting. Default is 1, which is the same as the data
                temporal resolutions, meaning no smoothing will occur.

            hsr_bands (int | list[int]): 
                The band indices to be plotted, specifically applicable to HSR data. By default, all HSR bands
                will be plotted.

            color (str | list[str]): 
                Matplotlib color name(s) to cycle through when plotting.

            figsize (list | tuple): 
                The overall figure size. Default is None, determined automatically by matplotlib.

            title (str): 
                The figure title. Default is no title.

            date_format (str): 
                The date format to use when plotting, represented as a string. For example, '%H' to format the 
                times as hours, "%H:%M" to format as hours and minutes, or "%Y-%m-%d" to format as the year-month-day.
                Default of "%H" to format as hours.

            xtitle (str): 
                The x-axis title. Default is no title.
            
            ytitle (str): 
                The y-axis title. Default is no title.

            xrange (list[datetime.datetime]): 
                The start and end time ranges for x-axis plotting. Default is all x-axis values (full range).

            yrange (list[int | float]): 
                The [min, max] y-values to use for plotting.

            linestyle (str | list[str]): 
                Matplotlib linestyle names to cycle through for plotting.

            returnfig (bool): 
                Instead of displaying the image, return the matplotlib figure object. This allows for further plot 
                manipulation, for example, adding labels or a title in a different location than the default. 
                
                Remember - if this parameter is supplied, be sure that you close your plot after finishing work 
                with it. This can be achieved by doing `plt.close(fig)`. 
                
                Note that this method cannot be used in combination with `savefig`.

            savefig (bool): 
                Save the displayed image to disk instead of displaying it. The parameter savefig_filename is required if 
                this parameter is set to True. Defaults to `False`.

            savefig_filename (str): 
                Filename to save the image to. Must be specified if the savefig parameter is set to True.

            savefig_quality (int): 
                Quality level of the saved image. This can be specified if the savefig_filename is a JPG image. If it
                is a PNG, quality is ignored. Default quality level for JPGs is matplotlib/Pillow's default of 75%.
            
        Returns:
            The displayed plot, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, axes)` will be returned.

        Raises:
            ValueError: issue with supplied parameters.
        """
        return func_plot(rio_data, absorption, stack_plot, downsample_seconds, hsr_bands, color, figsize, title, date_format, xtitle, ytitle, xrange,
                         yrange, linestyle, returnfig, savefig, savefig_filename, savefig_quality)
