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
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
from typing import List, Union, Optional
from pyucalgarysrs.data.classes import Data


def __smooth_data(data, window_size):
    """Moving Average Smoothing for down-sampling"""
    if window_size < 1:
        return data
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')


def plot(rio_data: Union[Data, List[Data]],
         absorption: bool = False,
         stack_plot: bool = False,
         downsample_seconds: Optional[int] = 1,
         hsr_bands: Optional[Union[int, List[int]]] = None,
         color: Optional[Union[str, List[str]]] = None,
         figsize: Optional[tuple] = (8, 4),
         return_fig: Optional[bool] = False,
         title: Optional[str] = None,
         date_format: Optional[str] = None,
         xtitle: Optional[str] = None,
         ytitle: Optional[str] = None,
         xrange: Optional[List] = None,
         yrange: Optional[List[datetime.datetime]] = None,
         linestyle: Optional[Union[str, List[str]]] = '-'):
    """
    Plot riometer data.

    Args:
        rio_data (pyucalgarysrs.data.classes | List): 
            A single, or list of Data objects containing riometer data. This isthe data to be
            plotted. All objects will be plotted according to plot settings.

        absorption (Optional[bool]): 
            If True, plot absorption data, as opposed to raw data. Defaults to False.

        stack_plot (Optional[bool]): 
            If true, split plots into a stack-plot of subplots for each data array. Defaults to False.
        
        downsample_seconds (Optional[int]):
            An integer, giving the window size for smoothing data before plotting. Default is no smoothing (1).

        hsr_bands (Optional[int | List]):
            An int or list of ints giving the band indices to be plotted for HSR data.

        color (Optional[str | list]):
            A string or list of strings giving matplotlib color names to cycle through for plotting.

        figsize (Optional[list | tuple]):
            The overall figure size. Default is (8,4).

        return_fig (Optional[bool]):
            If true, function call returns reference to the matplotlib figure.

        title (Optional[str]):
            The figure title. Default is no title.

        xtitle (Optional[str]):
            The x-axis title.
        
        ytitle (Optional[str]):
            The y-axis title. 

        xrange (Optional[list[datetime.datetime]]):
            The start and end times to cut-off x-axis plotting at.

        yrange (Optional[list[int | float]]):
            The min/max y-values to plot.

        linestyle (Optional[str | list]):
            A string or list of strings giving matplotlib linestyle names to cycle through for plotting.
        
    Returns:
        None, unless return_fig=True, in which case, returns a reference to the matplotlib figure.

    Raises:
        ValueError: issue with supplied parameters.
    """

    # Convert to single element list if only a single data object is passed in
    if isinstance(rio_data, Data):
        rio_data = [rio_data]

    # Cycle through colors and linestyles if provided
    color_cycle = itertools.cycle(color) if isinstance(
        color, list) else itertools.cycle([color])
    linestyle_cycle = itertools.cycle(linestyle) if isinstance(
        linestyle, list) else itertools.cycle([linestyle])

    # Count total plots required
    total_plots = 0
    for data in rio_data:
        if data.dataset.name == 'SWAN_HSR_K0_H5':
            if hsr_bands is not None:
                total_plots += len(hsr_bands)
            else:
                total_plots += len(
                    np.where(data.data[0].band_central_frequency)[0])
        else:
            total_plots += 1

    # Create subplots with the specified figsize
    if stack_plot:
        fig, axes = plt.subplots(total_plots, 1, figsize=figsize, sharex=True)
        if total_plots == 1:
            axes = [axes]  # Ensure axes is always iterable
        current_axis_idx = 0
    else:
        fig = plt.figure(figsize=figsize)

    # Iterate through each data object in list
    for data in rio_data:

        # Check for an empty data object (in case of attempting to download non-existing data)
        if len(data.data) == 0:
            warnings.warn("Received one or more empty Data objects ('%s')" %
                          (data.dataset.name),
                          UserWarning,
                          stacklevel=1)
            continue
        
        # Get the dataset and site names
        dataset = data.dataset.name
        site = data.metadata[0]['site_unique_id']

        # Initialize array and dict to hold timestamps and data, respectively
        time_stamp = np.array([])
        data_dict = dict()
        
        # Iterate through each Riometer / HSR data object (if spanning across multiple days for one dataset/site)
        for d in data.data:
            
            # Append to time stamp
            time_stamp = np.concatenate((time_stamp, d.timestamp))

            # Get the bands of interest and name them for tracking
            band_names = []
            if dataset == 'SWAN_HSR_K0_H5':
                if hsr_bands is None:
                    bands = np.where(d.band_central_frequency)[0]
                else:
                    bands = np.intersect1d(
                        hsr_bands,
                        np.where(d.band_central_frequency)[0])
                for band_idx in bands:
                    band_name = f"{site.upper()} {dataset} band_{str(band_idx).zfill(2)} {d.band_central_frequency[band_idx].decode('utf-8').split()[0]} MHz"
                    band_names.append(band_name)

            # Default band for non HSR data is 30 MHz
            else:
                bands = [0]
                band_name = f"{site.upper()} {dataset} band_00 30.00 MHz"
                band_names.append(band_name)

            # Pull out the data array of interest from the Riometer or HSR data object
            if (dataset == 'NORSTAR_RIOMETER_K0_TXT') or (
                    dataset == 'NORSTAR_RIOMETER_K2_TXT'):
                if absorption:
                    # Check there is absorption data if requested
                    if d.absorption is None:
                        warnings.warn(
                            f"Omitting plotting (no absorption data) for '{dataset}'",
                            UserWarning,
                            stacklevel=1)
                        continue
                    else:
                        for k, band_idx in enumerate(bands):
                            data_arr = d.absorption
                            if band_names[band_idx] in data_dict:
                                data_dict[band_names[k]] = np.concatenate(
                                    (data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, band_idx in enumerate(bands):
                        data_arr = d.raw_signal
                        if band_names[k] in data_dict:
                            data_dict[band_names[k]] = np.concatenate(
                                (data_dict[band_names[k]], data_arr))
                        else:
                            data_dict[band_names[k]] = data_arr
            elif dataset == 'SWAN_HSR_K0_H5':
                if absorption:
                    # Check there is absorption data if requested
                    if d.absorption is None:
                        warnings.warn(
                            f"Omitting plotting (no absorption data) for '{dataset}'",
                            UserWarning,
                            stacklevel=1)
                        continue
                    else:
                        for k, band_idx in enumerate(bands):
                            data_arr = d.absorption[band_idx, :]
                            if band_names[band_idx] in data_dict:
                                data_dict[band_names[k]] = np.concatenate(
                                    (data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, band_idx in enumerate(bands):
                        data_arr = d.raw_power[band_idx, :]
                        if band_names[k] in data_dict:
                            data_dict[band_names[k]] = np.concatenate(
                                (data_dict[band_names[k]], data_arr))
                        else:
                            data_dict[band_names[k]] = data_arr

        # Iterate through each data array we are plotting
        for signal_name, signal_data in data_dict.items():
            
            # Cycle colors and line-styles
            current_color = next(color_cycle)
            current_linestyle = next(linestyle_cycle)

            # Get the axis to plot on
            if stack_plot:
                ax = axes[current_axis_idx]
                current_axis_idx += 1
            else:
                ax = plt.gca()

            # Down-sample data if requested
            if downsample_seconds > 0:
                # Calculate the number of points to down-sample based on downsample_seconds and datetime array
                time_deltas = np.diff(time_stamp)
                sampling_rate = np.median(
                    time_deltas).total_seconds()  # Seconds as a float
                window_size = int(downsample_seconds / sampling_rate)
                if window_size > 0:
                    signal_data = __smooth_data(signal_data, window_size)

            # Plot the data
            ax.plot(time_stamp,
                    signal_data,
                    color=current_color,
                    label=signal_name,
                    linestyle=current_linestyle)
            
            # Add ytitle
            ax.set_ylabel(
                "Absorption (dB)" if absorption else "Raw Power (dB)")
            if ytitle:
                ax.set_ylabel(ytitle)

            # Add legend to each subplot
            ax.legend()

            # Add x-axis titles
            if stack_plot:
                if ax is axes[-1]:
                    if xtitle is None:
                        ax.set_xlabel("Hour (UTC)" if date_format is
                                      None else "Time (UTC)")
                    else:
                        ax.set_xlabel(xtitle)
            else:
                if xtitle is None:
                    ax.set_xlabel("Hour (UTC)" if date_format is
                                  None else "Time (UTC)")
                else:
                    ax.set_xlabel(xtitle)

            # Format the x-axis (dates) automatically or as requested
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter('%H' if date_format is
                                     None else date_format))
            
            # Set x-range
            if xrange:
                ax.set_xlim(xrange)
            if yrange:
                ax.set_ylim(yrange)

            # Adjust yticks to prevent overlap
            if stack_plot and current_axis_idx > 1:
                y_ticks = ax.get_yticks()  # Get the current Y ticks
                ax.set_yticks(y_ticks[:-1])
    
    # Add overall legend if not making a stack plot
    if not stack_plot:
        plt.legend()

    # Add title
    if title is not None:
        plt.title(title)

    # Make stack-plots flush with each-other, display plot
    plt.subplots_adjust(hspace=0)
    plt.show()

    # Return figure if requested
    if return_fig:
        return fig
    else:
        return None
