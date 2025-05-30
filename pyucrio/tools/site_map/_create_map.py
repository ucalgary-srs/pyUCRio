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

from ..classes.site_map import SiteMap


def create_map(ucrio_obj, cartopy_projection, site_uid_list, instrument_array, color, symbol, sym_size):

    # Convert everything to lists regardless so its easier to handle
    if (not isinstance(site_uid_list, list)):
        site_uid_list = [site_uid_list]

    if isinstance(site_uid_list[0], str):
        site_uid_list = [site_uid_list]

    if isinstance(instrument_array, str):
        instrument_array = [instrument_array]

    if (site_uid_list is None):
        all_sites_list = []
        for instrument in instrument_array:
            site_list = []
            # Get all site records for this instrument
            result = ucrio_obj.data.ucalgary.list_observatories(instrument)
            for r in result:
                site_list.append(r.uid)
            all_sites_list.append(site_list)

    if isinstance(color, str):
        color = [color]
        if len(color) < len(instrument_array):
            color_list = []
            for _ in instrument_array:
                color_list.append(color)
            color = color_list

    if isinstance(symbol, str):
        symbol = [symbol]
        if len(symbol) < len(instrument_array):
            symbol_list = []
            for _ in instrument_array:
                symbol_list.append(symbol)
            symbol = symbol_list

    if isinstance(sym_size, int):
        sym_size = [sym_size]
        if len(sym_size) < len(instrument_array):
            sym_size_list = []
            for _ in instrument_array:
                sym_size_list.append(sym_size)
            sym_size = sym_size_list

    instrument_sites = []
    instrument_site_locations = []
    for k, instrument in enumerate(instrument_array):

        site_dict = {}

        # First, if no sites are provided, we just get all sites for the provided 'instrument_array'
        if site_uid_list[0] is None:

            # Get all site records for this instrument
            result = ucrio_obj.data.ucalgary.list_observatories(instrument)

            for r in result:
                site_dict[r.uid] = (r.geodetic_latitude, r.geodetic_longitude)

        # Otherwise, iterate through each site provided
        else:

            if isinstance(site_uid_list[0], list):
                site_uids = site_uid_list[k]
            else:
                site_uids = site_uid_list

            for site in site_uids:

                # Get the site location of this site_uid for the chosen instrument_array, from the API
                result = ucrio_obj.data.ucalgary.list_observatories(instrument, uid=site)

                # Check if a site record was actually returned
                if len(result) == 0:
                    raise ValueError(f'Could not find requested site_uid "{site}" for instrument_array "{instrument}".')
                else:
                    site_record = result[0]

                # Add this record to the dictionary
                site_dict[site_record.uid] = (site_record.geodetic_latitude, site_record.geodetic_longitude)

        # Create site_uid list and dictionaries to hold fov coords and shapes, to put in the FOVData object
        instrument_sites.append(list(site_dict.keys()))
        instrument_site_locations.append(site_dict)

    # Now, site dict contains all of the site_uids and corresponding (lat, lon) pairs we want to get data
    # for, along with the altitude and minimum elevation to map FoVs at. Now, we iterate through each site

    # Create and return the FOVData object
    return SiteMap(cartopy_projection=cartopy_projection,
                   site_uid_list=instrument_sites,
                   site_locations=instrument_site_locations,
                   instrument_array=instrument_array,
                   data_availability=None,
                   color=color,
                   symbol=symbol,
                   sym_size=sym_size,
                   contour_data=None,
                   ucrio_obj=ucrio_obj)
