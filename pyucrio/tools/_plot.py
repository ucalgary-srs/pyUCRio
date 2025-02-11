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
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyucalgarysrs.data.classes import Data
from .._util import show_warning


def __smooth_data(data, window_size):
    """
    Moving Average Smoothing for down-sampling
    """
    if window_size < 1:  # pragma: nocover
        return data
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')


def plot(rio_data, absorption, stack_plot, downsample_seconds, hsr_bands, color, figsize, title, date_format, xtitle, ytitle, xrange, yrange,
         linestyle, returnfig, savefig, savefig_filename, savefig_quality):

    # check return mode
    if (returnfig is True and savefig is True):
        raise ValueError("Only one of returnfig or savefig can be set to True")
    if (returnfig is True and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                     "removing the savefig option parameter(s) as they will be ignored.")
    elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                     "savefig option parameters will be ignored.")

    # Convert to single element list if only a single data object is passed in
    if isinstance(rio_data, Data):
        rio_data = [rio_data]

    # do some checks on the data types
    #
    # NOTE: we do not allow multiple data types (NORSTAR riometer data and HSR data)
    # on the same axis
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
        if data_name == "SWAN_HSR_K0_H5":
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
        #
        # NOTE: we exclude this from the test suite since we updated PyUCalgarySRS reading to not
        # return empty data objects. We'll keep it in here in case there's an edge case lingering
        # that we're not aware of.
        if len(data.data) == 0:  # pragma: nocover-ok
            if data.dataset is not None:
                show_warning("Received one or more empty Data objects ('%s')" % (data.dataset.name))
            else:
                show_warning("Received one or more empty Data objects.")
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
            if (dataset == "SWAN_HSR_K0_H5"):

                if (hsr_bands is None):
                    bands = np.where(d.band_central_frequency)[0]
                else:
                    bands = np.intersect1d(hsr_bands, np.where(d.band_central_frequency)[0])

                for band_idx in bands:
                    band_name = (f"{site.upper()} HSR Band-{str(band_idx).zfill(2)} "
                                 f"{round(float(d.band_central_frequency[band_idx].split()[0]), 1)} MHz")
                    band_names.append(band_name)

                for _ in bands:
                    if (absorption is True):
                        y_axis_names.append("Absorption (dB)")
                    else:
                        y_axis_names.append("Raw Power (dB)")

            # Default band for non HSR data is 30 MHz
            else:
                if (absorption is True):
                    y_axis_names.append("Absorption (dB)")
                else:
                    y_axis_names.append("Raw Signal (V)")

                bands = [0]
                band_name = f"{site.upper()} Riometer 30.0 MHz"
                band_names.append(band_name)

            # Pull out the data array of interest from the Riometer or HSR data object
            if (dataset == "NORSTAR_RIOMETER_K0_TXT") or (dataset == "NORSTAR_RIOMETER_K2_TXT"):
                if (absorption is True):
                    # Check there is absorption data if requested
                    if (d.absorption is None):
                        show_warning(f"Omitting plotting (no absorption data) for '{dataset}'")
                        continue
                    else:
                        for k, _ in enumerate(bands):
                            data_arr = d.absorption
                            if band_names[k] in data_dict:  # pragma: nocover
                                data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, _ in enumerate(bands):
                        data_arr = d.raw_signal
                        if band_names[k] in data_dict:  # pragma: nocover
                            data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                        else:
                            data_dict[band_names[k]] = data_arr
            elif (dataset == "SWAN_HSR_K0_H5"):
                if (absorption is True):
                    # Check there is absorption data if requested
                    if (d.absorption is None):
                        show_warning(f"Omitting plotting (no absorption data) for '{dataset}'")
                        continue
                    else:
                        for k, band_idx in enumerate(bands):  # pragma: nocover
                            data_arr = d.absorption[band_idx, :]
                            if band_names[band_idx] in data_dict:
                                data_dict[band_names[k]] = np.concatenate((data_dict[band_names[k]], data_arr))
                            else:
                                data_dict[band_names[k]] = data_arr
                else:
                    for k, band_idx in enumerate(bands):
                        data_arr = d.raw_power[band_idx, :]
                        if band_names[k] in data_dict:  # pragma: nocover
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
            if (stack_plot is True):
                ax = axes[current_axis_idx]
                current_axis_idx += 1
            else:
                ax = plt.gca()

            # Down-sample data if requested
            if (downsample_seconds > 0):
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
            if (ytitle is not None):
                ax.set_ylabel(ytitle)

            # Add legend to each subplot
            ax.legend()

            # Add x-axis titles
            if (stack_plot is True):
                if ax is axes[-1]:
                    if (xtitle is None):
                        ax.set_xlabel("Hour (UTC)" if date_format is None else "Time (UTC)")
                    else:
                        ax.set_xlabel(xtitle)
            else:
                if (xtitle is None):
                    ax.set_xlabel("Hour (UTC)" if date_format is None else "Time (UTC)")
                else:
                    ax.set_xlabel(xtitle)

            # Format the x-axis (dates) automatically or as requested
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H' if date_format is None else date_format))

            # Set x-range
            if (xrange is not None):
                ax.set_xlim(xrange)  # type: ignore
            else:
                # If no x-range is supplied, get rid of whitespace
                ax.set_xlim([time_stamp[0], time_stamp[-1]])  # type: ignore

            if (yrange is not None):
                ax.set_ylim(yrange)

            # Adjust yticks to prevent overlap
            if stack_plot and current_axis_idx > 1:
                y_ticks = ax.get_yticks()  # Get the current Y ticks
                ax.set_yticks(y_ticks[:-1])

    # Add overall legend if not making a stack plot
    if (stack_plot is False):
        plt.legend()

    # Add title
    if (title is not None):
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
            if (savefig_quality is not None):  # pragma: nocover-ok
                plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")
            else:
                plt.savefig(savefig_filename, bbox_inches="tight")
        else:
            if (savefig_quality is not None):
                # quality specified, but output filename is not a JPG, so show a warning
                show_warning("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
                             "savefig_filename parameter was determined to not be a JPG file, so the quality will be ignored")
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
