
"""
This is the entire reduction method for the Saphria based infrared arrays.

"""
import glob

from IfA_Smeargle import bravo
from IfA_Smeargle import echo

from IfA_Smeargle.meta import *

def saphria_reduction_pipeline(data_directory, configuration_class):
    """This is the entire reduction and analysis pipeline for the SAPHRIA 
    arrays.

    This is the default reduction pipeline for the Saphria array. The
    "outputs" are written to file(s) and arranged in their own directory 
    instead of a Python output, mostly because of the sheer number of outputs.

    Parameters
    ----------
    data_directory : string
        The data directory straight out of the Saphria array. Data 
        preprocessing is internally handled.
    configuration_class : Configuration class
        The configuration class/options that go along with this reduction
        script. Must be a SmeargleConfig class instance.

    Returns
    -------
    nothing
    """

    # First, run the data reorganization program.
    bravo.bravo_execution_saphria(data_directory, configuration_class)

    
    # Apply the desired masks as needed. Although, the format provided by
    # the BRAVO line states that they should all be in the same directory.
    # Recursive is unneeded but still added.
    data_files = glob.glob(data_directory, recursive=True)
    for filedex in data_files:
        # Execute the mask.
        masked_array = echo.echo_execution(filedex, configuration_class)

        # Write the file, because masked arrays do not harm the original data
        # it is acceptable to overwrite.
        meta_faa.smeargle_write_fits_file(filedex, None, masked_array)



    # That should be it.
    return None