
"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 100; this file only contains ECHO-100 class masks.
"""

import astropy as ap
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma
import scipy as sp
import matplotlib.pyplot as plt
import warnings as warn

from IfA_Smeargle import echo
from IfA_Smeargle.echo import echo_functions as echo_funct
from IfA_Smeargle.echo import masks
from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar


def echo120_subarray_mask(data_array, x_range, y_range, previous_mask={}, return_mask=False):
    """ This applies a mask on the entire array except for a single sub-array 
    rectangle. 

    This function subsets a sub-array of the data array from a mask. Only one 
    sub-array can be defined using this function. The bounds of the sub-array 
    is inclusively defined by the x-ranges and y-ranges.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    x_range : list or ndarray
        The inclusive x-range bounds of the sub-array.
    y_range : list or ndarray
        The inclusive y-range bounds of the sub-array.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be 
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary 
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid 
        (False) will be added to the mask dictionary under the 
        key ``echo120_subarray_mask``.
    """
    # Data validation.
    x_range = np.array(x_range)
    y_range = np.array(y_range)

    # A sub-array mask is practically the opposite of a rectangle mask. As 
    # such will be the implementation of it.
    masked_array = masks.echo381_rectangle_mask(data_array,x_range,y_range,return_mask=True)
    masked_array = np.logical_not(masked_array)

    # Returning the mask.
    final_mask = echo_funct.echo_functioned_mask_returning(masked_array,previous_mask,
                                                     'echo120_subarray_mask',return_mask)
    
    return final_mask


def echo170_gaussian_truncation(data_array, sigma_multiple, bin_size, 
                                previous_mask={}, return_mask=False):
    """ This applies a mask on pixel values outside some Gaussian profile.

    This function is similar to echo277_sigma_truncation, but instead the
    mean and standard deviation are calculating using histogram methods 
    rather than absolute analysis. Because of the dependence on fits, this 
    method may be unstable.
    
    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    sigma_multiple : float
        The multiple of sigma from the mean that will be allowed; all else are
        masked.
    bin_size : float
        The size of the bins to use for the histogram fitting.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be 
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary 
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid 
        (False) will be added to the mask dictionary under the 
        key ``echo170_gaussian_truncation``.
    """


    # Fitting the Gaussian function. 
    __, gauss_param = meta_model.smeargle_fit_histogram_gaussian_function(data_array, 
                                                                          bin_width=bin_size)   

    # Basic Gaussian information.
    mean = gauss_param['mean']
    stddev = gauss_param['stddev']

    # Compute which pixels to be masked out. 
    with smeargle_silence_ifas_warnings():

        temp_mask_dict = {}
        temp_mask_dict = masks.echo270_minimum_cut(data_array, 
                                                   (mean - sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        temp_mask_dict = masks.echo271_maximum_cut(data_array, 
                                                   (mean + sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        # Synthesize the top and bottom masks.
        masked_array = echo_funct.echo_synthesize_mask_dictionary(temp_mask_dict)

    # Finally return
    final_mask = echo_funct.echo_functioned_mask_returning(masked_array, previous_mask,
                                                     'echo170_gaussian_truncation', return_mask)

    return final_mask