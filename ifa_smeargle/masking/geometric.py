"""
These are masks that are applied in a purely geometric method.
"""

import numpy as np

import ifa_smeargle.core as core
import ifa_smeargle.masking as mask

def mask_single_pixels(data_array, column_indexes, row_indexes):
    """ This applies a single mask on a single pixel(s)

    As the name implies, this function masks a single pixel value or 
    a list of single pixel pairs. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.
    column_indexes : list or ndarray
        The successive 0-indexed list of column indexes that specify 
        the pixel to be masked.
    row_indexes : list or ndarray
        The successive 0-indexed list of row indexes that specify the 
        pixel to be masked.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are 
        valid (False).

    """
    # Flatten the column and row indexes in the event that they are 
    # stacked?
    column_indexes = np.ravel(np.array(column_indexes, dtype=int))
    row_indexes = np.ravel(np.array(row_indexes, dtype=int))

    # Input validation. Both should be ordered pairs and thus have 
    # the same size.
    if (column_indexes.size != row_indexes.size):
        raise core.error.ConfigurationError("The column and row indexes "
                                            "should be parallel arrays, the "
                                            "current inputs are of "
                                            "different length. "
                                            "\n Column:  {col_index}  "
                                            "\n Row:  {row_index}"
                                            .format(col_index=column_indexes, 
                                                    row_index=row_indexes))
    
    # Taking a template mask to then change.
    masked_array = mask_nothing(data_array=data_array)

    # Loop over all of the pixel pairs, making as you proceed.
    for columndex, rowdex in zip(column_indexes, row_indexes):
        masked_array[rowdex, columndex] = True

    # Finished.
    final_mask = masked_array
    return final_mask

def mask_rectangle(data_array, column_range, row_range):
    """ This mask function applies rectangular masks to the data 
    array.

    The rectangles defined by subsequent xy-ranges (0-indexed) are 
    masked. The rectangle bounds provided are also masked as the 
    rectangle is inclusive of said bounds. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    column_range : list or ndarray
        The range of 0-indexed columns to be masked.
    row_range : list or ndarray
        The range of 0-indexed row to be masked.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """

    # Validating the input.
    column_range = np.array(column_range, dtype=int)
    row_range = np.array(row_range, dtype=int)

    # Check if the sizes of columns and rows are wrong.
    if (column_range.size > 2):
        core.error.ifas_warning(core.error.ConfigurationWarning,
                                ("There are more than two entries in the "
                                 "column range. Only the first and last "
                                 "entry will be considered as the bounds."))
    if (row_range.size > 2):
        core.error.ifas_warning(core.error.ConfigurationWarning,
                                ("There are more than two entries in the "
                                 "row range. Only the first and last entry "
                                 "will be considered as the bounds."))

    # Extract a blank mask as a template.
    masked_array = mask_nothing(data_array=data_array)

    # Mask rectangle inclusively.
    masked_array[row_range[0]:row_range[-1] + 1, 
                 column_range[0]:column_range[-1] + 1] = True

    # And returning.
    final_mask = masked_array

    return final_mask

def mask_subarray(data_array, column_range, row_range):
    """ This applies a mask on the entire array except for a single 
    sub-array rectangle. 

    This function subsets a sub-array of the data array from a 
    mask. Only one sub-array can be defined using this function. 
    The bounds of the sub-array is inclusively defined by the 
    x-ranges and y-ranges.

    If you want to mask a rectangular section of your array, use 
    `mask_rectangle`.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    column_range : list or ndarray
        The inclusive column bounds of the sub-array.
    row_range : list or ndarray
        The inclusive row bounds of the sub-array.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """
    # Data reformatting.
    column_range = np.array(column_range)
    row_range = np.array(row_range)

    # A sub-array mask is practically the opposite of a rectangle 
    # mask. As such will be the implementation of it.
    masked_array = mask_rectangle(data_array=data_array,
                                  column_range=column_range, 
                                  row_range=row_range)
    final_mask = np.logical_not(masked_array)    
    return final_mask

def mask_columns(data_array, column_list):
    """ This applies a column mask on the data array provided its 
    locations.

    The column mask takes a list of column numbers (0-indexed x-axis 
    values). All pixels within these columns are then masked. 


    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    column_list : list or ndarray
        The list of column x-axis values that will be masked. Should 
        be 0-indexed.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """

    # Extract a blank mask as a template.
    masked_array = mask_nothing(data_array=data_array)

    # Masking the columns
    for columndex in column_list:
        masked_array[:,columndex] = True

    # And returning.
    final_mask = masked_array
    return final_mask

def mask_rows(data_array, row_list):
    """ This applies a row mask on the data array provided its 
    locations.

    The row mask takes a list of column numbers (0-indexed x-axis 
    values). All pixels within these rows are then masked. 


    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    row_list : list or ndarray
        The list of row y-axis values that will be masked. Should be 
        0-indexed.

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """

    # Extract a blank mask as a template.
    masked_array = mask_nothing(data_array=data_array)

    # Masking the rows
    for rowdex in row_list:
        masked_array[rowdex,:] = True

    # And returning.
    final_mask = masked_array
    return final_mask

def mask_nothing(data_array):
    """ This applies a blanket blank (all pixels are valid) mask on 
    the data array.

    As the name says, this applies a mask...to...well...nothing. As 
    such, all that is returned is a blank mask.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """

    array_shape = data_array.shape
    final_mask = np.full(array_shape, False, dtype=bool)

    return final_mask

def mask_everything(data_array):
    """ This applies a blanket blank (all pixels are valid) mask on 
    the data array.

    As the name says, this applies a mask...to...well...everything. 
    As such, all that is returned is a full mask.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 

    Returns
    -------
    final_mask : ndarray
        A boolean array for pixels that are masked (True) or are 
        valid (False).
    """

    array_shape = data_array.shape
    final_mask = np.full(array_shape, True, dtype=bool)

    return final_mask












