

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
