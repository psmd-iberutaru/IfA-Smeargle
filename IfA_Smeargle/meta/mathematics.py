"""
Sometimes the math needs to be explicit.
"""


import numpy as np
import numpy.ma  as np_ma

from IfA_Smeargle.meta import *

def smeargle_mean(array, axis=None):
    """ This returns the true mean of the data. It only counts valid data.

    There are outstanding problems with how the masked arrays handle means. 
    For some reason, there is no np.ma.nanmean function. This adds that 
    functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the mean will be taken from.
    axis : int 
        The axis that the mean will be taken over.

    Returns
    -------
    true_mean : float or ndarray
        The mean of the array along which ever axis was given. 
    """

    # Fix all invalid data before taking the mean.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise DataError("The array still contains invalid nan data after the invalid data was "
                        "fixed. The true mean function will not work as expected.")
    if (np.any(np.isinf(valid_array))):
        raise DataError("The array still contains invalid inf data after the invalid data was "
                        "fixed. The true mean function will not work as expected.")

    # Calculate and return the mean. The masked array version of the 
    # functions seems to properly ignore masks as intended.
    true_mean = np_ma.mean(array, axis=axis)

    return true_mean

def smeargle_median(array, axis=None):
    """ This returns the true median of the data. It only counts valid data.

    There are outstanding problems with how the masked arrays handle medians. 
    For some reason, there is no np.ma.nanmedian function. This adds that 
    functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the median will be taken from.
    axis : int 
        The axis that the median will be taken over.

    Returns
    -------
    true_median : float or ndarray
        The median of the array along which ever axis was given. 
    """

    # Fix all invalid data before taking the median.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise DataError("The array still contains invalid nan data after the invalid data was "
                        "fixed. The true median function will not work as expected.")
    if (np.any(np.isinf(valid_array))):
        raise DataError("The array still contains invalid inf data after the invalid data was "
                        "fixed. The true median function will not work as expected.")

    # Calculate and return the median. The masked array version of the 
    # functions seems to properly ignore masks as intended.
    true_median = np_ma.median(array, axis=axis)

    return true_median

def smeargle_std(array, axis=None):
    """ This returns the true standard deviation of the data. It only counts 
    valid data.

    There are outstanding problems with how the masked arrays handle stds. 
    For some reason, there is no np.ma.nanstd function. This adds that 
    functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the standard deviation will be 
        taken from.
    axis : int 
        The axis that the median will be taken over.

    Returns
    -------
    true_std : float or ndarray
        The standard deviation of the array along which ever axis was given. 
    """

    # Fix all invalid data before taking the median.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise DataError("The array still contains invalid nan data after the invalid data was "
                        "fixed. The true std function will not work as expected.")
    if (np.any(np.isinf(valid_array))):
        raise DataError("The array still contains invalid inf data after the invalid data was "
                        "fixed. The true std function will not work as expected.")

    # Calculate and return the standard deviation. The masked array version 
    # of the functions seems to properly ignore masks as intended.
    true_std = np_ma.std(array, axis=axis)

    return true_std