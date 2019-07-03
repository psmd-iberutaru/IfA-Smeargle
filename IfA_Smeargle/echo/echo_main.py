

import inspect
import numpy as np

from ..meta import *

from IfA_Smeargle.echo import echo_functions as echo_funct
from IfA_Smeargle.echo import masks_echo000 as mask000
from IfA_Smeargle.echo import masks_echo100 as mask100
from IfA_Smeargle.echo import masks_echo200 as mask200
from IfA_Smeargle.echo import masks_echo300 as mask300



def execute_echo(data_array,configuration_class):
    """ This script pragmatically uses a configuration class to determine  
    which filters to use.

    This function goes through all possible filters, applying those that the 
    user specified in their configuration file. It only applies those which  
    are flagged to run where there is also some configuration. It handles 
    cases where this is not true accordingly.

    Parameters
    ----------
    data_array : ndarray
        The data array that is to processed and filtered accordingly
    configuration_class : EchoConfig class
        The configuration class that will be used to provide instruction
        to the ECHO filters.
    
    Returns
    -------
    masked_array : Masked Array
        The data containing the masked values from the mask provided in the
        configuration parameters.
    masking_dict : dictionary
        The dictionary of all of the masks applied.

    """

    # Gathering all possible filters, given as a dictionary.
    filter_000_list = dict(inspect.getmembers(mask000, inspect.isfunction))
    filter_100_list = dict(inspect.getmembers(mask100, inspect.isfunction))
    filter_200_list = dict(inspect.getmembers(mask200, inspect.isfunction))
    filter_300_list = dict(inspect.getmembers(mask300, inspect.isfunction))

    filter_list = {**{**filter_000_list,**filter_100_list},
                   **{**filter_200_list,**filter_300_list}}

    echo_filters = copy.deepcopy(filter_list)
    for keydex,valuedex in filter_list.items():
        if (not 'echo' in keydex):
            del echo_filters[keydex]

    # Extracting configuration parameters.
    temp_param_list = dict(inspect.getmembers(config.EchoConfig))
    config_param = copy.deepcopy(temp_param_list)
    for keydex, valuedex in temp_param_list.items():
        if (not 'echo' in keydex):
            del config_param[keydex]
    
    # This sorting method should suffice; these dictionaries should be 
    # parallel.
    echo_filters = echo_funct.sort_masking_dictionary(echo_filters)
    config_param = echo_funct.sort_masking_dictionary(config_param)


    # Loop and always add to the masking dictionary.
    masking_dict = {}
    for filter_keydex, config_keydex in zip(list(echo_filters.keys()),list(config_param.keys())):

        # Check if the names are related, ensuring proper filter-config 
        # pairing.
        if (filter_keydex[:7] != config_keydex[:7]):
            raise IllogicalProsedure("Attempting mismatched filter-config process with "
                                     "{filter} and {config}"
                                        .format(filter=filter_keydex,config=config_keydex))

        # Check if the filter should actually be run.
        if (not config_param[config_keydex]['run']):
            # Just send a notice that this filter is being skipped.
            print("Filter {filter} is being skipped as noted by configuration class."
                  .format(filter=filter_keydex))
            continue
        else:
            # Run the masking filter.
            masking_dict = echo_filters[filter_keydex](data_array, previous_mask=masking_dict,
                                                       **config_param[config_keydex])

    # Making the masked array.
    masked_array = echo_funct.numpy_masked_array(data_array,synthesized_mask=None,
                                                 masking_dictionary=masking_dict)

    # And, return
    return masked_array, masking_dict