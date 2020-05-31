
"""
This is a special file. It contains many script functions which
do not fit the normal work-flow of this package.
"""

import pathlib

import IfA_Smeargle.core as core

def script_special_create_tutorial_configuration_file(config):
    """ This function copies a tutorial configuration file into
    the current working directory. It serves to initiate the  
    tutorials provided.

    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None    
    """
    # There are no configuration parameters needed for this function.

    # In order to copy the configuration into the current working
    # directory, the directory path must be known.
    current_directory = pathlib.Path().absolute()

    # Copy the tutorial configuration into the current directory.
    config_path = core.config.copy_configuration_file(
        config_type='tutorial', destination=current_directory, 
        file_name=None)

    # All done.
    return None
