"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 000; this file only contains ECHO-000 class masks.
"""

import astropy as ap
import numpy as np
import numpy.ma  as np_ma
import scipy as sp
import warnings as warn

from . import echo_functions as echo_funct
from . import masks_echo100, masks_echo200, masks_echo300 as masks


def echo010_fixing_invalids(data_array, previous_mask={}, return_mask=False):
    """ This filter applies a mask to all numerically invalid inputs on a programing side.

    Numbers that are usually infinite or some other nonsensical quantity serve no real usage in
    calculations further downstream. Therefore, they are masked here.

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
        the mask dictionary under the key ``echo010_fixing_invalids``.

    """

    data_array = np.array(data_array)

    masked_array = np_ma.fix_invalid(data_array)

    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                     'echo010_fixing_invalids',return_mask)

    return final_mask