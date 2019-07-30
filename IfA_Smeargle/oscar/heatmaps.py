
"""
This file contains all of the different methods that a heatmap can be plotted.

"""

import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
import numpy.ma as np_ma

from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar

def plot_array_heatmap_image(data_array,
                             figure_axes=None, plot=True,
                             heatmap_plot_parameters={'interpolation':'nearest'},
                             colorbar_plot_paramters={'orientation':'vertical'}):
    """ A function to create a heatmap image of the data array provided.
    
    This function replicates the image plotting functionality of Tino Well's 
    program. (Found here: https://github.com/tinowells/ifa). More 
    specifically, the plot assigns a color according to the value a pixel 
    has, and plots it corresponding to its location in the provided data 
    array.

    Parameters
    ----------
    data_array : ndarray or string
        This is the provided array that is to be plotted. Dimensions matter! 
        May also be a fits file.
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have 
        the heatmap plot to. This defaults to either making new ones, or 
        using the currently defined axes. Note: This is not deep-copied!
    plot : boolean (optional)
        A flag to check if this plotting function should be run. A component 
        in the mutli-plot functions.

    heatmap_plot_parameters : dictionary <config>
        These are options the user may use to pass customization parameters 
        into the heatmap plot functionality. 
        See :py:function:`~.matplotlib.pyplot.imshow`.
    colorbar_plot_paramters : dictionary <config>
        These are options the user may use to pass customization parameters 
        into the colorbar class functionality. 
        See :py:function:`~.matplotlib.pyplot.colorbar`.

    Returns
    -------
    heatmap_plot_axes : Matplotlib Axes
        This is the heatmap plot made on the (provided, borrowed, or 
        generated) plotting axes.
    
    """
    # Decide if we even plot.
    if (not plot):
        # We're not plotting today.
        return None


    # First, figure out what type of Matplotlib axes to use. 
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()

    # Extract proper data.
    data_array = oscar.oscar_convert_data_inputs(data_array)

    # Color-map. This is a very roundabout way for customization because for 
    # some reason using a normal colorbar class gives a very weird error.
    if ('cmap' in heatmap_plot_parameters):
        pass
    else:
        colormap = mpl_cm.plasma
        colormap.set_bad('black',1.)
        heatmap_plot_parameters['cmap'] = colormap

    # Finally plotting.
    heatmap = ax.imshow(data_array, **heatmap_plot_parameters)
    plt.colorbar(mappable=heatmap, ax=ax, **colorbar_plot_paramters)

    # Return some information about how much masked pixels there are, if any.
    ax.text(data_array.shape[1],0,
            'Masked: {masked} / {total}'.format(
                masked=np_ma.count_masked(data_array),total=data_array.size),
            verticalalignment='bottom',horizontalalignment='right',fontsize='large')

    return ax


