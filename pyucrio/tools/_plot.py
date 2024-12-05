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
import warnings
import datetime
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import List, Union, Optional, Tuple, Any
from pyucalgarysrs.data.classes import Data


def __smooth_data(data, window_size):
    """Moving Average Smoothing for down-sampling"""
    if window_size < 1:
        return data
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')


def plot(rio_data: Union[Data, List[Data]],
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

        dateformat (str): 
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

    # check return mode
    if (returnfig is True and savefig is True):
        raise ValueError("Only one of returnfig or savefig can be set to True")
    if (returnfig is True and (savefig_filename is not None or savefig_quality is not None)):
        warnings.warn("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                      "removing the savefig option parameter(s) as they will be ignored.",
                      stacklevel=1)
    elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
        warnings.warn("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                      "savefig option parameters will be ignored.",
                      stacklevel=1)

    # Convert to single element list if only a single data object is passed in
    if isinstance(rio_data, Data):
        rio_data = [rio_data]

    data_types = []
    for data in rio_data:
        if type(data.data[0]) not in data_types:
            data_types.append(type(data.data[0]))

    if len(data_types) > 1 and not stack_plot:
        raise ValueError(f"Cannot plot multiple data-types on the same axis: {data_types}")

    # Cycle through colors and linestyles if provided
    color_cycle = itertools.cycle(color) if isinstance(color, list) else itertools.cycle([color])
    linestyle_cycle = itertools.cycle(linestyle) if isinstance(linestyle, list) else itertools.cycle([linestyle])

    # Count total plots required
    total_plots = 0
    for data in rio_data:
        data_name = data.dataset.name if data.dataset is not None else "unknown dataset"
        if data_name == 'SWAN_HSR_K0_H5':
            if hsr_bands is not None:

                total_plots += len(hsr_bands) if isinstance(hsr_bands, list) else 1
            else:
                total_plots += len(np.where(data.data[0].band_central_frequency)[0])
        else:
            total_plots += 1

    # Create subplots with the specified figsize
    current_axis_idx = 0
    if stack_plot:
        fig, axes = plt.subplots(total_plots, 1, figsize=figsize, sharex=True)
        if total_plots == 1:
            axes = [axes]  # Ensure axes is always iterable
    else:
        fig = plt.figure(figsize=figsize)
        axes = [fig.add_axes((0, 0, 1, 1))]

    # Iterate through each data object in list
    for data in rio_data:

        # Check for an empty data object (in case of attempting to download non-existing data)
        if len(data.data) == 0:
            if data.dataset is not None:
                warnings.warn("Received one or more empty Data objects ('%s')" % (data.dataset.name), UserWarning, stacklevel=1)
            else:
                warnings.warn("Received one or more empty Data objects." % UserWarning, stacklevel=1)
            continue

        # Get the dataset and site names
        dataset = data.dataset.name if data.dataset is not None else "unknown dataset"
        site = data.metadata[0]['site_unique_id']

        # Initialize array and dict to hold timestamps and data, respectively
        time_stamp = np.array([])
        data_dict = dict()

        # Initialize list to automatically determine axis names
        y_axis_names = []

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
                    bands = np.intersect1d(hsr_bands, np.where(d.band_central_frequency)[0])
                for band_idx in bands:
                    band_name = (f"{site.upper()} HSR Band-{str(band_idx).zfill(2)} "
                                 f"{round(float(d.band_central_frequency[band_idx].decode('utf-8').split()[0]), 1)} MHz")
                    band_names.append(band_name)

                for _idx in bands:
                    if absorption:
                        y_axis_names.append('Absorption (dB)')
                    else:
                        y_axis_names.append('Raw Power (dB)')

            # Default band for non HSR data is 30 MHz
            else:
                if absorption:
                    y_axis_names.append('Absorption (dB)')
                else:
                    y_axis_names.append('Raw Signal (V)')

                bands = [0]
                band_name = f"{site.upper()} Riometer 30.0 MHz"
                band_names.append(band_name)

            # Pull out the data array of interest from the Riometer or HSR data object
            if (dataset == 'NORSTAR_RIOMETER_K0_TXT') or (dataset == 'NORSTAR_RIOMETER_K2_TXT'):
                if absorption:
                    # Check there is absorption data if requested
                    if d.absorption is None:
                        warnings.warn(f"Omitting plotting (no absorption data) for '{dataset}'", UserWarning, stacklevel=1)
                        continue
                    else:
                        for k, _ in enumerate(bands):
                            data_arr = d.absorption
                            if band_names[k] in data_dict:
                                data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, _ in enumerate(bands):
                        data_arr = d.raw_signal
                        if band_names[k] in data_dict:
                            data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                        else:
                            data_dict[band_names[k]] = data_arr
            elif dataset == 'SWAN_HSR_K0_H5':
                if absorption:
                    # Check there is absorption data if requested
                    if d.absorption is None:
                        warnings.warn(f"Omitting plotting (no absorption data) for '{dataset}'", UserWarning, stacklevel=1)
                        continue
                    else:
                        for k, band_idx in enumerate(bands):
                            data_arr = d.absorption[band_idx, :]
                            if band_names[band_idx] in data_dict:
                                data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, band_idx in enumerate(bands):
                        data_arr = d.raw_power[band_idx, :]
                        if band_names[k] in data_dict:
                            data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                        else:
                            data_dict[band_names[k]] = data_arr

        # Iterate through each data array we are plotting
        for j, (signal_name, signal_data) in enumerate(data_dict.items()):

            auto_ylabel = y_axis_names[j]

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
                time_deltas = np.array([(time_stamp[i + 1] - time_stamp[i]).total_seconds() for i in range(len(time_stamp) - 1)])
                sampling_rate = np.median(time_deltas)
                window_size = int(downsample_seconds / sampling_rate)
                if window_size > 0:
                    signal_data = __smooth_data(signal_data, window_size)

            # Plot the data
            ax.plot(time_stamp, signal_data, color=current_color, label=signal_name, linestyle=current_linestyle)

            # Add ytitle
            ax.set_ylabel(auto_ylabel)
            if ytitle:
                ax.set_ylabel(ytitle)

            # Add legend to each subplot
            ax.legend()

            # Add x-axis titles
            if stack_plot:
                if ax is axes[-1]:
                    if xtitle is None:
                        ax.set_xlabel("Hour (UTC)" if date_format is None else "Time (UTC)")
                    else:
                        ax.set_xlabel(xtitle)
            else:
                if xtitle is None:
                    ax.set_xlabel("Hour (UTC)" if date_format is None else "Time (UTC)")
                else:
                    ax.set_xlabel(xtitle)

            # Format the x-axis (dates) automatically or as requested
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H' if date_format is None else date_format))

            # Set x-range
            if xrange:
                ax.set_xlim(xrange)  # type: ignore
            else:
                # If no x-range is supplied, get rid of whitespace
                ax.set_xlim([time_stamp[0], time_stamp[-1]])  # type: ignore

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
                plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")
            else:
                plt.savefig(savefig_filename, bbox_inches="tight")
        else:
            if (savefig_quality is not None):
                # quality specified, but output filename is not a JPG, so show a warning
                warnings.warn("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
                              "savefig_filename parameter was determined to not be a JPG file, so the quality will be ignored",
                              stacklevel=1)
            plt.savefig(savefig_filename, bbox_inches="tight")

        # clean up by closing the figure
        plt.close(fig)

    elif (returnfig is True):
        # return the figure and axis objects
        return (fig, axes)
    else:
        # show the figure
        plt.show(fig)

        # cleanup by closing the figure
        plt.close(fig)

    # return
    return None
