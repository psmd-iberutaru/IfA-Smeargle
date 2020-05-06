"""
This module contains functions that are strictly the backbone of many
of the modeling and fitting functionality.
"""

import astropy as ap
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma

import IfA_Smeargle.core as core

def fit_gaussian_function(x_data, y_data, inital_guesses):
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
        Initial guesses for the Gaussian fitting function. The allowed 
        inputs and their keys are:

            * 'mean' : The inital guess of the gaussian function's mean. 
                       Defaults to 0.
            * 'stddev' : The inital guess of the gaussian function's standard  
                         deviation. Defaults to 1.
            * 'amplitude' : The intial guess of the gaussian function's 
                            amplitude. Defaults to 1.
    Returns
    -------
    gaussian_function : function
        A callable function that when provided an X value, it will return
        the value of the function.
    gaussian_parameters : dictionary
        A compiled dictionary of all of the parameters of the Gaussian fit.
    """

    # Extract the initial guesses.
    inital_guesses = dict(inital_guesses)
    guess_mean = inital_guesses.get('mean', 0)
    guess_stddev = inital_guesses.get('stddev', 1)
    guess_amplitude = inital_guesses.get('amplitude', 1)

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
    temp_gauss_x_axis = np.linspace(np.nanmin(x_data) - 1, np.nanmax(x_data) + 1, 
                                    x_data.size * 100)
    gaussian_max = np.max(gaussian_fit(temp_gauss_x_axis))
    gaussian_parameters = {'mean':gaussian_mean, 'stddev':gaussian_stddev,
                           'amplitude':gaussian_amplitude, 'max':gaussian_max}

    # The Gaussian function
    gaussian_function = lambda input: gaussian_fit(np.array(input))

    return gaussian_function, gaussian_parameters


def fit_histogram_gaussian_function(data_array, bin_width):
    """ This function fits a Gaussian function to a specific set of data.

    Gaussian fitting is hard, this function exists as a port so that 
    all fitting functions use the same algorithm and said algorithm is easy
    to change. This applies it to the histogram of the data.
    
    Parameters
    ----------
    data_array : ndarray
        The data that the histogram Gaussian function is fitting.
    bin_width : float
        The width of the bins to use for the histogram fitting function.

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

    # Numpy does not support histogram bin widths, instead using bins defined
    # by values in an array. Converting equal bin widths to this array.
    hist_bins = core.math.generate_numpy_bin_width_array(data_array=flat_data, 
                                                         bin_width=bin_width)

    # Extract histogram data from the data.
    hist_data = np.histogram(flat_data, bins=hist_bins)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]

    # Determine the inital guesses of the gaussian histogram fit. So far 
    # magic is the best way.
    guess_mean, guess_stddev, guess_amplitude = \
        core.magic.magic_inital_gaussian_parameters(x_data=hist_x, 
                                                    y_data=hist_y)

    # Do the Gaussian fit.
    inital_guesses = {'mean': guess_mean,
                      'stddev': guess_stddev,
                      'amplitude': guess_amplitude}
    gauss_funct, gauss_param = fit_gaussian_function(hist_x, hist_y,
                                                     inital_guesses)
    # For naming convention.
    gaussian_function = gauss_funct
    gaussian_parameters = gauss_param
    return gaussian_function, gaussian_parameters