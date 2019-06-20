"""
    The main objective of the HOTEL line is to create plots and histograms displaying and 
    categorizing different elements of arrays and specifically defined sub-arrays.

    Most of the procedures derived from this module element is derived from 
    https://github.com/tinowells/ifa, as an extension and generalization of said project. 
"""

import astropy as ap
import astropy.io.fits as ap_fits
import astropy.modeling as ap_mod
import copy
import matplotlib as mpl
import matplotlib.cm as mpl_cm
import matplotlib.patches as mpl_patch
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import scipy as sp

from ..meta import *


def plot_array_heatmap_image(data_array,
                             figure_axes=None,  
                             heatmap_plot_parameters={'interpolation':'nearest'},
                             colorbar_plot_paramters={'orientation':'vertical'}):
    """ A function to create a heatmap image of the data array provided.
    
    This function replicates the image plotting functionality of Tino Well's program. 
    (Found here: https://github.com/tinowells/ifa). More specifically, the plot assigns a color
    according to the value a pixel has, and plots it corresponding to its location in the
    provided data array.

    Parameters
    ----------
    data_array : ndarray
        This is the provided array that is to be plotted. Dimensions matter!
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have the heatmap plot 
        to. This defaults to either making new ones, or using the currently defined axes. Note! 
        This is not deep-copied.

    heatmap_plot_parameters : dictionary <config>
        These are options the user may use to pass customization parameters into the heatmap plot
        functionality. See :py:function:`~.matplotlib.pyplot.imshow`.
    colorbar_plot_paramters : dictionary <config>
        These are options the user may use to pass customization parameters into the colorbar 
        class functionality. See :py:function:`~.matplotlib.pyplot.colorbar`.

    Returns
    -------
    heatmap_plot_axes : Matplotlib Axes
        This is the heatmap plot made on the (provided, borrowed, or generated) plotting axes.
    
    """

    # First, figure out what type of Matplotlib axes to use. 
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()

    # Color-map. This is a very roundabout way for customization because for some reason using a 
    # normal colorbar class gives a very weird error.
    if ('cmap' in heatmap_plot_parameters):
        pass
    else:
        colormap = mpl_cm.plasma
        colormap.set_bad('black',1.)
        heatmap_plot_parameters['cmap'] = colormap

    # Finally plotting.
    heatmap = ax.imshow(data_array, **heatmap_plot_parameters)
    plt.colorbar(mappable=heatmap, ax=ax, **colorbar_plot_paramters)

    #Return some information about how much masked pixels there are, if any.
    ax.text(data_array.shape[1],0,
            'Masked: {masked} / {total}'.format(
                masked=np_ma.count_masked(data_array),total=data_array.size),
            verticalalignment='bottom',horizontalalignment='right',fontsize='large')

    return ax




def plot_array_histogram(data_array, 
                         figure_axes=None, fit_gaussian=True,
                         histogram_plot_paramters={'bins':50, 'range':[-10,10]}):
    """ A function to create and plot histogram plots for better analysis of a given array.

    This function replicates the histogram plotting functionality of Tino Well's program. 
    (Found here: https://github.com/tinowells/ifa). More specifically, it attempts to plot 
    histograms of pixel data; then, the program attempts to fit a Gaussian function. 

    Parameters
    ----------
    data_array : ndarray
        This is the data array that is expected to be analyzed and have histograms made. 
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have the histogram plot 
        to. This defaults to either making new ones, or using the currently defined axes. Note! 
        This is not deep-copied.
    fit_gaussian : boolean (optional)
        This parameter regulates if the function should replicate the Gaussian function fitting.

    histogram_plot_parameters : dictionary <config>
        These are options the user may use to pass customization parameters into the histogram plot
        functionality. See :py:function:`~.matplotlib.pyplot.hist`. 

    Returns
    -------
    histogram_plot_axes : Matplotlib Axes
        This is the histogram plot made on the (provided, borrowed, or generated) plotting axes. 
    gaussian_fit_atributes : dictionary
        This is a dictionary of the mean, stddev, amplitude, and maximum of the computed/fit 
        Gaussian model.

    Notes
    -----
    If the ``histogram_plot_parameters`` specifies that the histogram plot should be logarithmic,
    the Gaussian function will be disabled because of some incompatibilities. 

    """

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
    except KeyError:
        # It does not exist.
        pass

    # Be able to accept both masked arrays and standard arrays and be able to tell.
    if (np_ma.is_masked(data_array)):
        plotting_data = data_array.compressed()
    else:
        plotting_data = data_array.flatten()


    # Derive histogram data, and double as plotting functionality.
    hist_data = ax.hist(plotting_data, **histogram_plot_paramters)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Derive middle of bin.
    hist_y = hist_data[0]
    # Personally, Sparrow does not find this helpful to look at.
    # ax.plot(hist_x,hist_y)

    if (fit_gaussian):
        # Plotting/fitting the Gaussian function.  For some reasons beyond what I can explain, 
        # Astropy seems to have better fitting capabilities, in this specific application, 
        # than Scipy.
        gaussian_init = ap_mod.models.Gaussian1D(amplitude=1.0, mean=0, stddev=1.0)
        gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
        gaussian_fit = gaussian_fit_model(gaussian_init, hist_x, hist_y)
        # For better plotting resolution.
        temp_gauss_x_axis = np.linspace(hist_x.min() - 1, hist_x.max() + 1, hist_x.size * 10)
        ax.plot(temp_gauss_x_axis, gaussian_fit(temp_gauss_x_axis), 
                linewidth=1.5, color='black')

        # Deriving basic information form Gaussian model to return back to the user.
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


def plot_single_heatmap_and_histogram(data_array,
                                      figure_subplot_parameters={'figsize':(9,3.5), 'dpi':100},
                                      plot_heatmap_parameters={},
                                      plot_histogram_parameters={}):
    """ This extracts data from a single data array, plotting a histogram and heatmap.

    This function attempts to plot both a histogram and a heatmap side-by-side given a data
    array. Although all of the customizable parameters may be sent via the dictionary, this
    is not the suggested method if extreme customization of the figure is needed. However,
    if the current arrangement is fine, then so too should this function be.

    Parameters
    ----------
    data_array : ndarray
        This is the data array that is expected to be analyzed and have histograms made. 

    figure_subplot_parameters : dictionary <config>
        These are parameters that are passed straight into the subplot routine to make the figure.
    plot_heatmap_parameters : dictionary <config>
        These are parameters that are passed directly into 
        :py:function:`~.plot_array_heatmap_image`.
    plot_histogram_parameters : dictionary <config>
        These are parameters that are passed directly into 
        :py:function:`~.plot_array_histogram`.

    Returns
    -------
    final_figure : Matplotlib Figure
        This is the final figure made of the heatmap and the histogram.
    """

    # Generate the figure, also use the user's specifications.
    fig, ax = plt.subplots(1, 2,**figure_subplot_parameters)

    # Plotting both figures in their respective areas side by side. Again, use user
    # specifications.
    plot_array_heatmap_image(data_array, figure_axes=ax[0], **plot_heatmap_parameters)
    plot_array_histogram(data_array, figure_axes=ax[1], **plot_histogram_parameters)
    
    # The histogram feels squished unless the axes ratios are modified.
    ax[1].set_aspect(1/(ax[1].get_data_ratio() * 1.5))

    # Visual modifications and cleanup to the final figure.
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)

    # Only done for naming conventions on the documentation.
    final_figure = fig

    return final_figure

