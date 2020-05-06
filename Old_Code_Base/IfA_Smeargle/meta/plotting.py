"""

This module just adds some shortcut calling functions to functionality of plotting functions
and related methods. 

Although the implementation of the entire functionality module is supposed to be untouched,
it is still suggested that these functions be used over custom approaches when applicable. 

"""

import astropy as ap
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sp_sig
import scipy.stats as sp_stat
import sys

from IfA_Smeargle.meta import *

def smeargle_save_figure_file(figure, file_name,
                              title=None, close_figure=True):
    """ This function just saves a figure to a file to a name provided.

    Because of some oddities with Matplotlib, saving a file within a function 
    and exiting said function (or overwriting in a loop its variable) with a 
    new figure causes two figures to be saved in parallel. This is very 
    memory intensive, so closing a saved figure is ideal.
    
    This function does it so the user or Smeargle lines do not need to care 
    about it.

    Parameters
    ----------
    figure : Matplotlib Figure
        This is the figure to be saved to a file.
    file_name : string
        This is the file string name for the figure to be saved. It should 
        already have the appropriate extension. If not, it defaults to pdf. 
    title : string (optional)
        This is the title for the figure plot. Although it can be added from 
        here, it is not advised.
    close_figure : boolean (optional)
        This specifies if the figure should be closed. Given that this 
        function is built for that, this should not be changed.

    Returns
    -------
    return_none : None
        Nothing

    Note
    ----
    The file type checking logic is not the smartest implementation.
    
    """

    # Warn about the build up of memory if the figure is not closed.
    if (not close_figure):
        smeargle_warning(MemoryWarning, ("The figure will not be released from RAM. An "
                                         "excessive amount of figures will be very memory "
                                         "intensive. Why this function is being used without "
                                         "its closing functionality is beyond Sparrow."))

    # Checking or applying file ending configuration.
    supported_file_types = figure.canvas.get_supported_filetypes()
    supported_file_types = list(supported_file_types.keys())
    if any(('.' + typedex) in file_name[-7:] for typedex in supported_file_types):
        # The there seems to be a supported file type already in here.
        pass
    else:
        # There does not seem to be an appropriate file extension. 
        # Add one (pdf).
        file_name += '.pdf'

    # Apply the title if provided, if the format isn't applicable, trash.
    if (title is not None):
        if (isinstance(title, str)):
            figure.suptitle(title)
        else:
            # Doesn't seem to be a string...
            smeargle_warning(InputWarning, ("The title parameter has been provided, but as it "
                                            "is not a string, it cannot be applied to the "
                                            "figure. The title will not be applied."))

    # Save to file then remove figure from RAM if specified.
    figure.savefig(file_name)
    if (close_figure):
        plt.close(figure)
        del figure

    return None