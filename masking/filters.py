
"""
This contains all of the value based filters when doing analysis.
"""
import numpy as np
import numpy.ma as np_ma

import IfA_Smeargle.core as core
import IfA_Smeargle.masking as mask

"""
[value]
    gaussian_sigma_value = float
    gaussian_bin_width = float
    sigma_sigma_value = float
    top_percent = float(min=0, max=1)
    bottom_percent = float(min=0, max=1)
    top_count = integer
    bottom_count = integer
    minimum_value = float
    maximum_value = float
    exact_value = float
"""

def filter_sigma_value(data_array, sigma_multiple):
    """
    This applies a mask on pixels outside a given multiple of a sigma 
    value.
    
    This function masks values if they are outsize of a sigma range 
    from the mean. The mean and sigma values are automatically 
    calculated from the array provided. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    sigma_multiple : float or array-like
        The multiple of sigma which will be applied. Unequal 
        bottom-top bounds may be set as a list-like input. The 
        first element is the bottom bound; the last element is the 
        top bound.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """

    # Check if the sigma limits are the same, or the user 
    # provided for a lower and upper sigma to use.
    if (isinstance(sigma_multiple,(int,float))):
        # It is just a number, apply them evenly.
        bottom_sigma_multiple = sigma_multiple
        top_sigma_multiple = sigma_multiple
    elif (np.array(sigma_multiple).size == 1):
        # It is likely that this is a single number, but just 
        # embedded,
        flat_sigma_multiple = np.squeeze(np.array(sigma_multiple))
        bottom_sigma_multiple = flat_sigma_multiple
        top_sigma_multiple = flat_sigma_multiple
    else:
        # The sigma multiple is most likely some sort of array for 
        # uneven values.
        flat_sigma_multiple = np.squeeze(np.array(sigma_multiple))
        bottom_sigma_multiple = flat_sigma_multiple[0]
        top_sigma_multiple = flat_sigma_multiple[-1]

    # Calculate the mean and the sigma values of the data array.
    mean = core.math.ifas_masked_mean(data_array)
    stddev = core.math.ifas_masked_std(data_array)
        

    # Calculating the two individual filters and combining them.
    min_filter = filter_minimum_value(
        data_array=data_array, 
        minimum_value=(mean - stddev * bottom_sigma_multiple))
    max_filter = filter_maximum_value(
        data_array=data_array, 
        maximum_value=(mean + stddev * top_sigma_multiple))
    
    # The mask based version is proper, the difference between a 
    # mask and a filter is just semantics.
    final_filter = mask.base.synthesize_masks(min_filter, max_filter)

    return final_filter

def filter_percent_truncation(data_array, top_percent, bottom_percent):
    """ This filter truncates the top and bottom percent of pixels 
    provided.

    The values ``top_percent`` and ``bottom_percent`` notate the 
    percentage of pixels from top and bottom of the data array 
    (in value) that should be filtered. The pixels masked are 
    independent on the previous masks applied.

    Parameters
    ----------
    data_array : ndarray
        The data array that the filter will be calculated from. 
    top_count : float
        The percent of pixels from the top (highest value) of 
        the array that is to be masked.
    bottom_count : int
        The percent of pixels from the bottom (lowest value) of 
        the array that is to be masked.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """
    # For higher precision.
    top_percent = np.longdouble(top_percent)
    bottom_percent = np.longdouble(bottom_percent)
    ONE = np.longdouble(1.0)

    # A percent truncation is a fancy pixel truncation, and is 
    # going to be  applied as such. 
    total_n_pixels = np.longdouble(data_array.size)
    top_pixel = int(np.ceil(total_n_pixels * (ONE - top_percent)))
    bottom_pixel = int(np.floor(total_n_pixels * bottom_percent))

    # The pixel mask
    final_filter = filter_pixel_truncation(data_array=data_array, 
                                         top_count=top_pixel, 
                                         bottom_count=bottom_pixel)

    # The above method requires that the total number of pixels is not
    # comparable to the float resolution. If not, then lower bound values 
    # will be improperly cut and percentages will not be accurately 
    # calculated.
    if (np.log10(total_n_pixels) 
        > (- np.log10(np.finfo(np.longdouble).resolution) - 5)):
        core.error.ifas_warning(core.error.ImprecisionWarning,
                                ("Float multiplication is used to calculate "
                                 "truncations. The total number of pixels "
                                 "approaches the machine resolution for "
                                 "multiplication."))
    elif (np.log10(total_n_pixels) 
          > (- np.log10(np.finfo(np.longdouble).resolution))):
        core.error.ifas_error(core.error.ImprecisionError,
                              ("Current number of pixels exceeds resolution "
                               "of float multiplication; percent truncation "
                               "may be wildly inaccurate."))
    # Finally return
    return final_filter

def filter_pixel_truncation(data_array, top_count, bottom_count):
    """ This filter truncates the top and bottom number of pixels 
    provided.

    The values ``top_count`` and ``bottom_count`` notate the number 
    of pixels from top and bottom of the data array (in value) that 
    should be cut. The pixels masked are independent on the 
    previous masks applied.

    Parameters
    ----------
    data_array : ndarray
        The data array that the filter will be calculated from. 
    top_count : int
        The number of pixels from the top (highest value) of the array 
        that is to be masked.
    bottom_count : int
        The number of pixels from the bottom (lowest value) of the array that 
        is to be masked.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """
    
    # Sort the data.
    sorted_data = np.sort(np_ma.getdata(data_array, subok=False), axis=None)

    
    # Find the values above and below the cuts, simplifying the process to 
    # pure value cuts.
    upper_value = sorted_data[:-top_count][-1]
    bottom_value = sorted_data[bottom_count:][0]

    # Calculating the two individual filters and combining them.
    max_filter = filter_maximum_value(data_array=data_array, 
                                      maximum_value=upper_value)
    min_filter = filter_minimum_value(data_array=data_array, 
                                      minimum_value=bottom_value)
    # The mask based version is proper, the difference between a 
    # mask and a filter is just semantics.
    final_filter = mask.base.synthesize_masks(min_filter, max_filter)

    return final_filter

def filter_maximum_value(data_array, maximum_value):
    """ This function computes a filter for all pixel values 
    strictly more than some maximum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the filter will be calculated from. 
    maximum_value : float
        The value that data values strictly more than will be 
        tagged as filtered.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """
    # Find which values are strictly less than.
    final_filter = np.where(data_array > float(maximum_value), True, False)

    # Done
    return final_filter

def filter_minimum_value(data_array, minimum_value):
    """ This function computes a filter for all pixel values 
    strictly less than some minimum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the filter will be calculated from. 
    minimum_value : float
        The value that data values strictly less than will be 
        tagged as filtered.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """
    # Find which values are strictly less than.
    final_filter = np.where(data_array < float(minimum_value), True, False)

    # Done
    return final_filter

def filter_exact_value(data_array, exact_value):
    """ This function computes a filter for all pixel values 
    equal to some exact value.

    Float equality comparisons are dependent on tolerances. The main
    back function used is `numpy.isclose`.

    Parameters
    ----------
    data_array : ndarray
        The data array that the filter will be calculated from. 
    exact_value : float
        The value that data values close will be tagged as filtered.

    Returns
    -------
    final_filter : ndarray
        The filter as computed by this function.
    """
    # Obtain the float equality tolerance from the configuration.
    float_tolerance = core.runtime.extract_runtime_configuration(
        config_key='FLOAT_EQUALITY_TOLERANCE')

    # For usage in the close comparison, a filled array.
    exact_value_array = np.full_like(data_array, exact_value)

    # Find which values are close.
    final_filter = np.isclose(data_array, exact_value_array)

    # Done
    return final_filter

