"""
This contains the common functions dedicated to the reading, 
writing, and validating of configuration files.
"""

import copy
import configobj
import validate
import os
import shutil
import IfA_Smeargle.core as core


def extract_configuration(config_object, keys):
    """ This is a wrapper to obtain the configuration parameter from 
    the configuration tag. This function includes proper error 
    handling.
    
    Parameters
    ----------
    config_object : ConfigObj
        The configuration object that is going to be tested.
    keys : list
        The keys that should be called, in order.
    Returns
    -------
    value : object
        The value that the keys was containing.
    """

    # Copy objects, this is to ensure nothing is messed up.
    config_copy = dict(copy.deepcopy(config_object))
    keys_copy = copy.deepcopy(keys)
    
    # The keys must be a list, if only a single tag it is likely 
    # that the next result would be the answer.
    try:
        if ((isinstance(keys_copy,str)) or 
            ((len(keys_copy) == 1) and (isinstance(keys_copy,(list,tuple))))):
            # Return the value.
            keys_copy = ([keys_copy] if isinstance(keys_copy, str) 
                         else keys_copy)
            return config_copy[str(keys_copy[0])]
        elif (isinstance(keys_copy, (list, tuple))):
            # There likely is more sub-layers to this configuration 
            # file. Dig another layer deeper.
            new_config_object = config_object[keys_copy[0]]
            new_keys = tuple(keys[1:])

            return extract_configuration(config_object=new_config_object, 
                                         keys=new_keys)
        else:
            raise core.error.InputError("The keys were not in a manageable "
                                        "form specified by this function.")
    except (KeyError, AttributeError):
        raise KeyError("In the configuration file `{config_file}`, "
                       "there does not exist the configuration key "
                       "path:  {key_path}"
                       .format(config_file=config_object.filename, 
                               key_path='->'.join(keys)))

    # The program should not get to here.
    raise core.error.BrokenLogicError
    return None



def read_configuration_file(config_file_name, specification_file_name):
    """ This reads in a configuration file name specified by the 
    ConfigObj module. Verification is required.

    Parameters
    ----------
    config_file_name : string
        The path and file name of the configuration. If None, then 
        the defaults are returned.
    specification_file_name : string
        The path and file name of the specification/validation file.

    Returns
    -------
    configuration : ConfigObj
        The configuration according to the specification and 
        configuration files.    
    """
    
    # Reading the configuration. 
    if (config_file_name is None):
        # Assume defaults.
        config = configobj.ConfigObj(configspec=specification_file_name)
    else:
        # Make sure it exists.
        if (not os.path.isfile(config_file_name)):
            raise core.error.InputError("The configuration file `{path}` "
                                        "does not exist. Please correct it."
                                        .format(path=config_file_name))
        else:
            config = configobj.ConfigObj(config_file_name, 
                                         configspec=specification_file_name)

    # The validator to validate with and ensure proper input.
    validator = validate.Validator()

    # Validating, a passed validator is a true pass.
    validation_results = config.validate(validator)
    # Checking to see if it passed validation. 
    # As it will return a non-empty dictionary if it fails, direct 
    # comparison to True is required rather than implicit checking.
    if (validation_results == True):
        # It seems fine, attach the filename meta-data too.
        config.filename = config_file_name
        return config
    # A dictionary is returned if there were bad entires.
    elif (isinstance(validation_results, dict)):
        for (sectiondex, keydex, __) in configobj.flatten_errors(
            config, validation_results):
            # Going through all configuration keys to see where
            # it went wrong.
            if (keydex is not None):
                # Keys that did not pass validation.
                core.error.ifas_error(core.error.ConfigurationError,
                                      ("The key `{bad_key}` in section "
                                       "`{bad_sec}` failed validation. "
                                       "Please correct it."
                                       .format(
                                           bad_key=keydex, 
                                           bad_sec='->'.join(sectiondex))))
            else:
                # Sections that are missing.
                core.error.ifas_error(core.error.ConfigurationError,
                                      ("The following section(s) are "
                                       "missing:  {miss_sec}"
                                       .format(
                                           miss_sec=', '.join(sectiondex))))
        # Stop, let the user correct and have them re-run.
        raise core.error.ConfigurationError("The validaton of the "
                                            "configuration file failed. "
                                            "Please check that the "
                                            "configuration file is formatted "
                                            "to the specification file.")
    else:
        raise core.error.AssumptionError("It had been assumed that "
                                         "validation only returns a boolean "
                                         "or a dictionary.")
    # The program should not reach here.
    raise core.error.BrokenLogicError
    return None

def write_configuration_file(config_file_name, config_object, 
                             specification_file_name=None):
    """ This function takes a configuration object and writes it to 
    file. If provided with a default, it will also write it to file.

    Parameters
    ----------
    config_file_name : string
        The file name that the configuration object will be  
        written to.
    config_object : ConfigObj
        The configuration object that will be written to file.
    specification_file_name : string (optional)
        The specification file that is used in the event defaults 
        are wanted.
    
    Returns
    -------
    None
    """

    # If the user wanted the defaults instead.
    if (config_object is None):
        if (specification_file_name is None):
            raise core.error.ExportingError("There is no configuration or "
                                            "specification object or file. "
                                            "There is nothing to write or "
                                            "create and write.")
        else:
            # Providing the configuration file with the defaults 
            # already written in.
            config = configobj.ConfigObj(configspec=specification_file_name)
            validator = validate.Validator()
            config.validate(validator, copy=True)
    else:
        # We assume that the configuration object is normal.
        pass

    # Attaching the filename. Prioritize the user input over other 
    # meta-data.
    if (hasattr(config,'filename')):
        core.error.ifas_log_warning(core.error.ExportingWarning,
                                    ("There was a file name meta-data "
                                     "attachment to the configuration file. "
                                     "It will be replaced."))
    config.filename = config_file_name

    # Writing to file.
    config.write()

    return None

def copy_configuration_file(config_type, destination, file_name=None):
    """ This function finds a configuration file based on the 
    configuration type, and copies it directly into the destination
    directory. If the configuration file doesn't not exist within 
    the library, an exception is raised.
    
    Simple substring testing is used to check if the configuration
    type matches.

    Parameters
    ----------
    config_type : string
        The type of configuration file that can be copied.
    destination : string
        The destination directory for the configuration file type
        copy.
    file_name : string (optional)
        This is an optional file name. The extension .ini will be 
        added unless it is already present. No directory information
        should be provided here. Defaults to the copied file name.

    Returns
    -------
    config_path : string
        The new path that the configuration can be found at.
    """

    # Obtaining the list of configuration files.
    config_files = core.runtime.get_configuration_files()
    # This is mostly for error messages and warnings as it is a 
    # nice string of the available configurations.
    avaliable_config_types = ', '.join(
        [keydex for keydex, __ in config_files.items()])

    # Checking for valid configuration files.
    matching_files = {}
    for keydex, pathdex in copy.deepcopy(config_files).items():
        if (config_type in keydex):
            # The configuration file matches 
            matching_files[keydex] = pathdex
        else:
            # It is not a matching file.
            continue

    # There should only be one matching file. If there is an improper
    # number, then inform the user.
    if (len(matching_files) == 0):
        # There are no matching configurations.
        raise core.error.InputError("No configuration type `{type}` "
                                    "matches found. Nothing can be copied. "
                                    "The available configurations are: "
                                    "\n    {available}"
                                    .format(type=config_type, 
                                            available=avaliable_config_types))
    elif (len(matching_files) == 1):
        # All is normal, the configuration file should be copied 
        # into the new directory, the file name is added too.
        # Check on if the directory provided is a valid one.
        if (os.path.isdir(destination)):
            dir = destination
        elif (os.path.isfile(destination)):
            # Attempt to extract only the needed directory 
            # information.
            dir, __, __ = core.strformat.split_pathname(pathname=destination)
        else:
            raise core.error.InputError("The destination provided is not a "
                                        "valid directory. Destination: "
                                        "`{dest}`"
                                        .format(dest=destination))
        # The source path for the copied directory file. This should
        # be okay as there is only one entry in the dictionary.
        source_path = list(matching_files.values())[0]
        # Constructing the destination path name for the copied file.
        if (file_name is not None):
            # A file name was provided, use it.
            __, file_name, __ = core.strformat.split_pathname(
                pathname=file_name)
            config_path = core.strformat.combine_pathname(
                directory=dir, file_name=file_name, extension='.ini')
        else:
            # A file name has not been provided, default to the 
            # copied file name.
            __, file_name, __ = core.strformat.split_pathname(
                pathname=source_path)
            config_path = core.strformat.combine_pathname(
                directory=dir, file_name=file_name, extension='.ini')

        # Inform that the file is being copied.
        core.error.ifas_info("The configuration file matching {type} is "
                             "being copied. \n "
                             "Source: {src}   Destination: {dest}"
                             .format(type=config_type, src=source_path, 
                                     dest=config_path))
        # Copying the file.
        shutil.copyfile(source_path, config_path, follow_symlinks=True)

        # Returning the path in the event that they need it. 
        return config_path
    elif (len(matching_files) >= 2):
        # It is indeterminable as to which file should be coped.
        raise core.error.InputError("The configuration type `{type}` "
                                    "returned more than one valid "
                                    "configuration file. Narrow your type "
                                    "using more exact inputs for the "
                                    "available configuration files."
                                    "\n Matching:  {match} "
                                    "\n Available:  {available}"
                                    .format(type=config_type,
                                            match=', '.join(
                                                [keydex for keydex, __ 
                                                 in matching_files.items()]),
                                            available=avaliable_config_types))
    else:
        # There is no reason why the code should enter here as the 
        # lengths should be defined.
        raise core.error.BrokenLogicError

    # All done. Though, it should still not enter here either.
    raise core.error.BrokenLogicError
    return None