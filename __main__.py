
"""
This is the command-line interface of the script functions. It would
be improper to run the scripts from anyplace other than using this 
function.
"""

import argparse
import configobj
import copy
import sys
import os
import logging
import time 
import warnings as warn

import IfA_Smeargle.core as core
from IfA_Smeargle import runtime


def run_script(script_name, config_pathname):
    """
    This, in general, is the main function that calls the scripts 
    that should be executed and runs them as necessary.

    Parameters
    ----------
    script_name : string
        The name of the script function to invoke to run.
    config_pathname : string
        The path or filename to the configuration file.

    Returns
    -------
    result : object
        This returns whatever the script functions returns. More 
        often than not it is a NoneType None.
    """
    # Obtaining constants.
    SCRIPT_FUNCTIONS = runtime.get_script_functions()
    SPECIFICATION_FILES = runtime.get_specification_files()

    # Check if the script name is within the module.
    if (not script_name in SCRIPT_FUNCTIONS):
        raise core.error.InputError("The provided script name is not a "
                                    "valid script name. It does not have "
                                    "an associated script function.")

    # Check and load the configuration object. Validate it when 
    # needed.
    if (not os.path.isfile(config_pathname)):
        raise core.error.InputError("The configuration file `{path}` "
                                    "does not exist. Please correct it."
                                    .format(path=config_pathname))
    else:
        temp_config = configobj.ConfigObj(config_pathname)
    # Ensure that the configuration file is a valid one and extract  
    # the required validation/spec file for the proper loading.
    try:
        spec_key = core.config.extract_configuration(
            config_object=temp_config, keys=['meta','config_spec'])
    except KeyError:
        raise core.error.InputError("The configuration file must have a "
                                    "`meta` section and must contain the "
                                    "configuration key in order to be "
                                    "accepted. See template configuration "
                                    "files.")
    # Find the correct specification file and load it.
    try:
        spec_file = SPECIFICATION_FILES[spec_key]
    except KeyError:
        raise core.error.ConfigurationError("There is no configuration "
                                            "specification file associated "
                                            "with the `config_spec` entry. "
                                            "The available files are:  \n "
                                            "{valid_specs}"
                                            .format(valid_specs=str(list(
                                                SPECIFICATION_FILES.keys()))))

    # Load the configuration file properly now with the new 
    # specification file.
    config_obj = core.config.read_configuration_file(
        config_file_name=config_pathname, specification_file_name=spec_file)

    # Execute the scripted function as desired.
    script_function = SCRIPT_FUNCTIONS[script_name]
    result = script_function(config=config_obj)

    return result




if (__name__ == '__main__'):
    # Creating the argpaser
    parser = argparse.ArgumentParser(
        description=("Execute an IfA-Smeargle script function. Change the "
                     "script by name and the configuration parameters by "
                     "the configuration file."))

    # Adding the three required arguments for all pipelines. These 
    # are always constant requirements and thus are positional.
    parser.add_argument("script_key", 
                        help=("The name of the script function that you "
                              "are trying to run."),
                        type=str)
    parser.add_argument("config_file", 
                        help=("The path to the .ini configuration file "
                              "which will be used. The validation file is "
                              "found using the `meta` tag within the "
                              "configuration file. Null or None as in input "
                              "allows for scripts to be run without "
                              "configuration files."),
                        type=str)
    parser.add_argument("--log_file", 
                        default=time.strftime('%Y%m%d-%H%M%S(Z%z)'),
                        help=("This is the name of the log file that will "
                              "be written, it defaults to a time-stamp "
                              "based name."))
    parser.add_argument("--log_level", default='INFO',
                        help=("The logging level that will be recorded "
                              "for the log file."))

    # Parse the arguments.
    args = parser.parse_args()

    # Extract the arguments for visual purposes.
    script_key = str(args.script_key)
    config_file = str(args.config_file)
    log_file = str(args.log_file)
    log_level = str(args.log_level)

    # There is a special case for configuration files if the script
    # should not be run with one.

    # Have logging capabilities, writing out a log to file. Use the  
    # appropriate logging level and file based on input.
    _log_level_warning = False
    if(log_level.upper() == 'DEBUG'):
        log_config_level = logging.DEBUG
    elif(log_level.upper() == 'INFO'):
        log_config_level = logging.INFO
    elif(log_level.upper() == 'WARNING'):
        log_config_level = logging.WARNING
    elif(log_level.upper() == 'ERROR'):
        log_config_level = logging.ERROR
    elif(log_level.upper() == 'CRITICAL'):
        log_config_level = logging.CRITICAL
    else:
        # The warning cannot be here else the root logger will not 
        # use the file and will not record other log messages.
        _log_level_warning = True
        log_config_level = logging.INFO

    # Check that the file has the proper file extension.
    log_dir, log_filename, log_ext = core.strformat.split_pathname(
        pathname=copy.deepcopy(log_file))
    if (log_ext not in ('.txt', 'log')):
        # The warning cannot be here else the root logger will not 
        # use a file.
        _log_extension_warning = True
        log_file = os.path.join(log_dir, ''.join([log_filename, '.log']))
    else:
        _log_extension_warning = False

    # Create the logger and log all of the calls.
    logging.basicConfig(filename=log_file, level=log_config_level)
    # ...Also, raise the warnings that should have been triggered 
    # earlier.
    if (_log_level_warning):
        core.error.ifas_warning(core.error.InputWarning,
                                ("The log level inputted is not a valid log "
                                 "level based on the logging module. Using "
                                 "INFO as the default."))
    if (_log_extension_warning):
        core.error.ifas_warning(core.error.InputWarning, 
                                ("The log file does not have a normal "
                                 "extension. Using `.log` as a default."))

    # Change the runtime variables for convenience and for the other
    # functions that may need it.
    runtime._smeargle_runtime['CONFIG_FILE_PATH'] = config_file
    runtime._smeargle_runtime['LOG_FILE_PATH'] = log_file

    # Inform the user that the script is going to be run.
    core.error.ifas_info("BEGIN! Running the script `{script}` using the "
                         "configuration file `{config}`."
                         .format(script=script_key, config=config_file))
    # Execute the function. The returned value is likely lost in the  
    # first place by using a script.
    __ = run_script(script_name=script_key, config_pathname=config_file)

    # Inform the user when the script is finished, mostly for
    # completeness.
    core.error.ifas_info("FINISH! The script `{script}` using the "
                         "configuration file `{config}` has been completed."
                         .format(script=script_key, config=config_file))
    