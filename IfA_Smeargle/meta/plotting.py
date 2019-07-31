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

from IfA_Smeargle.meta import *

def smeargle_fit_gaussian_function(x_data, y_data, inital_guesses):
    """ This function fits a Gaussian function to a specific set of data.

    Gaussian fitting is hard, this function exists as a port so that 
    all fitting functions use the same algorithm and said algorithm is easy
    to change.
    
    Parameters
    ----------
    x_data : ndarray
        The X data that the Gaussian will be fit over.
    y_data : ndarray
        The Y data that the Gaussian will be fit over.
    inital_guesses : dictionary
        Initial guesses for the Gaussian fitting function.

    Returns
    -------
    gaussian_function : function
        A callable function that when provided an X value, it will return
        the value of the function.
    gaussian_parameters : dictionary
        A compiled dictionary of all of the parameters of the Gaussian fit.
    """

    # Extract the initial guesses.
    try: 
        guess_mean = inital_guesses['mean'] 
    except Exception: 
        guess_mean = 0
    try:
        guess_stddev = inital_guesses['stddev']
    except Exception:
        guess_stddev = 1
    try:
        guess_amplitude = inital_guesses['amplitude']
    except Exception:
        guess_amplitude = 1

    # Plotting/fitting the Gaussian function.  For some reasons beyond 
    # what Sparrow can explain, Astropy seems to have better fitting 
    # capabilities, in this specific application, than Scipy.
    gaussian_init = ap_mod.models.Gaussian1D(amplitude=guess_amplitude, 
                                             mean=guess_mean, 
                                             stddev=guess_stddev)
    gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
    gaussian_fit = gaussian_fit_model(gaussian_init, x_data, y_data)

    # Deriving basic information form Gaussian model to return back to 
    # the user.
    gaussian_mean = gaussian_fit.mean.value
    gaussian_stddev = gaussian_fit.stddev.value
    gaussian_amplitude = gaussian_fit.amplitude.value
    temp_gauss_x_axis = np.linspace(x_data.min() - 1, x_data.max() + 1, x_data.size * 100)
    gaussian_max = np.max(gaussian_fit(temp_gauss_x_axis))
    gaussian_parameters = {'mean': gaussian_mean, 'stddev': gaussian_stddev,
                           'amplitude': gaussian_amplitude,'max' : gaussian_max}

    # The Gaussian function
    gaussian_function = lambda input: gaussian_fit(np.array(input))

    return gaussian_function, gaussian_parameters

def smeargle_fit_histogram_gaussian_function(data_array):
    """ This function fits a Gaussian function to a specific set of data.

    Gaussian fitting is hard, this function exists as a port so that 
    all fitting functions use the same algorithm and said algorithm is easy
    to change. This applies it to the histogram of the data.
    
    Parameters
    ----------
    x_data : ndarray
        The data that the histogram gaussian function is fitting.

    Returns
    -------
    gaussian_function : function
        A callable function that when provided an X value, it will return
        the value of the function.
    gaussian_parameters : dictionary
        A compiled dictionary of all of the parameters of the Gaussian fit.
    """

    # Be able to accept both masked arrays and standard arrays and be able 
    # to tell.
    if (np_ma.is_masked(data_array)):
        flat_data = data_array.compressed()
    else:
        flat_data = data_array.flatten()

    # For consistent measurements have a lot of bins throughout the values.
    # But, bins of width 1 are too many and take a lot of time to make. 
    # Extracting function temporarily.
    from IfA_Smeargle.oscar.oscar_functions import oscar_bin_width
    hist_bins = oscar_bin_width(flat_data, 100)
    del oscar_bin_width

    # Extract histogram data from the data.
    hist_data = np.histogram(flat_data, bins=hist_bins)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]

    # Filter out some of the outlier pixels, consider only 75% of the 
    # meaningful bins and the bins with a value greater than a limiting entry.
    valuecut_index = np.where(hist_y >= 10)
    cuthist_x = np.array(hist_x[valuecut_index])
    cuthist_y = np.array(hist_y[valuecut_index])

    sorted_index = np.argsort(cuthist_y)
    cut_index = sorted_index[-np.floor(len(sorted_index)*0.75).astype(int):]
    cuthist_x = np.array(cuthist_x[cut_index])
    cuthist_y = np.array(cuthist_y[cut_index])

    # Initial guesses...
    # The peak of the data is a good guess for the mean value.
    guess_mean = hist_x[np.argmax(cuthist_y)]
    # Reverse calculating from FWHM estimates based on the most prominent
    # peak found. Using the FWHM number conversion. Do not use cuthist_y.
    peak_index, __ = sp_sig.find_peaks(hist_y, width=3)
    fwhm_esti = sp_sig.peak_widths(hist_y, peak_index, rel_height=0.5)
    print(fwhm_esti)
    fwhm_esti = np.array(fwhm_esti).max()
    guess_stddev = fwhm_esti / 2.35482

    # Do the Gaussian fit.
    inital_guesses = {'mean': guess_mean,
                      'stddev': guess_stddev,
                      'amplitude':1}
    gaussian_function, gaussian_parameters = smeargle_fit_gaussian_function(cuthist_x, cuthist_y, 
                                                                            inital_guesses)

    return gaussian_function, gaussian_parameters


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