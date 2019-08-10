"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 300; this file only contains ECHO-300 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn

from IfA_Smeargle import echo
from IfA_Smeargle.echo import echo_functions as echo_funct
from IfA_Smeargle.echo import masks
from IfA_Smeargle.meta import *


def echo380_single_pixels(data_array, pixel_list, previous_mask={}, return_mask=False):
    """ This applies a single mask on a single pixel(s)

    As the name implies, this function masks a single pixel value or a list of single pixel       
    pairs. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.
    pixel_list : array-like, ndarray
        This is a list/array of pixel pair (x,y) values. The function loops and applies the
        mask to each pair.
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
        the mask dictionary under the key ``echo380single_pixels``.

    """

    # Input validation.
    if ((len(pixel_list.shape) != 2) and (pixel_list.shape[1] != 2)):
        raise ValueError("The pixel list must be a list (x,y) point pairs.")
    
    # Taking a template mask to then change.
    masked_array = masks.echo398_nothing(data_array, return_mask=True)

    # Looping over all pairs.
    for pixeldex in pixel_list:
        xpix, ypix = pixeldex
        masked_array[ypix,xpix] = True


    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                      'echo380_single_pixels',return_mask)

    return final_mask


def echo381_rectangle_mask(data_array, x_ranges, y_ranges, previous_mask={}, return_mask=False):
    """ This mask function applies rectangular masks to the data array.

    The rectangles defined by subsequent xy-ranges (0-indexed) are masked. Multiple overlapping
    rectangles may be defined and masked using this function. The rectangle bounds provided are
    also masked as the rectangle is inclusive of said bounds. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    x_ranges : list or ndarray
        The list of 0-indexed x_ranges to be masked. Must be the same length as y_ranges.
    y_ranges : list or ndarray
        The list of 0-indexed y_ranges to be masked. Must be the same length as x_ranges.
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
        the mask dictionary under the key ``echo381_rectangle_mask``.
    """

    # Validating the input.
    x_ranges = np.array(x_ranges)
    y_ranges = np.array(y_ranges)

    if (x_ranges.shape != y_ranges.shape):
        raise InputError("The x-range and y-range lists are not the same shape.")
    if (len(x_ranges.shape) == 0):
        raise InputError("You gave me nothing, the x-range and y-range is empty.")
    elif (len(x_ranges.shape) == 1):
        # Test to see if it is a single rectangle.
        if (x_ranges.size == 2):
            # It seems to be a single rectangle, embed one dimension further.
            x_ranges = np.array([x_ranges])
            y_ranges = np.array([y_ranges])
        else:
            raise InputError("The x-range and y-range is not the correct shape.")
    elif (len(x_ranges.shape) == 2):
        # Assume they know what they are doing?
        pass
    else:
        raise InputError("The x-range and y-range has too many dimensions to parse logically.")

    # Extract a blank mask as a template.
    masked_array = masks.echo398_nothing(data_array, return_mask=True)

    # Mask rectangles.
    for xrangedex,yrangedex in zip(x_ranges,y_ranges):
        # The +1 is needed for inclusive ranges which is the conceptual
        # default.
        masked_array[yrangedex[0]:yrangedex[-1] + 1,xrangedex[0]:xrangedex[-1] + 1] = True

    # And returning.
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                      'echo381_rectangle_mask',return_mask)

    return final_mask


def echo382_column_mask(data_array, column_list, previous_mask={}, return_mask=False):
    """ This applies a column mask on the data array provided its locations.

    The column mask takes a list of column numbers (0-indexed x-axis values). All pixels within
    these columns are then masked. 


    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    column_list : list or ndarray
        The list of column x-axis values that will be masked. Should be 0-indexed.
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
        the mask dictionary under the key ``echo382_column_mask``.
    """

    # Extract a blank mask as a template.
    masked_array = masks.echo398_nothing(data_array, return_mask=True)

    # Masking the columns
    for columndex in column_list:
        masked_array[:,columndex] = True

    # And returning.
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                      'echo382_column_mask',return_mask)

    return final_mask


def echo383_row_mask(data_array, row_list, previous_mask={}, return_mask=False):
    """ This applies a row mask on the data array provided its locations.

    The row mask takes a list of column numbers (0-indexed x-axis values). All pixels within
    these rows are then masked. 


    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    row_list : list or ndarray
        The list of row y-axis values that will be masked. Should be 0-indexed.
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
        the mask dictionary under the key ``echo383_row_mask``.
    """

    # Extract a blank mask as a template.
    masked_array = masks.echo398_nothing(data_array, return_mask=True)

    # Masking the rows
    for rowdex in row_list:
        masked_array[rowdex,:] = True

    # And returning.
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                      'echo383_row_mask',return_mask)

    return final_mask


def echo398_nothing(data_array, previous_mask={}, return_mask=False):
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

    # Warnings are printed when a filter returns zero masked pixels, this 
    # is actually intended for this mask, ignore the filter.
    with smeargle_silence_specific_warnings(MaskingWarning):
        final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                          'echo398_nothing',return_mask)

    return final_mask


def echo399_everything(data_array, previous_mask={}, return_mask=False):
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

    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                      'echo399_everything',return_mask)

    return final_mask