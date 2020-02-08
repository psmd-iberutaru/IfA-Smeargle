
"""
This file contains functions dealing with the loading and handling of fits files and their 
associated header and data arrays.
"""

import astropy as ap
import astropy.io.fits as ap_fits
import copy
import inspect
import numpy as np
import numpy.ma as np_ma
import os
import warnings as warn

from IfA_Smeargle.meta import *


def smeargle_extract_subarray(primary_array,x_bounds,y_bounds):
    """ A function to extract a smaller array copy from a larger array.

    Sub-arrays are rather important in the analysis of specific arrays. 
    This function extracts a sub-array from a given primary array specified 
    by the x_bounds and y_bounds.

    Parameters
    ----------
    primary_array : ndarray
        This is the data array that is desired to be sliced.
    x_bounds : list-like
        The bounds of the x-axis of a given array. 
    y_bounds : list-like
        The bounds of the y-axis of a given array.

    Returns
    -------
    sub_array : ndarray
        An array containing only data within the xy-bounds provided.
    
    """

    # Be verbose in accepting reversed (but valid) bounds.
    x_bounds = np.sort(x_bounds)
    y_bounds = np.sort(y_bounds)

    sub_array = primary_array[y_bounds[0]:y_bounds[-1],x_bounds[0]:x_bounds[1]]

    raise DeprecationError

    return np.array(sub_array)


def smeargle_masked_array_min_max(masked_array):
    """ This function returns a masked array's minimum and maximum value.

    This function determines the minimum and maximum of a masked arrays 
    between valid, unmasked, values only. Masked values are not considered 
    for min-max evaluation.
    
    Parameters
    ----------
    masked_array : masked ndarray 
        The array that has a mask, and is also the one that will have a 
        min max calculated.

    Returns
    -------
    masked_min : float
        The value of the minimum of the masked array ignoring masking.
    masked_max : float
        The value of the maximum of the masked array ignoring masking.
    """
    
    # Sparrow was wrong when coding the function that required this function.
    # It has scene been reduced to the logical answer and is thus depreciated. 
    smeargle_warning(DeprecatedWarning,("This function was built because of the erroneous "
                                          "understanding that it was difficult to get min-max "
                                          "from Numpy Masked Arrays. This function is a "
                                          "wrapper around the easy and proper method."))

    # Execute a copy just in case of damage to the array.
    masked_array = copy.deepcopy(masked_array)

    # Finding the minimum of the array.
    masked_min = np.nanmin(masked_array)

    # Finding the maximum of the array
    masked_max = np.nanmax(masked_array)

    raise DeprecationError

    return masked_min, masked_max


def smeargle_remake_array(array, new_array_type):
    """  This function is built to remake an array into any array type.
    
    Having to deal with both masked arrays and normal arrays, and mixing the
    two up, is not optimal. This function makes the desired array type,
    switching as needed.

    Parameters
    ----------
    array : array-like
        The "array" that will be turned into the proper format.
    new_array_type
        The new array type. It must be supported by this function.

    Returns
    -------
    new_array : "new_array_type"
        The final array in the specified type.
    """
    raise DeprecationError

    if (not inspect.isclass(new_array_type)):
        raise InputError("The new array type must be a class.")

    try:
        # Determine the desired form and convert based on it.
        if (new_array_type is np.ndarray):
            return np.array(array)
        elif (new_array_type is np_ma.masked_array):
            return np_ma.array(data=np.array(array), mask=np_ma.getmask(array))
        else:
            # The type provided doesn't seem to be a supported type. 
            raise InputError("The new array type provided is not supported. ")
    except InputError:
        raise
    except Exception:
        raise TypeError("The conversion cannot take place. The two types <{type1}> and <type2> "
                        "seem to be incompatible."
                        .format(type1=type(array),type2=new_array_type))