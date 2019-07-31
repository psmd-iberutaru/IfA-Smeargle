
"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 100; this file only contains ECHO-100 class masks.
"""

import astropy as ap
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma
import scipy as sp
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

    # A sub-array mask is practically the opposite of a rectangle mask. As such will be the 
    # implementation of it.
    masked_array = masks.echo381_rectangle_mask(data_array,x_range,y_range,return_mask=True)
    masked_array = np.logical_not(masked_array)

    # Returning the mask.
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                     'echo120_subarray_mask',return_mask)
    
    return final_mask


def echo170_gaussian_truncation(data_array, sigma_multiple, previous_mask={}, return_mask=False):
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

    # Be able to accept both masked arrays and standard arrays and be able 
    # to tell.
    if (np_ma.is_masked(data_array)):
        flat_data = data_array.compressed()
    else:
        flat_data = data_array.flatten()

    # For consistent measurements have a lot of bins throughout the values.
    # But, bins of width 1 are too many and take a lot of time to make. 
    hist_bins = oscar.oscar_bin_width(flat_data, 42)

    # Extract histogram data from the data.
    hist_data = np.histogram(flat_data, bins=hist_bins)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]

    # Filter out some of the outlier pixels, consider only 75% of the 
    # meaningful bins and the bins with a value greater than a limiting entry.
    valuecut_index = np.where(hist_y >= 5)
    hist_x = np.array(hist_x[valuecut_index])
    hist_y = np.array(hist_y[valuecut_index])

    sorted_index = np.argsort(hist_y)
    cut_index = sorted_index[-np.floor(len(sorted_index)*0.75).astype(int):]
    hist_x = np.array(hist_x[cut_index])
    hist_y = np.array(hist_y[cut_index])


    # Fitting the Gaussian function.  For some reasons beyond 
    # what Sparrow can explain, Astropy seems to have better fitting 
    # capabilities, in this specific application, than Scipy.
    gaussian_init = ap_mod.models.Gaussian1D(amplitude=1.0, mean=0, stddev=1.0)
    gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
    gaussian_fit = gaussian_fit_model(gaussian_init, hist_x, hist_y)

    # Basic Gaussian information.
    mean = gaussian_fit.mean.value
    stddev = gaussian_fit.stddev.value

#    # Check if the Gaussian fit did anything useful.
#    if ((int(mean) == 0) or (int(stddev) == 1)):
#        smeargle_warning(MaskingWarning,("The Gaussian fit is remarkably close to the initial "
#                                         "conditions. It is highly likely that the Gaussian "
#                                         "fit silently failed. "))
    print(mean,stddev)

    # Compute which pixels to be masked out. 
    with warn.catch_warnings():
        warn.simplefilter("ignore", MaskingWarning)
        temp_mask_dict = {}
        temp_mask_dict = masks.echo270_minimum_cut(data_array, 
                                                   (mean - sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        temp_mask_dict = masks.echo271_maximum_cut(data_array, 
                                                   (mean + sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        # Synthesize the top and bottom masks.
        masked_array = echo_funct.synthesize_mask_dictionary(temp_mask_dict)

    # Finally return
    final_mask = echo_funct.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo277_sigma_truncation', return_mask)

    return final_mask