
"""
This is a special file. It contains many script functions which
do not fit the normal work-flow of this package.
"""

import pathlib
import numpy as np

import ifa_smeargle.core as core



def script_special_create_configuration_file(config):
    """ This function copies a given configuration file into
    the current working directory. The type of configuration is 
    given by the configuration object.

    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None    
    """
    # The configuration type.
    try:
        type = core.config.extract_configuration(
            config_object=config, keys=['type'])
    except KeyError as error:
        core.error.ifas_error(type(error), str(error))
        raise core.error.ConfigurationError("This script requires that the "
                                            "configuration file type is in "
                                            "the configuration class. You "
                                            "may use "
                                            "`--override={'type':type}` to "
                                            "specify the type.")

    # In order to copy the configuration into the current working
    # directory, the directory path must be known.
    current_directory = pathlib.Path().absolute()

    # Copy the tutorial configuration into the current directory.
    config_path = core.config.copy_configuration_file(
        config_type=type, destination=current_directory, 
        file_name=None)

    # All done.
    return None


def script_special_list_scripts(config):
    """ This lists all of the scripts in alphabetical order in 
    two columns.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None    
    """

    # There are no real configuration parameters needed.
    pass

    # Obtain the list of all scripts.
    script_functions = core.runtime.get_script_functions()
    # Only the keys are needed.
    script_keys = list(script_functions.keys())
    # Sorting them as the script printing should be in alphabetical 
    # order.
    sorted_script_keys = sorted(script_keys)
    n_keys = len(sorted_script_keys)
    max_length = len(max(sorted_script_keys, key=len))
    
    # Format the key list in the two columns, going across first
    # so the alphabetical list is spread across the two.
    printed_lines = []
    for evendex, odddex in zip(np.arange(0, n_keys + 1, 2), 
                               np.arange(1, n_keys + 1, 2)):
        # This is the left entry of the line.
        try:
            temp_left_entry = sorted_script_keys[evendex].ljust(max_length)
        except IndexError:
            # The default empty line if there was none to print.
            temp_left_entry = '-' * max_length
        # This is the right entry of the line.
        try:
            temp_right_entry = sorted_script_keys[odddex].ljust(max_length)
        except IndexError:
            # The default empty line if there was none to print.
            temp_right_entry = '-' * max_length
        # Compile the line itself.
        temp_line = ' '.join([temp_left_entry, temp_right_entry])
        printed_lines.append(temp_line)

    # Display the information as normal information. (Some fancy 
    # formatting to help the eyes.)
    core.error.ifas_info("The list of all callable scripts are: \n"
                         "{hline} \n"
                         "{script_print}"
                         "\n"
                         .format(hline=''.join(['=' for __ in range(49)]),
                                 script_print='\n'.join(printed_lines)))
    
    # All done.
    return None