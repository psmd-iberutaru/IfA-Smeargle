
"""
This is the command-line interface of the script functions. It would
be improper to run the scripts from anyplace other than using this 
function.
"""

import ast
import argparse
import configobj
import copy
import sys
import os
import logging
import time 
import textwrap
import warnings as warn

import ifa_smeargle.core as core


def run_script(script_name, config_pathname, override=None):
    """
    This, in general, is the main function that calls the scripts 
    that should be executed and runs them as necessary.

    Parameters
    ----------
    script_name : string
        The name of the script function to invoke to run.
    config_pathname : string
        The path or filename to the configuration file.
    override : dictionary
        The override. If this is set, then the configuration
        dictionary overwrites the configuration object where needed.


    Returns
    -------
    result : object
        This returns whatever the script functions returns. More 
        often than not it is a NoneType None.
    """
    # Obtaining constants.
    SCRIPT_FUNCTIONS = core.runtime.get_script_functions()
    SPECIFICATION_FILES = core.runtime.get_specification_files()

    # Check if the script name is within the module.
    if (not script_name in SCRIPT_FUNCTIONS):
        raise core.error.InputError("The provided script name `{script}` is "
                                    "not a valid script name. It does not "
                                    "have an associated script function."
                                    .format(script=str(script_name)))

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

    # Apply any overrides if need be.
    if (isinstance(override, dict)):
        config_obj.merge(override)
    else:
        # No need.
        pass

    # Execute the scripted function as desired.
    script_function = SCRIPT_FUNCTIONS[script_name]
    result = script_function(config=config_obj)

    return result

def run_entry():
    """
    This allows for the .exe based script version to run. It
    prompts for the input of the script name and the configuration
    file path.

    Parameters
    ----------
    none

    Returns
    -------
    result : object
        This returns whatever the script functions returns. More 
        often than not it is a NoneType None.
    """
    # Prompt for the input of the script name.
    script_key = input("Input the script name that you want to run:  ")
    # Prompt for the input of the configuration file path.
    config_file = input("Input the path to the configuration file:  ")

    # There is a special case for configuration files if the script
    # should not be run with one.
    if ((config_file.lower() == 'none') or (config_file.lower() == 'null')):
        # The user input the special string to run a script
        # without any explicit configuration file. However, logs 
        # cannot be called until the file manger is set.
        _log_blank_configuration_info = True

        # Obtain the list of all configuration files, the blank one
        # should be in there.
        config_files = core.runtime.get_configuration_files()
        # Find the blank specification file.
        blank_config_path = config_files.get('blank_configuration', None)
        # If the file is not there, raise as it should be there.
        try:
            if (blank_config_path is None):
                raise FileNotFoundError("The blank configuration path "
                                        "cannot be found in the dictionary "
                                        "of configuration files.")
            elif (not os.path.isfile(blank_config_path)):
                raise FileNotFoundError("The blank configuration path does "
                                        "not lead to a proper file.")
            elif (core.strformat.split_pathname(
                pathname=blank_config_path)[-1] != '.ini'):
                raise FileNotFoundError("The blank configuration path does "
                                        "not lead to a configuration file.")
            else:
                # The configuration file shall be reassigned as a
                # blank file as per functionality.
                config_file = blank_config_path
        except FileNotFoundError:
            raise core.error.AssumptionError("The blank configuration file "
                                             "cannot be used or found. The "
                                             "configuration file path: "
                                             "{path}"
                                             .format(path=blank_config_path))
    else:
        pass
    
    # Create the logger and log all of the calls.
    logging.basicConfig(filename=time.strftime('%Y%m%d-%H%M%S(Z%z).log'))

    # Inform the user that the script is going to be run.
    core.error.ifas_info("BEGIN! Running the script `{script}` using the "
                         "configuration file `{config}`."
                         .format(script=script_key, config=config_file))
    # Execute the function. The returned value is likely lost in the  
    # first place by using a script.
    result = run_script(script_name=script_key, config_pathname=config_file)

    # Inform the user when the script is finished, mostly for
    # completeness.
    core.error.ifas_info("FINISH! The script `{script}` using the "
                         "configuration file `{config}` has been completed."
                         .format(script=script_key, config=config_file))
    # All done.
    return result

if (__name__ == '__main__'):
    # Creating the argpaser. The textwrap is for formatting.
    parser = argparse.ArgumentParser(
        description=textwrap.indent(textwrap.dedent(
            '''
            Execute an IfA-Smeargle script function. Change the 
            script by name and the configuration parameters by the 
            configuration file."
            '''), prefix='  '),
        epilog=textwrap.indent(textwrap.dedent(
            '''
            The script to show all available scripts is:
                python -m ifa_smeargle script_special_list_scripts none
            '''), prefix='  '),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Adding the three required arguments for all pipelines. These 
    # are always constant requirements and thus are positional.
    parser.add_argument("script_key", 
                        help=("the name of the script function to be run"),
                        type=str)
    parser.add_argument("config_file", 
                        help=("the path to the configuration file; if "
                              "`none` or `null` a blank one is used"),
                        type=str)
    parser.add_argument("--override", default='None',
                        help=("a python-like dictionary specifying "
                              "configuration parameters to be overridden"))
    parser.add_argument("--log_file", 
                        default=time.strftime('%Y%m%d-%H%M%S(Z%z)'),
                        help=("the log file to be used to log messages "
                              "while the script is being run"))
    parser.add_argument("--log_level", default='INFO',
                        help=("the level for the logger to determine what "
                              "should be logged or not"))

    # Parse the arguments.
    args = parser.parse_args()

    # Extract the arguments for visual purposes.
    script_key = str(args.script_key)
    config_file = str(args.config_file)
    override = str(args.override)
    log_file = str(args.log_file)
    log_level = str(args.log_level)

    # There is a special case for configuration files if the script
    # should not be run with one.
    if ((config_file.lower() == 'none') or (config_file.lower() == 'null')):
        # The user input the special string to run a script
        # without any explicit configuration file. However, logs 
        # cannot be called until the file manger is set.
        _log_blank_configuration_info = True

        # Obtain the list of all configuration files, the blank one
        # should be in there.
        config_files = core.runtime.get_configuration_files()
        # Find the blank specification file.
        blank_config_path = config_files.get('blank_configuration', None)
        # If the file is not there, raise as it should be there.
        try:
            if (blank_config_path is None):
                raise FileNotFoundError("The blank configuration path "
                                        "cannot be found in the dictionary "
                                        "of configuration files.")
            elif (not os.path.isfile(blank_config_path)):
                raise FileNotFoundError("The blank configuration path does "
                                        "not lead to a proper file.")
            elif (core.strformat.split_pathname(
                pathname=blank_config_path)[-1] != '.ini'):
                raise FileNotFoundError("The blank configuration path does "
                                        "not lead to a configuration file.")
            else:
                # The configuration file shall be reassigned as a
                # blank file as per functionality.
                config_file = blank_config_path
        except FileNotFoundError:
            raise core.error.AssumptionError("The blank configuration file "
                                             "cannot be used or found. The "
                                             "configuration file path: "
                                             "{path}"
                                             .format(path=blank_config_path))
    else:
        # The configuration file should be treated as a normal file.
        _log_blank_configuration_info = False

    # If any configuration parameters should be overrun, then 
    # apply them.
    override = ast.literal_eval(override)
    if (override is not None):
        # The user wanted some sort of override.
        override = dict(override)
    else:
        # The configuration should be untouched. The override
        # should be blank.
        override = dict()

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
    if (_log_blank_configuration_info):
        core.error.ifas_info("The configuration file path provided is "
                             "equivalent None or Null, a blank "
                             "configuration will be used.")

    # Change the runtime variables for convenience and for the other
    # functions that may need it.
    core.runtime._smeargle_runtime['CONFIG_FILE_PATH'] = config_file
    core.runtime._smeargle_runtime['LOG_FILE_PATH'] = log_file

    # Inform the user that the script is going to be run.
    core.error.ifas_info("BEGIN! Running the script `{script}` using the "
                         "configuration file `{config}`."
                         .format(script=script_key, config=config_file))
    # Execute the function. The returned value is likely lost in the  
    # first place by using a script.
    __ = run_script(script_name=script_key, config_pathname=config_file,
                    override=override)

    # Inform the user when the script is finished, mostly for
    # completeness.
    core.error.ifas_info("FINISH! The script `{script}` using the "
                         "configuration file `{config}` has been completed."
                         .format(script=script_key, config=config_file))
    