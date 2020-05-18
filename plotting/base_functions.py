
"""
These are the base functions that are common to the entire plotting
functionality.
"""

import matplotlib.pyplot as plt

import numpy as np
import numpy.ma as np_ma

import IfA_Smeargle.core as core
import IfA_Smeargle.analysis as analysis


def write_plot_file(file_name, figure, title=None, close_figure=True):
    """ This function just saves a figure to a file to a name 
    provided.

    Because of some oddities with Matplotlib, saving a file within 
    a function and exiting said function (or overwriting in a loop 
    its variable) with a new figure causes two figures to be saved 
    in parallel. This is very memory intensive, so closing a saved 
    figure is ideal. This function does this by default.

    Parameters
    ----------
    file_name : string
        This is the file string name for the figure to be saved. It 
        should already have the appropriate extension. If not, it 
        defaults to the configuration default. 
    figure : Matplotlib Figure
        This is the figure to be saved to a file.
    title : string (optional)
        This is the title for the figure plot. Although it can be 
        added from here, it is not advised; the original function 
        creating the plot should do it instead.
    close_figure : boolean (optional)
        This specifies if the figure should be closed. Given that 
        this function is built for that, this should not be changed.

    Returns
    -------
    Nothing

    Note
    ----
    The file type checking logic is not the smartest implementation.
    
    """

    # Warn about the build up of memory if the figure is not closed.
    if (not close_figure):
        core.error.ifas_warning(core.error.MemoryWarning, 
                                ("The figure will not be released from RAM. "
                                 "An excessive amount of figures will be "
                                 "very memory intensive. Why this function "
                                 "is being used without its closing "
                                 "functionality is beyond Sparrow."))

    # Checking or applying file ending configuration.
    supported_file_types = figure.canvas.get_supported_filetypes()
    supported_file_types = list(supported_file_types.keys())
    if (any(('.' + typedex) in file_name[-7:] 
            for typedex in supported_file_types)):
        # The there seems to be a supported file type already in 
        # here.
        pass
    else:
        # There does not seem to be an appropriate file extension. 

        file_name = core.strformat.combine_pathname(
            file_name=[file_name], extension=['.pdf'])

    # Apply the title if provided. If the format isn't applicable, 
    # ignore the input.
    if (title is not None):
        if (isinstance(title, str)):
            figure.suptitle(title)
        else:
            # Doesn't seem to be a string...
            core.error.ifas_warning(core.error.InputWarning,
                                    ("The title parameter has been provided, "
                                     "but as it is not a string, it cannot "
                                     "be applied to the figure. The title "
                                     "will not be applied."))

    # Save to file then remove figure from RAM if specified.
    figure.savefig(file_name, bbox_inches='tight')
    if (close_figure):
        plt.close(figure)
        del figure

    return None


def create_directory_plot_files(data_directory, plotting_function,
                                figure_arguments,
                                plot_arguments, matplotlib_arguments):
    """ This function is the common function to create plots for 
    all analysis fits files.

    Parameters
    ----------
    data_directory : string
        The data directory by which all of data for the analysis
        is contained within.
    plotting_function : function
        This is the plotting function that will be applied to all
        analysis fits files. 
    figure_arguments : dictionary
        The plotting arguments that will be sent to the function
        that creates the function.s
    plot_arguments : dictionary
        Custom arguments that shall be given to the plotting 
        function. For arguments that should be sent to the 
        matplotlib function, use `matplotlib_arguments`.
    matplotlib_arguments : dictionary
        Custom arguments that shall be given to the matplotlib 
        functions. For arguments that should be sent to the 
        plotting function, use `plot_arguments`.

    Returns
    -------
    None
    
    """

    # Obtain all of the analysis files within the data directory 
    # provided.
    analysis_file_list = analysis.base.get_analysis_fits_filenames(
        data_directory=data_directory, recursive=False)

    # For each of the files, read them, plot, and write the plot
    # to file.
    for filedex in analysis_file_list:
        # Read the file into memory.
        __, hdu_header, hdu_data= core.io.read_fits_file(file_name=filedex, 
                                                         silent=True)
        # If the data array has a mask, then it will be shown as
        # nans. Masked arrays are the best way to handle this.
        masked_array = np_ma.fix_invalid(hdu_data)
        raw_data = np_ma.getdata(masked_array)
        mask = np_ma.getmaskarray(masked_array)

        # Creating the figure that will be saved.
        fig, ax = plt.subplots(1, 1,**figure_arguments)

        # Run the plotting function to create the plot that is 
        # desired.
        plot = plotting_function(data_array=hdu_data, data_header=hdu_header, 
                                 data_mask=mask, figure_axes=None,
                                 matplotlib_arguments=matplotlib_arguments,
                                 **plot_arguments)
        ax = plot

        # The file name of the plot. The core will generally be the 
        # root file name.
        root_filename = str(filedex).split('.')[0]
        figure_filename = core.strformat.combine_pathname(
            file_name=[root_filename, '__', plotting_function.__name__])

        # Save the plot to file.
        write_plot_file(file_name=figure_filename, figure=fig, 
                        title=None, close_figure=True)

    # All done?