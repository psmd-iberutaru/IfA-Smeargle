
"""
Contains all of the methods used for renaming and reformatting data. 

Each function is dependent on the array and/or method. Only one function 
should ever be used for any one given process. 
"""

import glob

from IfA_Smeargle import bravo
from IfA_Smeargle import yankee

from IfA_Smeargle.meta import *

def bravo_execution_saphira(data_directory, configuration_class):
    """ Reformats data provided by a SAPHIRA array into a form used by this
    program.

    Each array or data set has their own different forms of representing the 
    data that has been collected. The purpose of this, and other modules, is
    to reformat and restructure the data collected into a more useful form
    for this program.

    The function automatically reformats the directories.

    Parameters
    ----------
    data_directory : ndarray
        The data array that is to processed and filtered accordingly
    configuration_class : SmeargleConfig or BravoConfig class
        The configuration class that will be used to provide instruction
        to the ECHO filters.
    
    Returns
    -------
    nothing
    """

    # Be adaptive as to which configuration class is given.
    provided_config = yankee.extract_proper_configuration_class(configuration_class,
                                                                yankee.BravoConfig)

    # Determine the detector's name.
    if (isinstance(provided_config.detector_name,str)):
        detector_name = provided_config.detector_name
    elif (isinstance(provided_config.detector_name,dict)):
        try:
            detector_name = provided_config.detector_name['name']
        except KeyError:
            raise ConfigurationError("The detector name cannot be found in the configuration "
                                     "file. It must either be a string or a dictionary with "
                                     "the name value referenced by the key <name>.")
    else:
        raise ConfigurationError("The detector name cannot be found in the configuration "
                                 "file. It must either be a string or a dictionary with "
                                 "the name value referenced by the key <name>.")

    # Getting the voltage renames
    voltage_names = bravo.rename.voltage_pattern_rename_fits(data_directory,
                                                         **provided_config.voltpat_rename_config)
    n_files = len(voltage_names)


    # Rename all of the files. The directory structure seems fine.
    final_names = []
    for index, detectdex, voltdex in zip(range(len(voltage_names)),
                                         [detector_name for index in range(n_files)],
                                         voltage_names):
        final_names.append(detectdex
                           + '__' + 'num;' + str(index + 1) 
                           + '__' + voltdex 
                           # + '__'
                           + '.fits')

    bravo.rename.parallel_renaming(None, final_names, data_directory, file_extensions='.fits')


    # Next, modifying the data to its own standard format. 
    averaging_names = glob.glob(data_directory + '/*' + '.fits')
    for fitsdex in averaging_names:
        bravo.avging.average_endpoints_per_second(fitsdex, 
                                                  **provided_config.avg_endpts_persec_config) 

    return None


