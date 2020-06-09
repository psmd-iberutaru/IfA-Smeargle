
"""
This creates a plot of a heat-map from analysis fits files.
"""

import numpy as np
import numpy.ma as np_ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import mpl_toolkits.axes_grid1 as mpltk_axg1

import ifa_smeargle.core as core
import ifa_smeargle.plotting as plot

def plot_heatmap(data_array, data_header=None, data_mask=None, 
                 figure_axes=None, matplotlib_arguments=None,
                 **kwargs):
    """ A function to create a heat-map image of the data array 
    provided.
    
    This function replicates the image plotting functionality of 
    Tino Well's program. (Found here: 
    https://github.com/tinowells/ifa). More specifically, the plot 
    assigns a color according to the value a pixel has, and plots 
    it corresponding to its location in the provided data array.

    Parameters
    ----------
    data_array : ndarray
        This is the provided array that is to be plotted. 
        Dimensions matter!
    data_header : Astropy Header (optional)
        This is the data header of the fits file. If it is not 
        provided, plotting parameters which use it will not be plot.
        An error may also be raised.
    data_mask : ndarray (optional)
        The mask that should be applied to the `data_array`.
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire 
        to have the heat-map plot to. This defaults to either making 
        new ones, or using the currently defined axes. Note: This 
        is not deep-copied!
    matplotlib_arguments : dictionary (optional)
        These are options the user may use to pass customization 
        parameters into the heat-map plot or the color-bar 
        functionalities.
        See :py:func:`~.matplotlib.pyplot.imshow` and 
        :py:func:`~.matplotlib.pyplot.colorbar`.

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
        run_param = data_header.get('heatmap_run', default=False)
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
        raise core.error.DataError("The `heatmap_run` parameter is not in "
                                   "this file's header. This file was not "
                                   "analyzed by the proper function to "
                                   "prepare the data for plotting.")

    # If the user provided a mask, apply it. Otherwise, use a blank
    # mask.
    if (data_mask is not None):
        # The mask exists so it shall be applied. Override whatever
        # the data object itself has.
        plot_data = np_ma.array(np_ma.getdata(data_array, False), 
                                mask=data_mask)
    elif (isinstance(data_array, np_ma.MaskedArray)):
        # The object is already a masked array, deferring to the 
        # user here.
        plot_data = data_array
        core.error.ifas_info("The provided data array is a masked "
                             "array. Its mask will be applied to the "
                             "heat-map.")
    else:
        # There is no mask, so none shall be applied.
        plot_data = np_ma.array(data_array, mask=np_ma.nomask)


    # If the data array is not the proper dimensions, bark. 
    # Rewriting the Astropy errors for context.
    if (plot_data.ndim == 0):
        raise core.error.DataError("This data array has no dimensions "
                                   "(data_array.ndim=0). A heat-map plot "
                                   "cannot be logically constructed.")
    elif (plot_data.ndim == 1):
        # This is technically a valid data set, but, still warn as 
        # it is unusual.
        core.error.ifas_warning(core.error.DataWarning, 
                                ("This data array only has one dimension. "
                                 "Plotting will continue despite this "
                                 "unusual data input."))
    elif (plot_data.ndim == 2):
        # Normal operations
        pass
    elif (plot_data.ndim >= 3):
        raise core.error.DataError("A heat map cannot be logically "
                                   "constructed from a 3+ dimensional "
                                   "data set. Current number of dimensions "
                                   "of data set is:  {ndim}"
                                   .format(ndim=str(plot_data.ndim)))
    else:
        raise core.error.BrokenLogicError("The data array apparently "
                                          "doesn't have a compatible "
                                          "dimensional number. The "
                                          "dimensional number is:  {ndim}"
                                          .format(ndim=plot_data.ndim))


    # First, figure out what type of Matplotlib axes to use. 
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()


    # Color-map. This is a very roundabout way for customization 
    # because for some reason using a normal color-bar class gives 
    # a very weird error.
    if ('cmap' in matplotlib_arguments):
        pass
    else:
        colormap = mpl_cm.rainbow
        colormap.set_bad('black',1.)
        matplotlib_arguments['cmap'] = colormap

    # Finally plotting. Extract the needed parameters too.
    interpolation = matplotlib_arguments.pop('interpolation', None)
    cmap = matplotlib_arguments.pop('cmap', None)
    heatmap = ax.imshow(plot_data, origin='lower', 
                        interpolation=interpolation, cmap=cmap,
                        **matplotlib_arguments)

    # Make color bar match the graph size. There seems to be two 
    # ways of doing this; pragmatically and magically. Default 
    # is pragmatically. 
    _magic = False
    if (_magic):
        # See https://stackoverflow.com/a/26720422
        core.error.ifas_warning(core.error.MagicWarning,
                                ("The colorbar location and scale are being "
                                 "set by magic values. Use this if and only "
                                 "if the pragmatic method fails."))
        plt.colorbar(mappable=heatmap, fraction=0.046, pad=0.04)
    else:
        # See https://stackoverflow.com/a/18195921
        divider = mpltk_axg1.make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(mappable=heatmap, cax=cax, ax=ax, 
                     **matplotlib_arguments)

    # Return some information about how much masked pixels there 
    # are, if any.
    ax.text(plot_data.shape[1],plot_data.shape[0],
            'Masked: {masked} / {total}'.format(
                masked=np_ma.count_masked(plot_data),
                total=plot_data.size),
            verticalalignment='bottom', horizontalalignment='right', 
            fontsize='medium')

    return ax


def script_plot_heatmap(config):
    """ The scripting version of `plot_heatmap`. This function 
    automatically creates heat-map plots for each and every analysis
    data file.
    
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
    pass
    # Compile the configuration parameters for the plotting function.
    plot_arguments = {}

    # Extract configuration parameters for the inner matplotlib 
    # function that the plotting function uses.
    interpolation = core.config.extract_configuration(
        config_object=config, keys=['heatmap','interpolation'])
    # Compile the configuration parameters for the matplotlib 
    # function that is the base of the plotting function.
    matplotlib_arguments = {'interpolation':interpolation}

    
    # The plotting function
    plotting_function = plot_heatmap

    # Run the function. The base function is used as the 
    # standard template.
    plot.base.create_directory_plot_files(
        data_directory=data_directory, plotting_function=plotting_function,
        figure_arguments=figure_arguments,
        plot_arguments=plot_arguments, 
        matplotlib_arguments=matplotlib_arguments)

    # All done.
    return None