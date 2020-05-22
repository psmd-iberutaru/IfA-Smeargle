"""
This contains the common functions dedicated to the reading, writing, and
validating of configuration files.
"""

import copy
import configobj
import validate
import os
import IfA_Smeargle.core as core


def extract_configuration(config_object, keys):
    """ This is a wrapper to obtain the configuration parameter from the 
    configuration tag. This function includes proper error handling.
    
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
    
    # The keys must be a list, if only a single tag it is likely that the next
    # result would be the answer.
    try:
        if ((isinstance(keys_copy,str)) or 
            ((len(keys_copy) == 1) and (isinstance(keys_copy,(list,tuple))))):
            # Return the value.
            keys_copy = ([keys_copy] if isinstance(keys_copy, str) 
                         else keys_copy)
            return config_copy[str(keys_copy[0])]
        elif (isinstance(keys_copy, (list, tuple))):
            # There likely is more sub-layers to this configuration file. Dig 
            # another layer deeper.
            new_config_object = config_object[keys_copy[0]]
            new_keys = tuple(keys[1:])

            return extract_configuration(config_object=new_config_object, keys=new_keys)
        else:
            raise core.error.InputError("The keys were not in a manageable form specified "
                                        "by this function.")
    except (KeyError, AttributeError):
        raise KeyError("In the configuration file `{config_file}`, there does not exist the "
                       "configuration key path:  {key_path}"
                       .format(config_file=config_object.filename, key_path='->'.join(keys)))

    # The program should not get to here.
    raise core.error.BrokenLogicError
    return None



def read_configuration_file(config_file_name, specification_file_name):
    """ This reads in a configuration file name specified by the ConfigObj
    module. Verification is required.

    Parameters
    ----------
    config_file_name : string
        The path and file name of the configuration. If None, then the 
        defaults are returned.
    specification_file_name : string
        The path and file name of the specification/validation file.

    Returns
    -------
    configuration : ConfigObj
        The configuration according to the specification and configuration
        files.    
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
            config = configobj.ConfigObj(config_file_name, configspec=specification_file_name)

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
                                        ("The key `{bad_key}` in section `{bad_sec}` failed "
                                         "validation. Please correct it."
                                         .format(bad_key=keydex, bad_sec='->'.join(sectiondex))))
            else:
                # Sections that are missing.
                core.error.ifas_error(core.error.ConfigurationError,
                                        ("The following section(s) are missing:  {miss_sec}"
                                         .format(miss_sec=', '.join(sectiondex))))
        # Stop, let the user correct and have them re-run.
        raise core.error.ConfigurationError("The validaton of the configuration file failed. "
                                            "Please check that the configuration file is "
                                            "formatted to the specification file.")
    else:
        raise core.error.AssumptionError("It had been assumed that "
                                         "validation only returns a boolean "
                                         "or a dictionary.")
    # The program should not reach here.
    raise core.error.BrokenLogicError
    return None

def write_configuration_file(config_file_name, config_object, specification_file_name=None):
    """ This function takes a configuration object and writes it to file.
    If provided with a default, it will also write it to file.

    Parameters
    ----------
    config_file_name : string
        The file name that the configuration object will be written to.
    config_object : ConfigObj
        The configuration object that will be written to file.
    specification_file_name : string (optional)
        The specification file that is used in the event defaults are wanted.
    
    Returns
    -------
    None
    """

    # If the user wanted the defaults instead.
    if (config_object is None):
        if (specification_file_name is None):
            raise core.error.ExportingError("There is no configuration or specification object "
                                            "or file. I don't know what to do.")
        else:
            # Providing the configuration file with the defaults already
            # written in.
            config = configobj.ConfigObj(configspec=specification_file_name)
            validator = validate.Validator()
            config.validate(validator, copy=True)
    else:
        # We assume that the Configuration object is normal.
        pass

    # Attaching the filename. Prioritize the user input over other meta-data.
    if (hasattr(config,'filename')):
        core.error.ifas_log_warning(core.error.ExportingWarning,
                                    ("There was a file name meta-data attachment to the "
                                     "configuration file. It has been replaced."))
    config.filename = config_file_name

    # Writing to file.
    config.write()

    return None
