
"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 100; this file only contains ECHO-100 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn

import masks_echo000, masks_echo200, masks_echo300 as masks 


def echo_130_pixel_trimming(data_array, previous_mask={}, 
                            method='default',
                            trim_parameters={
                                # Required for percentcut and hardcut.
                                'upper':None, 'lower':None
                                }):
    """ This applies a pixel trimming mask based on set parameters. 
    
    Pixel trimming is used to cut pixels that are considered to be outliers. There are many
    different methods that one can use to accomplish this. As such, this function can use
    many different methods.

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
    method : string (optional)
        The method of pixel trimming that will be used. Available methods (consult readme.md
        markdown for more information).

        - ``percentcut``
        - ``hardcut``
        - ``nothing``

    trim_parameters : dictionary
        The parameters required for some methods of trimming (such as percentcut and hardcut).

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid (False) will be added to 
        the mask dictionary under the key ``echo130_pixtrim``.

    """

    def _pixel_trim_percentcut(data_array, upper=None, lower=None):
        """ The implementation of the percent cut algorithm.
        
        The values of ``upper`` and ``lower`` is the fraction of how much pixels are taken off
        from the upper bound and lower bound respectively. 
        """

        # Make sure the values of upper and lower make some sort of sense.
        if ((upper < 0.0) or (upper > 1.0)):
            raise ValueError("The upper percentage must be between 0 - 1.")
        if ((lower < 0.0) or (lower > 1.0)):
            raise ValueError("The lower percentage must be between 0 - 1.")
        
        # Find the pixel index (and value) corresponding to the upper and lower limits.
        flat_data_array = np.sort(data_array, axis=None)
        array_size = flat_data_array.size
        upper_index = int(np.ceil((1 - upper) * array_size))
        lower_index = int(np.floor(lower * array_size))
        # ...and value.
        upper_value = flat_data_array[upper_index]
        lower_value = flat_data_array[lower_index]

        # Because the above method uses float multiplication, there can be issues with
        # significant digits.
        if (array_size >= 1e10):
            warn.warn(("Determining upper and lower index values uses float multiplication. "
                       "The indexes may be a bit off because the array size is greater than a "
                       "billion."),
                      RuntimeWarning)

        # Now that the numerical bounds have been established, the percentcut has been turned 
        # into a hardcut.
        masked_array = _pixel_trim_hardcut(data_array, upper=upper_value, lower=lower_value)

        return masked_array


    def _pixel_trim_hardcut(data_array, upper=None, lower=None):
        """ The implementation of the hard value cut algorithm. 
        
        The values of ``upper`` and ``lower`` should be hard pixel values. Any pixel value above 
        ``upper`` and below ``lower`` are flagged (True), else they are fine (False).
        """

        # Make sure that the upper and lower values make sense.
        if (lower >= upper):
            raise ValueError("It does not make sense for the lower bound to be greater than the "
                             "upper bound. The lower bound must be less than the upper bound.")

        # Abusing np.where. If condition is true, then the pixel is considered bad.
        masked_array = np.where(((data_array > upper) or (data_array < lower)), x=True, y=False)

        return masked_array

    
    def _pixel_trim_nothing(data_array):
        """ The implementation of the nothing cut algorithm.

        This is really just for completeness, and the event that the blank all False mask is
        needed. Pixels flagged are True, else False.
        
        """

        masked_array = masks.echo_398_nothing(data_array, return_mask=True)

        return masked_array

    # Finally, determine which method to use.
    method = method.lower()
    if (method == 'percentcut'):
        masked_array = _pixel_trim_percentcut(data_array, **trim_parameters)
    elif (method == 'hardcut'):
        masked_array = _pixel_trim_hardcut(data_array, **trim_parameters)
    elif (method == 'nothing'):
        masked_array = _pixel_trim_nothing(data_array)


    # Figure out what to return.
    if (return_mask):
        final_mask = masked_array
    elif (not return_mask):
        final_mask = previous_mask
    else:
        final_mask = previous_mask

    return final_mask
