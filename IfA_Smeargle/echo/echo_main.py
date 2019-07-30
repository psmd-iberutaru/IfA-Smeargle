
import copy
import glob
import inspect
import numpy as np
import warnings as warn


from IfA_Smeargle import echo
from IfA_Smeargle.echo import echo_functions as echo_funct
from IfA_Smeargle.echo import masks
from IfA_Smeargle.meta import *
from IfA_Smeargle import yankee



def echo_execution(data_array, configuration_class,
                   hushed=False):
    """ This script pragmatically uses a configuration class to determine  
    which filters to use.

    This function goes through all possible filters, applying those that the 
    user specified in their configuration file. It only applies those which  
    are flagged to run where there is also some configuration. It handles 
    cases where this is not true accordingly.

    Parameters
    ----------
    data_array : ndarray or string
        The data array that is to processed and filtered accordingly. A fits 
        file is also acceptable.
    configuration_class : SmeargleConfig or EchoConfig class
        The configuration class that will be used to provide instruction
        to the ECHO filters.
    hushed : boolean (optional)
        If true, then no warnings or informational messages will be displayed
        if and only if they come from this function, other warnings from 
        inner used functions still apply.
    
    Returns
    -------
    masked_array : Masked Array
        The data containing the masked values from the mask provided in the
        configuration parameters.
    masking_dict : dictionary
        The dictionary of all of the masks applied.

    """
    # Be adaptive with accepting a fits file.
    if (isinstance(data_array,str)):
        __, __, data_array = meta_faa.smeargle_open_fits_file(data_array)

    # Be adaptive as to which configuration class is given.
    provided_config = meta_config.extract_proper_configuration_class(configuration_class,
                                                                     yankee.EchoConfig)


    # Gathering all possible filters, given as a dictionary.
    filter_list = dict(inspect.getmembers(masks, inspect.isfunction))

    echo_filters = copy.deepcopy(filter_list)
    for keydex, valuedex in filter_list.items():
        if (not 'echo' in keydex):
            echo_filters.pop(keydex, None)

    # Extracting configuration parameters.
    temp_param_list = dict(inspect.getmembers(provided_config))
    config_param = copy.deepcopy(temp_param_list)
    for keydex, valuedex in temp_param_list.items():
        if (not 'echo' in keydex):
            config_param.pop(keydex, None)
    
    # This sorting method should suffice; these dictionaries must be 
    # parallel for the below method to work.
    echo_filters = echo_funct.sort_masking_dictionary(echo_filters)
    config_param = echo_funct.sort_masking_dictionary(config_param)

    # Loop and always add to the masking dictionary.
    masking_dict = {}
    for filter_keydex, config_keydex in zip(list(echo_filters.keys()),list(config_param.keys())):

        # Check if the names are related, ensuring proper filter-config 
        # pairing.
        if (filter_keydex[:7] != config_keydex[:7]):
            raise IllogicalProsedureError("Attempting mismatched filter-config process with "
                                          "{filter} and {config}".format(
                                              filter=filter_keydex,config=config_keydex))

        # Check if the filter should actually be run.
        try:
            if (not config_param[config_keydex]['run']):
                # Just send a notice that this filter is being skipped.
                if not (hushed):
                    # String concentration is first before function calls. 
                    print("Filter {filter} is being skipped "
                          "as noted by configuration class.".format(
                        filter=filter_keydex))
                # Skip the filter, continue to the next filter.
                continue
            else:
                # The 'run' key is not an official parameter; delete it before 
                # passing onto the function.
                proper_config_dict = copy.deepcopy(config_param[config_keydex])
                proper_config_dict.pop('run', None)

                # Run the masking filter.
                masking_dict = echo_filters[filter_keydex](data_array, 
                                                           previous_mask=masking_dict,
                                                           **proper_config_dict)
        except KeyError:
            smeargle_warning(ConfigurationWarning, ("The following configuration dictionary is "
                                                    "missing the 'run' parameter. The masking "
                                                    "method is skipped as if 'run'=False. \n"
                                                    "Problem configuration dictionary: \n  "
                                                    "{config_name}".format(
                                                        config_name=config_keydex)),
                             silent=hushed)
            continue

    # Making the masked array.
    masked_array = echo_funct.numpy_masked_array(data_array,synthesized_mask=None,
                                                 masking_dictionary=masking_dict)

    # And, return
    return masked_array, masking_dict


def echo_directory_execution(data_directory, configuration_class,
                             overwrite=True, hushed=False):
    """ This function extends the ECHO abilities to entire directories of
    using the same configuration file.

    The original echo_execution function only handles a single data array,
    computing the mask, and then returning a masked array. This function 
    extends such capabilities and overwrites the files.
    
    Parameters
    ----------
    data_directory : string
        The directory to the data files.
    configuration_class : SmeargleConfig or EchoConfig class
        The configuration class (and by extension, filters) that are to be
        used for all files.
    overwrite : boolean (optional)
        An option to decide if the files should be overwritten or renamed.
    hushed : boolean (optional)
        If true, then no warnings or informational messages will be displayed
        if and only if they come from this function, other warnings from 
        inner used functions still apply.

    Returns
    -------
    nothing
    """

    # Obtain the fits files by reference name.
    data_files = glob.glob(data_directory + '/*.fits')

    
    # Limit warnings, the files should be overwritten and should also
    # have the mask contained within.
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=OverwriteWarning)
        warn.simplefilter("ignore", category=OutputWarning)

        # Loop over all files.
        for filedex in data_files:
            # Execute the mask; catch the dictionary, it is unneeded though.
            masked_array, __ = echo.echo_execution(filedex, configuration_class,
                                                   hushed=hushed)

            # The Header should remain unchanged; it is read and reused 
            # from the file itself. 
            __, temp_header, __ = meta_faa.smeargle_open_fits_file(filedex)

            # Check for the overwriting option.
            if (overwrite):
                meta_faa.smeargle_write_fits_file(filedex, temp_header, masked_array)
            else:
                # This is incomplete, how to proceed is likely to require a 
                # list of strings equal in length to number of files.
                raise IncompleteError