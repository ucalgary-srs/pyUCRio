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
Class representation for a FoV map.
"""

import os
import datetime
import pyproj
import aacgmv2
import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs
from typing import List, Dict, Tuple, Sequence, Union, Optional, Any
from numpy import ndarray
from ..._util import show_warning


class SiteMap:
    """
    Class representation for a generated site map.

    Attributes:
        cartopy_projection (cartopy.crs.Projection): 
            Cartopy projection to utilize.

        site_uid_list (list or str): 
            The sites included in this SiteMap object.

        site_locations (list or Dict[str, ndarry]): 
            The geodetic coordinates of the sites included in this SiteMap object.

        instrument_array (list or str): 
            String giving the name of the instrument(s) that the site locations 
            correspond to.

        data_availability (list[Dict[str, bool]]): 
            Booleans to specify which sites have available data.

        color (list or str): 
            String specifying the color to associate with each set of sites for plotting.
        
        symbol (list or str): 
            String specifying the matplotlib.pyplot marker style to associate with each
            set of sites for plotting.
        
        sym_size (list or int): 
            Int specifying the marker size to associate with each set of sites for plotting.
            Default is 1.
        
        contour_data (Dict[str, List[Any]]): 
            Generated contour data.
    """

    def __init__(self, cartopy_projection: cartopy.crs.Projection, site_uid_list: List[List[str]], site_locations: List[Dict[str, ndarray]],
                 instrument_array: List[str], data_availability: Optional[List[Dict[str, bool]]], color: List[str], symbol: List[str],
                 sym_size: List[int], contour_data, ucrio_obj):

        # Public vars
        self.cartopy_projection = cartopy_projection
        self.site_uid_list = site_uid_list
        self.site_locations = site_locations
        self.instrument_array = instrument_array
        self.data_availability = data_availability
        self.color = color
        self.sym_size = sym_size
        self.symbol = symbol
        self.contour_data = contour_data

        # Private vars
        self.__ucrio_obj = ucrio_obj

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:

        # set special strings
        n_instruments = len(self.site_locations)
        n_sites = 0
        for i in range(0, n_instruments):
            n_sites += len(self.site_locations[i].keys())

        locations_str = "Dict[%d site(s) across %d instrument(s)]" % (n_sites, n_instruments)

        # return
        return "SiteMap(cartopy_projection=Projection(%s), site_locations=%s, site_uid_list=%s, instrument_array(s)=%s)" % (
            self.cartopy_projection, locations_str, self.site_uid_list.__repr__(), self.instrument_array)

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set special strings
        cartopy_projection_str = "Projection(%s)" % (self.cartopy_projection.to_string())

        n_instruments = len(self.site_locations)
        n_sites = 0
        for i in range(0, n_instruments):
            n_sites += len(self.site_locations[i].keys())

        locations_str = "Dict[%d site(s) across %d instrument(s)]" % (n_sites, n_instruments)

        # print
        print("SiteMap:")
        print("  %-23s: %s" % ("cartopy_projection", cartopy_projection_str))
        print("  %-19s: %s" % ("instrument_array", self.instrument_array))
        print("  %-19s: %s" % ("site_uid_list", self.site_uid_list))
        print("  %-19s: %s" % ("site_locations", locations_str))

    def add_availability(self, dataset_name: Union[str, List[str]], start: datetime.datetime, end: datetime.datetime):
        """
        Add data availability information to an SiteMap object. Given a start and end time, information
        will be added to the object regarding whether or not each site included in the SiteMap object
        took data in that time range. This is useful for plotting only those sites that took
        data in a given time interval.

        Args:
            dataset_name (str): 
                The name of the dataset to check for data availability (e.g. "TODO:")

            start (datetime.datetime): 
                Defines the start time of the interval to check for data availability.
                
            end (datetime.datetime): 
                Defines the end time of the interval to check for data availability.

        Returns:
            The SiteMap object is updated to hold data availability information, that can be used when
            plotting to omit sites that did not take data during the time interval defined by start and end.

        Raises:
        """
        if isinstance(dataset_name, str):
            dataset_name = [dataset_name]

        data_availability_list = []
        for i, dataset in enumerate(dataset_name):

            if (self.instrument_array[i] is None):
                raise ValueError(
                    "Cannot add data availability to a SiteMap object with no associated instrument_array. Please specify " +  # pragma: nocover
                    "instrument_array upon creation of SiteMap object to enforce data availability.")

            # Check if the requested dataset makes sense for the FOVData
            fov_instrument = self.instrument_array[i].upper()

            if (fov_instrument not in dataset):

                raise ValueError(
                    f"Requested dataset_name: {dataset} does not match the instrument_array: {fov_instrument} contained in this SiteMap object.")

            # Create a dictionary corresponding to the FoV data, that will hold
            # booleans specifying whether or not there is data for each site
            availability_dict = {}
            for site in self.site_locations[i].keys():

                # Request list of all files of requested dataset at requested site
                result = self.__ucrio_obj.data.ucalgary.get_urls(dataset, start, end, site_uid=site)

                # If there are any files within the desired time-range then update availability dict with True, otherwise update False
                if (result.count > 0):
                    availability_dict[site] = True
                else:
                    availability_dict[site] = False

                data_availability_list.append(availability_dict)

        if len(data_availability_list) == 0:
            self.data_availability = None  # pragma: nocover
        else:
            self.data_availability = data_availability_list

    def plot(self,
             map_extent: Sequence[Union[float, int]],
             label: bool = True,
             upper_label: bool = False,
             enforce_data_availability: bool = False,
             figsize: Optional[Tuple[int, int]] = None,
             title: Optional[str] = None,
             ocean_color: Optional[str] = None,
             land_color: str = "gray",
             land_edgecolor: str = "#8A8A8A",
             borders_color: str = "#AEAEAE",
             borders_disable: bool = False,
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Generate a plot of the SiteMap. 
        
        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            map_extent (List[int]): 
                Latitude/longitude range to be visible on the rendered map. This is a list of 4 integers 
                and/or floats, in the order of [min_lon, max_lon, min_lat, max_lat].

            label (bool): 
                Specifies that individual sites will be labelled with their site_uid.
            
            upper_label (bool): 
                Plots site labels in uppercase

            enforce_data_availability (bool): 
                Plot only sites that have data availability. This option may only be used if the SiteMap
                already has data_availibility information associated with it, which is usually achieved
                using the add_availability() method.

            figsize (tuple): 
                The matplotlib figure size to use when plotting. For example `figsize=(14,4)`.

            title (str): 
                The title to display above the plotted site map. Default is no title.

            ocean_color (str): 
                Colour of the ocean. Default is cartopy's default shade of blue. Colours can be supplied
                as a word, or hexcode prefixed with a '#' character (ie. `#55AADD`).
            
            land_color (str): 
                Colour of the land. Default is `gray`. Colours can be supplied as a word, or hexcode 
                prefixed with a '#' character (ie. `#41BB87`).

            land_edgecolor (str): 
                Color of the land edges. Default is `#8A8A8A`. Colours can be supplied as a word, or
                hexcode prefixed with a '#' character.

            borders_color (str): 
                Color of the country borders. Default is `AEAEAE`. Colours can be supplied as a word, or
                hexcode prefixed with a '#' character.
            
            borders_disable (bool): 
                Disbale rendering of the borders. Default is `False`.

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
            The displayed site map, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
        """
        # check return mode
        if (returnfig is True and savefig is True):
            raise ValueError("Only one of returnfig or savefig can be set to True")
        if returnfig is True and (savefig_filename is not None or savefig_quality is not None):
            show_warning("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                         "removing the savefig option parameter(s) as they will be ignored.",
                         stacklevel=1)
        elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
            show_warning("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                         "savefig option parameters will be ignored.",
                         stacklevel=1)

        # Initialize figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes((0, 0, 1, 1), projection=self.cartopy_projection)
        ax.set_extent(map_extent, crs=cartopy.crs.Geodetic())  # type: ignore

        # Add ocean
        #
        # NOTE: we use the default ocean color
        if (ocean_color is not None):
            ax.add_feature(  # type: ignore
                cartopy.feature.OCEAN, facecolor=ocean_color, zorder=0)
        else:
            ax.add_feature(cartopy.feature.OCEAN, zorder=0)  # type: ignore

        # add land
        ax.add_feature(  # type: ignore
            cartopy.feature.LAND, facecolor=land_color, edgecolor=land_edgecolor, zorder=0)

        # add borders
        if (borders_disable is False):
            ax.add_feature(  # type: ignore
                cartopy.feature.BORDERS, edgecolor=borders_color, zorder=0)

        # iterate through each instrument array included
        for i, _ in enumerate(self.instrument_array):

            color = self.color[i]
            symbol = self.symbol[i]
            sym_size = self.sym_size[i]

            if isinstance(color, list):
                color = color[0]
            if isinstance(symbol, list):
                symbol = symbol[0]
            if isinstance(sym_size, list):
                sym_size = sym_size[0]

            site_locations = self.site_locations[i]

            for site in self.site_uid_list[i]:

                if (self.data_availability is not None):

                    if (enforce_data_availability is True) and (self.data_availability[i] is not None) and (site in self.data_availability[i].keys()):
                        if (self.data_availability[i][site] is False):
                            continue

                if (enforce_data_availability is True and self.data_availability is None):
                    raise ValueError("Before plotting FOV object with enforce_data_availability=True, " +
                                     "FOVData.add_availability(...) must be called for all included FOVData objects.")

                latlon = site_locations[site]

                ax.plot(np.squeeze(latlon[1]),
                        np.squeeze(latlon[0]),
                        color=color,
                        zorder=1,
                        marker=symbol,
                        markersize=sym_size,
                        transform=cartopy.crs.Geodetic())

                # Add site_uid labels to the FoV plot, in the center of each ASI FoV
                if label:
                    center_lat = latlon[0] + 1.0
                    center_lon = latlon[1]

                    if (upper_label is True):
                        ax.text(center_lon,
                                center_lat,
                                site.upper(),
                                ha="center",
                                va="center",
                                color=color,
                                transform=cartopy.crs.Geodetic(),
                                clip_on=True)
                    else:
                        ax.text(center_lon,
                                center_lat,
                                site.lower(),
                                ha="center",
                                va="center",
                                color=color,
                                transform=cartopy.crs.Geodetic(),
                                clip_on=True)

        # Go through and plot all of the contour data included in the Object
        if self.contour_data is not None:
            for i in range(len(self.contour_data["x"])):
                ax.plot(self.contour_data["x"][i],
                        self.contour_data["y"][i],
                        color=self.contour_data["color"][i],
                        linewidth=self.contour_data["linewidth"][i],
                        linestyle=self.contour_data["linestyle"][i],
                        marker=self.contour_data["marker"][i],
                        zorder=self.contour_data["zorder"][i])

        # set title
        if (title is not None):
            ax.set_title(title)

        # save figure or show it
        if (savefig is True):
            # check that filename has been set
            if (savefig_filename is None):
                raise ValueError("The savefig_filename parameter is missing, but required since savefig was set to True.")

            # save the figure
            f_extension = os.path.splitext(savefig_filename)[-1].lower()
            if (".jpg" == f_extension or ".jpeg" == f_extension):
                # check quality setting
                if (savefig_quality is not None):
                    plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")  # pragma: nocover
                else:
                    plt.savefig(savefig_filename, bbox_inches="tight")
            else:
                if (savefig_quality is not None):
                    # quality specified, but output filename is not a JPG, so show a warning
                    show_warning("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
                                 "savefig_filename parameter was determined to not be a JPG file, so the quality will be ignored",
                                 stacklevel=1)
                plt.savefig(savefig_filename, bbox_inches="tight")

            # clean up by closing the figure
            plt.close(fig)
        elif (returnfig is True):
            # return the figure and axis objects
            return (fig, ax)
        else:
            # show the figure
            plt.show(fig)

            # cleanup by closing the figure
            plt.close(fig)

        # return
        return None

    def add_geo_contours(self,
                         lats: Optional[Union[ndarray, list]] = None,
                         lons: Optional[Union[ndarray, list]] = None,
                         constant_lats: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         constant_lons: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         color: str = "black",
                         linewidth: Union[float, int] = 1,
                         linestyle: str = "solid",
                         marker: str = "",
                         bring_to_front: bool = False):
        """
        Add geographic contours to a FoV map.

        Args:
            lats (ndarray or list): 
                Sequence of geographic latitudes defining a contour.
            
            lons (ndarray or list): 
                Sequence of geographic longitudes defining a contour.

            constant_lats (float, int, or Sequence): 
                Geographic Latitude(s) at which to add line(s) of constant latitude.
            
            constant_lons (float, int, or Sequence): 
                Geographic Longitude(s) at which to add line(s) of constant longitude.

            color (str): 
                The matplotlib color used for the contour(s).

            linewidth (float or int): 
                The contour thickness.
            
            linestyle (str): 
                The matplotlib linestyle used for the contour(s).

            marker (str): 
                The matplotlib marker used for the contour(s).

            bring_to_front (bool): 
                Plots the contour on top of all other currently plotted objects.

        Returns:
            The object's contour_data parameter is populated appropriately.

        Raises:
            ValueError: issues encountered with supplied parameters.
        """
        # Make sure some form of lat/lon is provided
        if (constant_lats is None) and (constant_lons is None) and (lats is None) and (lons is None):
            raise ValueError("No latitudes or longitudes provided.")

        # If manually passing in lats & lons, make sure both are provided
        if (lats is not None or lons is not None) and (lats is None or lons is None):
            raise (ValueError("Manually supplying contour requires both lats and lons."))

        # Check that color exists in matplotlib
        if color not in matplotlib.colors.CSS4_COLORS:
            raise ValueError(f"Color '{color}' not recognized by matplotlib.")

        # Check that linestyle is valid
        if linestyle not in ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]:
            raise ValueError(f"Linestyle '{linestyle}' not recognized by matplotlib.")

        # Check that linewidth is valid
        if linewidth <= 0:
            raise ValueError("Linewidth must be greater than zero.")

        # Check that marker is valid
        if marker not in ["", "o", ".", "p", "*", "x", "+", "X"]:
            raise ValueError(f"Marker '{marker}' is not currently supported.")

        # Convert numerics to lists if necessary
        if constant_lats is not None:
            if isinstance(constant_lats, (float, int)):
                constant_lats = [constant_lats]
        if constant_lons is not None:
            if isinstance(constant_lons, (float, int)):
                constant_lons = [constant_lons]

        # Initialize contour data dict if it doesn't exist yet
        if self.contour_data is None:
            self.contour_data = {"x": [], "y": [], "color": [], "linewidth": [], "linestyle": [], "marker": [], "zorder": []}

        # Obtain the Fov map's projection
        source_proj = pyproj.CRS.from_user_input(cartopy.crs.Geodetic())
        mosaic_proj = pyproj.CRS.from_user_input(self.cartopy_projection)
        transformer = pyproj.Transformer.from_crs(source_proj, mosaic_proj, always_xy=True)

        # First handling manually supplied lat/lon arrays
        if (lats is not None) and (lons is not None):
            # Convert lists to ndarrays if necessary
            if isinstance(lats, list):
                lats = np.array(lats)
            if isinstance(lons, list):
                lons = np.array(lons)

            if len(lats) != len(lons):
                raise ValueError("Lat/Lon data must be of the same size.")

            # Create specified contour from geographic coords
            x, y = transformer.transform(lons, lats)
            # Add contour to dict, along with color and linewidth
            self.contour_data["x"].append(x)
            self.contour_data["y"].append(y)
            self.contour_data["color"].append(color)
            self.contour_data["linewidth"].append(linewidth)
            self.contour_data["linestyle"].append(linestyle)
            self.contour_data["marker"].append(marker)
            self.contour_data["zorder"].append(int(bring_to_front))

        # Next handling lines of constant latitude
        if constant_lats is not None:
            # Generate longitudinal domain of the lat line (full globe)
            lon_domain = np.arange(-180, 180 + 0.2, 0.2)

            # Iterate through all lines of constant lat requested
            for lat in constant_lats:
                # Create line of constant lat
                const_lat_x, const_lat_y = (lon_domain, lon_domain * 0 + lat)
                sort_idx = np.argsort(const_lat_x)
                const_lat_y = const_lat_y[sort_idx]
                const_lat_x = const_lat_x[sort_idx]
                const_lat_x, const_lat_y = transformer.transform(const_lat_x, const_lat_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lat_x)
                self.contour_data["y"].append(const_lat_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

        # Now handling lines of constant longitude
        if constant_lons is not None:
            # Generate latitudinal domain of the lon line (full globe)
            lat_domain = np.arange(-90, 90 + 0.1, 0.1)

            # Iterate through all lines of constant lon requested
            for lon in constant_lons:
                # Create line of constant lon and add to dict
                const_lon_x, const_lon_y = (lat_domain * 0 + lon, lat_domain)
                sort_idx = np.argsort(const_lon_y)
                const_lon_x = const_lon_x[sort_idx]
                const_lon_y = const_lon_y[sort_idx]
                const_lon_x, const_lon_y = transformer.transform(const_lon_x, const_lon_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lon_x)
                self.contour_data["y"].append(const_lon_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

    def add_mag_contours(self,
                         timestamp: datetime.datetime,
                         constant_lats: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         constant_lons: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         lats: Optional[Union[ndarray, list]] = None,
                         lons: Optional[Union[ndarray, list]] = None,
                         color: str = "black",
                         linewidth: Union[float, int] = 1,
                         linestyle: str = "solid",
                         marker: str = "",
                         bring_to_front: bool = False):
        """
        Add geomagnetic contours to a FoV map.

        Args:
            timestamp (datetime.datetime): 
                The timestamp used in computing AACGM coordinates.

            lats (ndarray or list): 
                Sequence of geomagnetic latitudes defining a contour.
            
            lons (ndarray or list): 
                Sequence of geomagnetic longitudes defining a contour.

            constant_lats (float, int, Sequence): 
                Geomagnetic latitude(s) at which to add contour(s) of constant latitude.
            
            constant_lons (float, int, Sequence): 
                Geomagnetic longitude(s) at which to add contours(s) of constant longitude.

            color (str): 
                The matplotlib color used for the contour(s).

            linewidth (float or int): 
                The contour thickness.

            linestyle (str): 
                The matplotlib linestyle used for the contour(s).

            marker (str): 
                The matplotlib marker used for the contour(s).

            bring_to_front (bool): 
                Plots the contour on top of all other currently plotted objects.

        Returns:
            The object's contour_data parameter is populated appropriately.

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        # Make sure some form of lat/lon is provided
        if (constant_lats is None) and (constant_lons is None) and (lats is None) and (lons is None):
            raise ValueError("No latitudes or longitudes provided.")

        # If manually passing in lats & lons, make sure both are provided
        if (lats is not None or lons is not None) and (lats is None or lons is None):
            raise ValueError("Manually supplying contour requires both lats and lons.")

        # Check that color exists in matplotlib
        if color not in matplotlib.colors.CSS4_COLORS:
            raise ValueError(f"Color '{color}' not recognized by matplotlib.")

        # Check that linestyle is valid
        if linestyle not in ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]:
            raise ValueError(f"Linestyle '{linestyle}' not recognized by matplotlib.")

        # Check that linewidth is valid
        if linewidth <= 0:
            raise ValueError("linewidth must be greater than zero.")

        # Convert numerics to lists if necessary
        if constant_lats is not None:
            if isinstance(constant_lats, (float, int)):
                constant_lats = [constant_lats]
        if constant_lons is not None:
            if isinstance(constant_lons, (float, int)):
                constant_lons = [constant_lons]

        # Initialize contour data dict if it doesn't exist yet
        if self.contour_data is None:
            self.contour_data = {"x": [], "y": [], "color": [], "linewidth": [], "linestyle": [], "marker": [], "zorder": []}

        # Obtain the FoV map's projection
        source_proj = pyproj.CRS.from_user_input(cartopy.crs.Geodetic())
        mosaic_proj = pyproj.CRS.from_user_input(self.cartopy_projection)
        transformer = pyproj.Transformer.from_crs(source_proj, mosaic_proj, always_xy=True)

        # First handling manually supplied lat/lon arrays
        if (lats is not None) and (lons is not None):
            # Convert lists to ndarrays if necessary
            if isinstance(lats, list):
                lats = np.array(lats)
            if isinstance(lons, list):
                lons = np.array(lons)

            if len(lats) != len(lons):
                raise ValueError("Lat/Lon data must be of the same size.")

            # Create specified contour from magnetic coords
            y, x, alt = aacgmv2.convert_latlon_arr(lats, lons, lats * 0.0, timestamp, method_code="A2G")
            x, y = transformer.transform(x, y)

            # Add contour to dict, along with color and linewidth
            self.contour_data["x"].append(x)
            self.contour_data["y"].append(y)
            self.contour_data["color"].append(color)
            self.contour_data["linewidth"].append(linewidth)
            self.contour_data["linestyle"].append(linestyle)
            self.contour_data["marker"].append(marker)
            self.contour_data["zorder"].append(int(bring_to_front))

        # Next handling lines of constant latitude
        if constant_lats is not None:
            # Generate longitudinal domain of the lat line (full globe)
            lon_domain = np.arange(-180, 180 + 0.2, 0.2)

            # iterate through all lines of constant lat requested
            for lat in constant_lats:
                # Create line of constant lat from magnetic coords
                const_lat_x, const_lat_y = (lon_domain, lon_domain * 0 + lat)
                const_lat_y, const_lat_x, alt = aacgmv2.convert_latlon_arr(const_lat_y, const_lat_x, const_lat_x * 0.0, timestamp, method_code="A2G")
                sort_idx = np.argsort(const_lat_x)
                const_lat_y = const_lat_y[sort_idx]
                const_lat_x = const_lat_x[sort_idx]
                const_lat_x, const_lat_y = transformer.transform(const_lat_x, const_lat_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lat_x)
                self.contour_data["y"].append(const_lat_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

        # Now handling lines of constant longitude
        if constant_lons is not None:
            # Generate latitudinal domain of the lon line (full globe)
            lat_domain = np.arange(-90, 90 + 0.1, 0.1)

            # iterate through all lines of constant lon requested
            for lon in constant_lons:
                # Create line of constant lon from magnetic coords
                const_lon_x, const_lon_y = (lat_domain * 0 + lon, lat_domain)
                const_lon_y, const_lon_x, alt = aacgmv2.convert_latlon_arr(const_lon_y, const_lon_x, const_lon_x * 0.0, timestamp, method_code="A2G")
                sort_idx = np.argsort(const_lon_y)
                const_lon_x = const_lon_x[sort_idx]
                const_lon_y = const_lon_y[sort_idx]
                const_lon_x, const_lon_y = transformer.transform(const_lon_x, const_lon_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lon_x)
                self.contour_data["y"].append(const_lon_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))
