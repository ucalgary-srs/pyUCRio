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
Obtain FoVs of ASIs and create plots.
"""

import cartopy.crs
from typing import Optional, List, Literal, Union
from ..classes.site_map import SiteMap
from ._create_map import create_map as func_create_map

__all__ = ["SiteMapManager"]


class SiteMapManager:
    """
    The SiteMapManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, ucrio_obj):
        self.__ucrio_obj = ucrio_obj

    def create_map(self,
                   cartopy_projection: cartopy.crs.Projection,
                   instrument_array: Union[Literal["swan_hsr", "norstar_riometer"], List[str]],
                   site_uid_list: Optional[Union[List[str], List[List[str]]]] = None,
                   color: Union[str, List[str]] = 'black',
                   symbol: Union[str, List[str]] = 'o',
                   sym_size: Union[int, List[int]] = 1) -> SiteMap:
        """
        Create a SiteMap object.

        Args:
            
            cartopy_projection (cartopy.crs.Projection): 
                The cartopy projection to use when creating the FoV map.

            site_uid_list (str or list of str): 
                List of site UIDs to include in the map.

            instrument_array (str): 
                The instrument array that the site_uid_list sites are a part of.

            color (str): 
                String specifying a matplotlib color to associate with site locations
                for plotting.

            symbol (int): 
                Integer giving the linewidth to associate with site locations for plotting.

            sym_size (str): 
                String specifying a matplotlib linestyle to associate with site locations
                for plotting.

        Returns:
            The generated `pyaurorax.tools.SiteMap` object.

        Raises:
            ValueError: issues encountered with supplied parameters
            pyaurorax.exceptions.AuroraXError: general issue encountered
        """
        return func_create_map(self.__ucrio_obj, cartopy_projection, site_uid_list, instrument_array, color, symbol, sym_size)
