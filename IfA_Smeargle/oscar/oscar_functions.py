

import numpy as np
import numpy.ma as np_ma

from IfA_Smeargle.meta import *

def oscar_convert_data_inputs(data, desired_form=np.ma.MaskedArray):
    """ Converts between the many different types of inputs that are accepted.

    The following forms of data are currently accepted:
    - Numpy Array
    - Numpy Masked Array
    - .fits files (a string)
    
    Parameters
    ----------
    data : Any of the aforementioned types.
        The input data that is to be converted.
    desired_form : Any of the aforementioned types.
        The type that the output would be in. 

    Returns
    -------
    converted_data : Numpy Masked Array
        The data after conversion in its desired form.
    """

    # The default being a masked array.
    if (issubclass(desired_form, np_ma.MaskedArray)):
        if (isinstance(data, np_ma.MaskedArray)):
            # Test for Masked Arrays first because is-instance covers 
            # subclasses.
            converted_data = np_ma.array(data)
        elif (isinstance(data, np.ndarray)):
            # Converted to a masked array/
            converted_data = np_ma.array(data)
        elif (isinstance(data,str)):
            # Read the fits file.
            __, __, temp_data = meta_faa.smeargle_open_fits_file(data)
            converted_data = np_ma.array(temp_data)



    # Finally, return the data.
    return converted_data


def oscar_bin_width(data_array, bin_width,
                    local_minimum=None, local_maximum=None):
    """ Matplotlib does not support having input bin withs; this returns a 
    valid form.

    This function just generates a valid bin value list provided a given 
    bin widths. If the ``local_maximum`` or ``local_minimum value`` is not 
    provided, then the absolute maximum and minimum of the provided array is
    used. 

    If mod[(max - min), bin_width] != 0, the last/highest bin is 
    disenfranchised. This function can adapt to masked arrays. 

    Parameters
    ----------
    data_array : ndarray
        The data to which the bins will be calculated from; ignored if the two
        local maximum and minimum parameters are provided.
    bin_width : float
        The width of the bins.
    local_minimum : float (optional)
        A predefined minimum that the calculating function should use.
    local_maximum : float (optional)
        A predefined maximum that the calculating function should use. 

    Returns
    -------
    bin_list_values : ndarray
        A list of values that can be fed into matplotlib to emulate binning by
        a value width.
    """

    # Test if the user provided their own minimum or maximums.
    if ((local_minimum is not None) and (local_maximum is not None)):
        # They have, apply the minimum and maximums.
        minimum = local_minimum
        maximum = local_maximum
    else:
        # They have not, or at least, it is not a usable set.
        if (not isinstance(data_array,np.ndarray)):
            data_array = np.array(data_array)
        minimum = np.nanmin(data_array)
        maximum = np.nanmax(data_array)

    # Calculate the bins based off of the width provided. Numpy is pretty 
    # good with this.
    bin_list_values = np.arange(minimum, maximum, bin_width)
    bin_list_values = np.append(bin_list_values, maximum)

    # All done.
    return bin_list_values