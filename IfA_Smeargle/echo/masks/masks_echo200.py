"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 200; this file only contains ECHO-200 class masks.
"""

import astropy as ap
import numpy as np
import numpy.ma as np_ma
import scipy as sp
import warnings as warn

from IfA_Smeargle import echo
from IfA_Smeargle.echo import echo_functions as echo_funct
from IfA_Smeargle.echo import masks
from IfA_Smeargle.meta import *

def echo270_minimum_cut(data_array, minimum_value, previous_mask={}, return_mask=False):
    """ This applies a mask on all pixels lower than some value.

    As the name implies, this function masks all pixels with some value 
    strictly lower than some minimum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    minimum_value : float
        The minimum value that the filter references.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be  
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary  
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False)  
        will be added to the mask dictionary under the key 
        ``echo270_minimum_cut``.
    """

    masked_array = np.where(data_array < minimum_value, True, False)

    final_mask = echo_funct.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo270_minimum_cut', return_mask)

    return final_mask


def echo271_maximum_cut(data_array, maximum_value, previous_mask={}, return_mask=False):
    """ This applies a mask on all pixels lower than some value.

    As the name implies, this function masks all pixels with some value 
    strictly higher than some maximum value.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    maximum_value : float
        The maximum value that the filter references.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be  
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary  
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False)  
        will be added to the mask dictionary under the key 
        ``echo271_maximum_cut``.
    """

    masked_array = np.where(data_array > maximum_value, True, False)

    final_mask = echo_funct.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo271_maximum_cut', return_mask)

    return final_mask


def echo275_pixel_truncation(data_array, top_count, bottom_count, 
                             previous_mask={}, return_mask=False):
    """ This filter truncates the top and bottom number of pixels provided.

    The values ``top_count`` and ``bottom_count`` notate the number of pixels 
    from top and bottom of the data array  (in value) that should be cut. 
    The pixels masked are independent on the previous masks applied.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    top_count : int
        The number of pixels from the top (highest value ) of the array 
        that is to be masked.
    bottom_count : int
        The number of pixels from the bottom (lowest value) of the array that 
        is to be masked.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be 
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary  
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False)  
        will be added to the mask dictionary under the key 
        ``echo275_pixel_truncation``.
    """
    
    # Sort the data.
    sorted_data = np.sort(np_ma.getdata(data_array, subok=False), axis=None)

    
    # Find the values above and below the cuts, simplifying the process to 
    # pure value cuts.
    upper_value = sorted_data[:-top_count][-1]
    bottom_value = sorted_data[bottom_count:][0]

    temp_mask_dict = {}
    temp_mask_dict = masks.echo270_minimum_cut(data_array, bottom_value, 
                                               previous_mask=temp_mask_dict)
    temp_mask_dict = masks.echo271_maximum_cut(data_array, upper_value, 
                                               previous_mask=temp_mask_dict)

    masked_array = echo_funct.synthesize_mask_dictionary(temp_mask_dict)

    # Finally return
    final_mask = echo_funct.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo275_pixel_truncation', return_mask)

    return final_mask


def echo276_percent_truncation(data_array, kept_range, previous_mask={}, return_mask=False):
    """ This filter truncates the top and bottom percent of pixels from the 
    data array.

    The parameter ``kept_range`` define the percent range of pixels that will 
    be kept. Anything outside this percentage range is masked. The pixels 
    the previous masked are independent of masks provided.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    kept_range : ndarray or array-like
        This is the percentage span that will be kept, the rest will be 
        masked. Percentages are expected to be less than 1.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be  
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary  
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False)  
        will be added to the mask dictionary under the key 
        ``echo276_percent_truncation``.
    """
    data_array = np.array(data_array)
    kept_range = np.array(kept_range, dtype=np.longdouble)

    # A percent truncation is a fancy pixel truncation, and is going to be 
    # applied as such. 
    total_n_pixels = data_array.size
    top_pixel = int(np.ceil(total_n_pixels * (1.0 - kept_range[-1])))
    bottom_pixel = int(np.floor(total_n_pixels * kept_range[0]))

    masked_array = masks.echo275_pixel_truncation(data_array, top_pixel, bottom_pixel, 
                                                 return_mask=True)

    # The above method requires that the total number of pixels is not
    # comparable to the float resolution. If not, then lower bound values 
    # will be improperly cut and percentages will not be accurately 
    # calculated.
    if (np.log10(total_n_pixels) > (- np.log10(np.finfo(np.longdouble).resolution) - 5)):
        smeargle_warning(ImprecisionWarning,
                         ("Float multiplication is used to calculate truncations. The total "
                          "number of pixels approaches the machine resolution for "
                          "multiplication."))
    elif (np.log10(total_n_pixels) > (- np.log10(np.finfo(np.longdouble).resolution))):
        raise ImprecisionError(("Current number of pixels exceeds resolution of float "
                                "multiplication; percent truncation will be wildly inaccurate."))

    # Otherwise... return
    final_mask = echo_funct.functioned_mask_returning(masked_array,previous_mask,
                                                     'echo276_percent_truncation', return_mask)

    return final_mask


def echo277_sigma_truncation(data_array, sigma_limits,
                             previous_mask={}, return_mask=False):
    """ This applies a mask on pixels outside a given multiple of a sigma 
    value.
    
    This function masks values if they are outsize of a sigma range from the 
    mean. The mean and sigma values are automatically calculated from the
    array provided. 

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from. 
    sigma_limits : float or ndarray
        The multiple of sigma which will be applied. Unequal bottom-top bounds
        may be set as a list-like input.
    previous_mask : dictionary (optional)
        Any previous masks done. The new mask made in this function will be  
        added to the dictionary. Default is to make a new mask dictionary.
    return_mask : boolean (optional)
        If this is true, then the mask itself (rather than the dictionary  
        entry) will be returned instead.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False)  
        will be added to the mask dictionary under the key 
        ``echo277_sigma_truncation``.
    """

    # Check if the sigma limits are the same, or the user provided for a lower
    # and upper sigma to use.
    if (isinstance(sigma_limits,(int,float))):
        # It is just a number, apply them evenly.
        bottom_sigma_multiple = sigma_limits
        top_sigma_multiple = sigma_limits
    elif (np.squeeze(np.array(sigma_limits)).size == 2):
        # It is asynchronous and valid, apply it as so.
        sigma_limits = np.squeeze(np.array(sigma_limits))
        bottom_sigma_multiple = sigma_limits[0]
        top_sigma_multiple = sigma_limits[-1]
    else:
        raise InputError("The sigma_limits parameter must either a number or a 2 large range "
                         "for the bottom and top sigma multiple bounds. It is unknown how to "
                         "handle the current input.")

    # Calculate the mean and the sigma values of the data array. Handle for NaNs.
    mean = np.nanmean(data_array)
    stddev = np.nanstd(data_array)
        
    # Compute which pixels to be masked out. 
    with warn.catch_warnings():
        warn.simplefilter("ignore", MaskingWarning)
        temp_mask_dict = {}
        temp_mask_dict = masks.echo270_minimum_cut(data_array, 
                                                   (mean - bottom_sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        temp_mask_dict = masks.echo271_maximum_cut(data_array, 
                                                   (mean + top_sigma_multiple * stddev),
                                                   previous_mask=temp_mask_dict)
        # Synthesize the top and bottom masks.
        masked_array = echo_funct.synthesize_mask_dictionary(temp_mask_dict)

    # Finally return
    final_mask = echo_funct.functioned_mask_returning(masked_array, previous_mask,
                                                     'echo277_sigma_truncation', return_mask)

    return final_mask
