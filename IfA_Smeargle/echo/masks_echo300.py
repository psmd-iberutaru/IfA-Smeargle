"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 300; this file only contains ECHO-300 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn


def echo_380_single_pixels(data_array, previous_mask={}, return_mask=False,
                           pixel_list=None):
    """ This applies a single mask on a single pixel(s)

    As the name implies, this function masks a single pixel value or a list of single pixel
    pairs. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be added to the 
        dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary entry) will be 
        returned instead.
    pixel_list : array-like, ndarray
        This is a list/array of pixel pair (x,y) values. The function loops and applies the
        mask to each pair.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False) will be added to 
        the mask dictionary under the key ``echo380_single_pixels``.

    """

    # Input validation.
    if (pixel_list is None):
        raise ValueError("The pixel list must actually be provided.")
    if ((len(pixel_list.shape) != 2 ) and (pixel_list.shape[1] != 2)):
        raise ValueError("The pixel list must be a list (x,y) point pairs.")
    
    # Taking a template mask to then change.
    masked_array = echo_398_nothing(data_array, return_mask=True)

    # Looping over all pairs.
    for pixeldex in pixel_list:
        xpix, ypix = pixeldex
        masked_array[ypix,xpix] = True


    previous_mask['echo380_single_pixels'] = masked_array

    if (return_mask):
        final_mask = masked_array
    elif (not return_mask):
        final_mask = previous_mask
    else:
        final_mask = previous_mask

    return final_mask




def echo_398_nothing(data_array, previous_mask={}, return_mask=False):
    """ This applies a blanket blank (all pixels are valid) mask on the data array.

    As the name says, this applies a mask...to...well...nothing. As such, all that is 
    returned in the mask dictionary is the blank mask.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be added to the 
        dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary entry) will be 
        returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False) will be added to 
        the mask dictionary under the key ``echo398_nothing``.
    """

    array_shape = data_array.shape
    masked_array = np.full(array_shape, False)

    previous_mask['echo398_nothing'] = masked_array

    if (return_mask):
        final_mask = masked_array
    elif (not return_mask):
        final_mask = previous_mask
    else:
        final_mask = previous_mask

    return final_mask


def echo_399_everything(data_array, previous_mask={}, return_mask=False):
    """ This applies a blanket blank (all pixels are invalid) mask on the data array.

    As the name says, this applies a mask...to...well...everything. As such, all that is 
    returned in the mask dictionary is the full mask.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be added to the 
        dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary entry) will be 
        returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False) will be added to 
        the mask dictionary under the key ``echo399_everything``.
    """

    array_shape = data_array.shape
    masked_array = np.full(array_shape, True)

    previous_mask['echo399_everything'] = masked_array

    if (return_mask):
        final_mask = masked_array
    elif (not return_mask):
        final_mask = previous_mask
    else:
        final_mask = previous_mask

    return final_mask