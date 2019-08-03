
"""
This contains all of the histogram plotting methods.
"""

import astropy.modeling as ap_mod
import matplotlib.patches as mpl_patch
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma

from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar

def plot_array_histogram(data_array, 
                         figure_axes=None, fit_gaussian=True, bin_width=None,
                         plot=True,
                         histogram_plot_paramters={}):
    """ A function to create and plot histogram plots for better analysis of 
    a given array.

    This function replicates the histogram plotting functionality of Tino 
    Well's program. (Found here: https://github.com/tinowells/ifa). More 
    specifically, it attempts to plot histograms of pixel data; then, the 
    program attempts to fit a Gaussian function. 

    Parameters
    ----------
    data_array : ndarray or string
        This is the data array that is expected to be analyzed and have 
        histograms made. May also be a fits file.
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have 
        the histogram plot to. This defaults to either making new ones, or 
        using the currently defined axes. Note: This is not deep-copied!
    fit_gaussian : boolean (optional)
        This parameter regulates if the function should replicate the 
        Gaussian function fitting.
    bin_width : boolean (optional)
        Matplotlib is not nice with bin widths, if it is an integer, widths 
        are applied instead.
    plot : boolean (optional)
        A flag to check if this plotting function should be run. A component 
        in the mutli-plot functions. Defaults to true.

    histogram_plot_parameters : dictionary <config>
        These are options the user may use to pass customization parameters 
        into the histogram plot functionality. 
        See :py:function:`~.matplotlib.pyplot.hist`. 

    Returns
    -------
    histogram_plot_axes : Matplotlib Axes
        This is the histogram plot made on the (provided, borrowed, or 
        generated) plotting axes. 
    gaussian_fit_atributes : dictionary
        This is a dictionary of the mean, stddev, amplitude, and maximum of 
        the computed/fit Gaussian model.

    Notes
    -----
    If the ``histogram_plot_parameters`` specifies that the histogram plot 
    should be logarithmic, the Gaussian function will be disabled because of 
    some incompatibilities. 

    """

    # Decide if we even plot.
    if (not plot):
        # We're not plotting today.
        return None

    # Extract proper data.
    data_array = oscar.oscar_convert_data_inputs(data_array)

    # First, figure out what type of Matplotlib axes to use.
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()

    # Check to see if the user specified a log histogram.
    try:
        # In the event that the value they gave is not strictly boolean.
        if (histogram_plot_paramters['log'] == True):
            fit_gaussian = False
        else:
            smeargle_warning(InputWarning,("The histogram plot parameter for log plotting is not "
                                           "None or True; the unreadable input is ignored. "))
    except KeyError:
        # It does not exist.
        pass

    # Be able to accept both masked arrays and standard arrays and be able 
    # to tell.
    if (np_ma.is_masked(data_array)):
        plotting_data = data_array.compressed()
    else:
        plotting_data = data_array.flatten()

    # Test for bin width instead of numbers.
    if (isinstance(bin_width,(int,float))):
        histogram_plot_paramters['bins'] = oscar.oscar_bin_width(plotting_data, bin_width)
    else:
        bin_width = data_array.ptp() / float(np.nanmax(histogram_plot_paramters['bins']))

    # Range is not used when bin sequences are provided. Allow for a patch 
    # that would return data as expected.
    if (('range' in histogram_plot_paramters) and 
        (isinstance(histogram_plot_paramters['bins'],np.ndarray))):
        # The user provided their own range parameter, "override" the bin
        # with parameter by using a different bin width system.
        min_range = histogram_plot_paramters['range'][0]
        max_range = histogram_plot_paramters['range'][-1]

        # Apply the bins
        histogram_plot_paramters['bins'] = oscar.oscar_bin_width(None, bin_width,
                                                                 local_minimum=min_range,
                                                                 local_maximum=max_range)
    else:
        pass

    # Derive histogram data, and double as plotting functionality.
    hist_data = ax.hist(plotting_data, **histogram_plot_paramters)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]
    # Personally, Sparrow does not find this helpful to look at.
    # ax.plot(hist_x,hist_y)

    if (fit_gaussian):
        # Fit a Gaussian to the data.
        gauss_funt, gauss_param = \
            meta_model.smeargle_fit_histogram_gaussian_function(plotting_data, bin_width)

        # For better plotting resolution.
        temp_gauss_x_axis = np.linspace(np.nanmin(hist_x) - 1, np.nanmax(hist_x) + 1, 
                                        hist_x.size * 10)
        ax.plot(temp_gauss_x_axis, gauss_funt(temp_gauss_x_axis), 
                linewidth=1.5, color='black')

        # Deriving basic information form Gaussian model to return back to 
        # the user.
        gaussian_mean = gauss_param['mean']
        gaussian_stddev = gauss_param['stddev']
        gaussian_amplitude = gauss_param['amplitude']
        gaussian_max = np.nanmax(gauss_funt(temp_gauss_x_axis))
        gaussian_fit_atributes = {'mean': gaussian_mean, 'stddev': gaussian_stddev,
                                  'amplitude': gaussian_amplitude,'max' : gaussian_max}

        # Center line and +/- 1 or 2 sigma vertical lines.
        mean_stddev_lines = gaussian_mean + gaussian_stddev * np.array([-2,-1,0,1,2])
        mean_stddev_colors = ['red', 'red', 'purple', 'red', 'red']
        line_patterns = ['dotted','dashed','solid','dashed','dotted']
        for linedex, colordex, patterndex in zip(mean_stddev_lines, 
                                                 mean_stddev_colors, 
                                                 line_patterns):
            ax.axvline(x=linedex, linestyle=patterndex, color=colordex, alpha=0.75)
        # Gaussian peak value horizontal line.
        ax.axhline(y=gaussian_max, color='orange', alpha=0.75)

        # Manually assigning legend elements.
        center_label = mpl_patch.Patch(color=mean_stddev_colors[2], linewidth=1, 
                                       label='μ = {0:.3f}'.format(gaussian_mean))
        stddev_label = mpl_patch.Patch(color=mean_stddev_colors[1], linewidth=1, 
                                        label='σ = {0:.3f}'.format(gaussian_stddev))
        peak_label = mpl_patch.Patch(color='orange', 
                                     label='Max = {0:.3f}'.format(gaussian_max))
        ax.legend(handles=[center_label,stddev_label,peak_label],
                  markerscale=0.75, fontsize='small',
                  loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=4)
    elif not (fit_gaussian):
        # There is no Gaussian information to return.
        gaussian_fit_atributes = None
    else:
        raise BrokenLogicError("The program should not have entered here. Please contact "
                               "developers with proper information.")
    
    # Basic axis labels.
    ax.set_xlabel('Pixel Values')
    ax.set_ylabel('Count Quantity')

    # If the range has been set, adhere to it. Have a fall back in the event 
    # The user may have messed up.
    if ('range' in histogram_plot_paramters):
        left_range = (np.nanmin(histogram_plot_paramters.get('range', np.nanmin(plotting_data))) 
                      - 1)
        right_range = (np.nanmax(histogram_plot_paramters.get('range', np.nanmax(plotting_data))) 
                       + 1)
        ax.set_xlim(left_range, right_range)

    # That should be it.
    return ax, gaussian_fit_atributes

