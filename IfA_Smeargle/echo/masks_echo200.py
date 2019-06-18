"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 200; this file only contains ECHO-200 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn

from . import echo_main
from . import masks_echo000, masks_echo100, masks_echo300 as masks


def echo_270_minimum_cut(data_array, minimum_value, previous_mask={}, return_mask=False):
    """ This applies a mask on all pixels lower than some value.

    As the name implies, this function masks all pixels with some value strictly lower than
    some minimum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    minimum_value : float
        The minimum value that the filter references.
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
        the mask dictionary under the key ``echo270_minimum_cut``.
    """

    masked_array = np.where(data_array < minimum_value, True, False)

    final_mask = echo_main.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo270_minimum_cut', return_mask)

    return final_mask


def echo_271_maximum_cut(data_array, maximum_value, previous_mask={}, return_mask=False):
    """ This applies a mask on all pixels lower than some value.

    As the name implies, this function masks all pixels with some value strictly higher than
    some maximum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    maximum_value : float
        The maximum value that the filter references.
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
        the mask dictionary under the key ``echo271_maximum_cut``.
    """

    masked_array = np.where(data_array > maximum_value, True, False)

    final_mask = echo_main.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo271_maximum_cut', return_mask)

    return final_mask