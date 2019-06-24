
"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 100; this file only contains ECHO-100 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn

from ..meta import *

from . import echo_functions as echo_funct
from . import masks_echo000, masks_echo200, masks_echo300 as masks


def echo120_subarray_mask(data_array, x_range, y_range, previous_mask={}, return_mask=False):
    """ This applies a mask on the entire array except for a single sub-array rectangle. 

    This function subsets a sub-array of the data array from a mask. Only one sub-array can be
    defined using this function. The bounds of the sub-array is inclusively defined by the 
    x-ranges and y-ranges.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    x_range : list or ndarray
        The inclusive x-range bounds of the sub-array.
    y_range : list or ndarray
        The inclusive y-range bounds of the sub-array.
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
        the mask dictionary under the key ``echo120_subarray_mask``.
    """

    # A sub-array mask is practically the opposite of a rectangle mask. As such will be the 
    # implementation of it.
    masked_array = masks.echo381_rectangle_mask(data_array,[x_range],[y_range],return_mask=True)
    masked_array = np.logical_not(masked_array)

    # Returning the mask.
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                     'echo120_subarray_mask',return_mask)
    
    return final_mask