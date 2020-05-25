
"""
This is the function for plotting the histogram and Gaussian fits.
"""

import ast
import copy
import matplotlib as mpl
import matplotlib.patches as mpl_patch
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma

import IfA_Smeargle.core as core
import IfA_Smeargle.plotting as plot

def plot_gaussian_histogram(data_array, data_header=None, data_mask=None,
                            figure_axes=None, matplotlib_arguments=None,
                            fit_gaussian=True,
                            **kwargs):
    """ A function to create and plot histogram plots for better 
    analysis of a given array.

    This function replicates the histogram plotting functionality 
    of Tino Well's program. 
    (Found here: https://github.com/tinowells/ifa). More 
    specifically, it attempts to plot histograms of pixel data; then, 
    the program attempts to fit a Gaussian function. 

    Parameters
    ----------
    data_array : ndarray
        This is the provided array that is to be plotted. 
        Dimensions matter!
    data_header : Astropy Header (optional)
        This is the data header of the fits file. If it is not 
        provided, plotting parameters which use it will not be plot.
        I will raise if I need it.
    data_mask : ndarray (optional)
        The mask that should be applied to the `data_array`.
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire 
        to have the heat-map plot to. This defaults to either making 
        new ones, or using the currently defined axes. Note: This 
        is not deep-copied!
    matplotlib_arguments : dictionary (optional)
        These are options the user may use to pass customization 
        parameters into the histogram plot or the Gaussian function
        plot.
        See :py:func:`~.matplotlib.pyplot.bar` and 
        :py:func:`~.matplotlib.pyplot.plot`.

    Returns
    -------
    heatmap_plot_axes : Matplotlib Axes
        This is the heatmap plot made on the (provided, borrowed, or 
        generated) plotting axes.

    """

    # Check that this file was processed by the prior analysis file.
    # If so, also extract needed information for the plot.
    if (data_header is not None):
        # Extract the proper configuration parameters
        run_param = data_header.get('histogram_run', default=False)
    else:
        # The data header is not provided. Warn and continue.
        core.error.ifas_error(core.error.DataError,
                              ("There is no header file associated with "
                               "this data array. Analysis values which are "
                               "stored in it for usage by this function's "
                               "plots may not work or may raise."))
        # Defaults.
        run_param = True

    # If this file was not analyzed by the previous function for 
    # making heat-maps.
    if (not run_param):
        raise core.error.DataError("The `histogram_run` parameter is not in "
                                   "this file's header. This file was not "
                                   "analyzed by the proper function to "
                                   "prepare the data for plotting.")

    # If the user provided a mask, apply it. Otherwise, use a blank
    # mask.
    if (data_mask is not None):
        # The mask exists so it shall be applied.
        plot_data = np_ma.array(np_ma.getdata(data_array, False), 
                                mask=data_mask)
    else:
        if (isinstance(data_array, np_ma.MaskedArray)):
            # The object is already a masked array, deferring to the 
            # user here.
            plot_data = data_array
            core.error.ifas_info("The provided data array is a masked "
                                 "array. Its mask will be applied to the "
                                 "heat-map.")
        else:
            # There is no mask, so none shall be applied.
            plot_data = np_ma.array(data_array, mask=np_ma.nomask)


    # First, figure out what type of Matplotlib axes to use.
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()


    # Obtaining the histogram data.
    hist_bins = np.array(ast.literal_eval(data_header['HIST_BIN']), 
                         dtype=float)
    hist_values = np.array(ast.literal_eval(data_header['HIST_VAL']),
                           dtype=int)

    # Create the histogram plot manually, rather than recomputing the
    # entire histogram.
    ax.bar(hist_bins[:-1], hist_values, width=(hist_bins[1:]-hist_bins[:-1]), 
           align='edge', **matplotlib_arguments)

    if (fit_gaussian):
        # Obtain the Gaussian parameters.
        gauss_mean = data_header['histogram_mean']                                               
        gauss_std = data_header['histogram_stddev']                                   
        gauss_ampli = data_header['histogram_amplitude']
        gauss_max = data_header['histogram_max']


        # Creating the Gaussian functional fit from the calculated 
        # parameters.
        __, gauss_funct = core.math.ifas_gaussian_function(
            input=0, mean=gauss_mean, stddev=gauss_std, amplitude=gauss_ampli)

        # Creating the input to plot. The number of points at this
        # point is arbitrary but sufficient.
        buffer_factor = 0.2
        gauss_input = np.linspace((np.nanmin(hist_bins) 
                                   - (np.abs(np.nanmin(hist_bins))
                                      * buffer_factor)), 
                                  (np.nanmax(hist_bins) 
                                   + (np.abs(np.nanmin(hist_bins)) 
                                      * buffer_factor)), 
                                  (100 + hist_bins.size**2), endpoint=True)
        gauss_output = gauss_funct(gauss_input)

        # Plot the Gaussian. 
        ax.plot(gauss_input, gauss_output, linewidth=1.5, color='black')

        # Also plot the other lines of the Gaussian plot, such as
        # the maximum and sigma limits.
        # Center line and +/- 1 or 2 sigma vertical lines.
        stddev_lines = (gauss_mean + gauss_std*np.array([-2,-1,0,1,2]))
        stddev_colors = ['red', 'red', 'purple', 'red', 'red']
        line_patterns = ['dotted','dashed','solid','dashed','dotted']
        for linedex, colordex, patterndex in zip(
            stddev_lines, stddev_colors, line_patterns):
            # Making each line.
            ax.axvline(x=linedex, linestyle=patterndex, 
                       color=colordex, alpha=0.75)
        # Gaussian max peak value horizontal line.
        ax.axhline(y=gauss_max, color='orange', alpha=0.75)

        # Manually assigning legend elements.
        center_label = mpl_patch.Patch(
            color=stddev_colors[2], linewidth=1, 
            label='\u03BC = {0:.3f}'.format(gauss_mean))
        stddev_label = mpl_patch.Patch(
            color=stddev_colors[1], linewidth=1,
            label='\u03C3 = {0:.3f}'.format(gauss_std))
        peak_label = mpl_patch.Patch(
            color='orange', label='Max = {0:.3f}'.format(gauss_max))
        ax.legend(handles=[center_label,stddev_label,peak_label],
                  markerscale=0.75, fontsize='small',
                  loc='upper center', bbox_to_anchor=(0.5, -0.1), 
                  shadow=True, ncol=4)
    else:
        # No Gaussian function plot.
        pass

    # Basic axis labels.
    ax.set_xlabel('Pixel Values')
    ax.set_ylabel('Count Quantity')

    # Always auto-adjust the x-axis to fit the histogram properly.
    bound_factor = 0.1
    left_bound = (np.nanmin(hist_bins) 
                  - np.abs(np.nanmin(hist_bins)*bound_factor))
    right_bound = (np.nanmax(hist_bins) 
                   + np.abs(np.nanmax(hist_bins)*bound_factor))
    ax.set_xlim(left_bound, right_bound)

    # Always auto-adjust y-axis to histogram as it is the data. If
    # log plotting is on, then scale to correct for the sub-1 values
    # too.
    range_factor = 0.1
    bottom_range = 1.0 if (matplotlib_arguments.get('log', False)) else None
    top_range = (np.nanmax(hist_values) 
                 + np.abs(np.nanmax(hist_values))*range_factor)
    ax.set_ylim(bottom_range, top_range)

    # That should be it, for naming convention.
    heatmap_plot_axes = ax
    return heatmap_plot_axes



def script_plot_gaussian_histogram(config):
    """ The scripting version of `plot_gaussian_histogram`. This 
    function automatically creates heat-map plots for each and 
    every analysis data file.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """

    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])


    # Compile the configuration parameters for the creation of the 
    # figure itself.
    figure_arguments = {}

    # Extract configuration parameters that the plotting function 
    # itself uses. Parameters for matplotlib's functions are done
    # through `matplotlib_arguments`.
    fit_gaussian = core.config.extract_configuration(
        config_object=config, keys=['histogram','fit_gaussian'])
    # Compile the configuration parameters for the plotting function.
    plot_arguments = {'fit_gaussian':fit_gaussian}

    # Extract configuration parameters for the inner matplotlib 
    # function that the plotting function uses.
    log = core.config.extract_configuration(
        config_object=config, keys=['histogram','log_plot'])
    # Compile the configuration parameters for the matplotlib 
    # function that is the base of the plotting function.
    matplotlib_arguments = {'log':log}

    
    # The plotting function
    plotting_function = plot_gaussian_histogram

    # Run the function. The base function is used as the 
    # standard template.
    plot.base.create_directory_plot_files(
        data_directory=data_directory, plotting_function=plotting_function,
        figure_arguments=figure_arguments,
        plot_arguments=plot_arguments, 
        matplotlib_arguments=matplotlib_arguments)

    # All done.
    return None