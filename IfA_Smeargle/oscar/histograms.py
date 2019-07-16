
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
                         figure_axes=None, fit_gaussian=True,
                         histogram_plot_paramters={'bins':50, 'range':[-10,10]}):
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
    # Extract proper data.
    data_array = oscar.oscar_funct.oscar_convert_data_inputs(data_array)

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


    # Derive histogram data, and double as plotting functionality.
    hist_data = ax.hist(plotting_data, **histogram_plot_paramters)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]
    # Personally, Sparrow does not find this helpful to look at.
    # ax.plot(hist_x,hist_y)

    if (fit_gaussian):
        # Plotting/fitting the Gaussian function.  For some reasons beyond 
        # what I can explain, Astropy seems to have better fitting 
        # capabilities, in this specific application, than Scipy.
        gaussian_init = ap_mod.models.Gaussian1D(amplitude=1.0, mean=0, stddev=1.0)
        gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
        gaussian_fit = gaussian_fit_model(gaussian_init, hist_x, hist_y)
        # For better plotting resolution.
        temp_gauss_x_axis = np.linspace(hist_x.min() - 1, hist_x.max() + 1, hist_x.size * 10)
        ax.plot(temp_gauss_x_axis, gaussian_fit(temp_gauss_x_axis), 
                linewidth=1.5, color='black')

        # Deriving basic information form Gaussian model to return back to 
        # the user.
        gaussian_mean = gaussian_fit.mean.value
        gaussian_stddev = gaussian_fit.stddev.value
        gaussian_amplitude = gaussian_fit.amplitude.value
        gaussian_max = np.max(gaussian_fit(temp_gauss_x_axis))
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
        counts_label = mpl_patch.Patch(color='blue', 
                                       label='Counts')
        center_label = mpl_patch.Patch(color=mean_stddev_colors[2], linewidth=1, 
                                       label='μ = {val}'.format(val=gaussian_mean)[:9])
        stddev_label = mpl_patch.Patch(color=mean_stddev_colors[1], linewidth=1, 
                                        label='σ = {val}'.format(val=gaussian_stddev)[:9])
        peak_label = mpl_patch.Patch(color='orange', 
                                     label='Max = {val}'.format(val=gaussian_max)[:12])
        ax.legend(handles=[counts_label,center_label,stddev_label,peak_label],
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

    # That should be it.
    return ax, gaussian_fit_atributes

