
"""
This file contains all of the different methods that a heatmap can be plotted.

"""

import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1 as mpltk_axg1
import numpy as np
import numpy.ma as np_ma

from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar

def plot_array_heatmap_image(data_array,
                             figure_axes=None, plot=True,
                             heatmap_plot_parameters={'interpolation':'nearest'},
                             colorbar_plot_paramters={'orientation':'vertical'},
                             **kwargs):
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
        See :py:func:`~.matplotlib.pyplot.imshow`.
    colorbar_plot_paramters : dictionary <config>
        These are options the user may use to pass customization parameters 
        into the colorbar class functionality. 
        See :py:func:`~.matplotlib.pyplot.colorbar`.

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

    # The rest of the computations require a Numpy array. Forcibly 
    # establishing it. Adapt for masked arrays.
    data_array = meta_faa.smeargle_remake_array(data_array, np_ma.masked_array)

    # If the data array is not the proper dimensions. Rewriting the Astropy
    # error for context.
    if (data_array.ndim == 0):
        raise DataError("This data array has no dimensions (ndim=0). A heatmap cannot be "
                        "logically constructed.")
    elif (data_array.ndim == 1):
        # This is technically a valid data set, but, still warn as it is 
        # unusual.
        smeargle_warning(DataWarning, ("This data array only has one dimension. Plotting will "
                                       "continue despite this unusual data input."))
    elif (data_array.ndim == 2):
        # Normal operations
        pass
    elif (data_array.ndim >= 3):
        raise DataError("A heat map cannot be logically constructed from a 3+ dimensional "
                        "data set. Current number of dimensions of data set is:  {ndim}"
                        .format(ndim=str(data_array.ndim)))
    else:
        raise BrokenLogicError("The data array apparently doesn't have a compatible "
                               "dimensional number. The dimensional number is:  {ndim}"
                               .format(ndim=data_array.ndim))


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
        colormap = mpl_cm.rainbow
        colormap.set_bad('black',1.)
        heatmap_plot_parameters['cmap'] = colormap

    # Finally plotting.
    heatmap = ax.imshow(data_array, origin='lower', **heatmap_plot_parameters)

    # Make color bar match the graph size. There seems to be two ways of doing
    # this; pragmatically and magically. Default is pragmatically. 
    _magic = False
    if (_magic):
        # See https://stackoverflow.com/a/26720422
        smeargle_warning(MagicWarning, "The colorbar location and scale are being set by magic " 
                                       "values. Use this if and only if the pragmatic method "
                                       "fails.")
        plt.colorbar(mappable=heatmap, fraction=0.046, pad=0.04)
    else:
        # See https://stackoverflow.com/a/18195921
        divider = mpltk_axg1.make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(mappable=heatmap, cax=cax, ax=ax, **colorbar_plot_paramters)

    # Return some information about how much masked pixels there are, if any.
    ax.text(data_array.shape[1],data_array.shape[0],
            'Masked: {masked} / {total}'.format(
                masked=np_ma.count_masked(data_array),total=data_array.size),
            verticalalignment='bottom', horizontalalignment='right', fontsize='medium')

    return ax


