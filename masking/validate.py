"""
This functions and masks only mask values which are inherently 
invalid through a software perspective. The values may be wrong 
scientifically, but these masks mask values based on mathematical 
rules.
"""

import numpy as np
import numpy.ma  as np_ma
import astropy as ap
import astropy.io.fits as ap_fits
import shutil
import os

import IfA_Smeargle.core as core
import IfA_Smeargle.masking as mask

def mask_invalids(data_array):
    """ This filter applies a mask to all numerically invalid inputs on a 
    programing side.

    Numbers that are usually infinite or some other nonsensical quantity 
    serve no real usage in calculations further downstream. Therefore, they 
    are masked here.

    See numpy.ma.fix_invalid for what is considered invalid.

    Parameters
    ----------
    data_array : ndarray
        The data array that the mask will be calculated from.

    Returns
    -------
    final_mask : ndarray -> dictionary
        A boolean array for pixels that are masked (True) or are valid 
        (False).

    """
    # As fixing all invalid data is required, masks might obscure the data
    # itself.
    raw_data_array = np_ma.getdata(data_array)
    # Mask all of the invalid data.
    final_mask = np_ma.getmaskarray(np_ma.fix_invalid(raw_data_array))

    return final_mask



# The scripts of the masks.
def script_mask_invalids(config):
    """ The scripting version of `mask_invalids`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])
    # Extract the masking programs configuration parameters.
    pass

    # The function that is being used to calculate the masks.
    masking_function = mask_invalids

    # Compiling the arguments that the masking function uses.
    masking_arguments = {}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_files(data_directory=data_directory,
                                          mask_function=masking_function,
                                          mask_arguments=masking_arguments,
                                          recursive=recursive, 
                                          subfolder=subfolder)

    # All done.
    return None