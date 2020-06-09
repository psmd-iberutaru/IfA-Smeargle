"""
This module contains runtime-variables that are important for the 
function of this module.
"""


import copy
import glob
import os
import importlib
import inspect
import functools


import ifa_smeargle.core as core


def get_module_directory():
    """ This function returns the path of this module.
    
    
    Parameters
    ----------
    None

    Returns
    -------
    module_directory : string
        The directory of this module.
    """
    # Getting the module directory based on the script 
    # file's location.
    module_directory = os.path.dirname(os.path.abspath(__file__))

    # Adding the extra slash, else the directory name may be 
    # incorrectly split as a file name.
    module_directory = os.path.join(module_directory,'')

    return module_directory


def get_configuration_files():
    """ This function obtains all of the configuration files,
    returning a dictionary of them for each of their paths.
    
    The qualifier to be a configuration file is just to have `.ini` 
    extension to the file name.
    
    Parameters
    ----------
    None

    Returns
    -------
    config_files : dictionary
        The configuration files that have been found in the module 
        and its sub-modules.
    """

    # Extract the directory that the module is generally hosted in.
    module_pathname = get_module_directory()
    module_dir, __, __ = core.strformat.split_pathname(
        pathname=module_pathname)

    # Obtain all configuration files within that directory.
    config_file_list = glob.glob(
        core.strformat.combine_pathname(directory=[module_dir, '**'], 
                                        file_name=['*'], 
                                        extension=['.ini']), 
        recursive=True)

    # Constructing the dictionary, the key being the true file name 
    # without extension, the value being the full path.
    config_files = {}
    for filedex in config_file_list:
        __, config_key, config_ext = core.strformat.split_pathname(
            pathname=filedex)
        # Quick check that the configuration file really is one. 
        # (And that the splitting path name is a valid function.)
        assert (config_ext == '.ini')
        config_files[config_key] = filedex

    # The files have been combined.
    return config_files

def get_specification_files():
    """ This function obtains all of the configuration specification 
    files, returning a dictionary of them for each of their paths.
    
    The qualifier to be a specification file is just to have `.spec` 
    extension to the file name.
    
    Parameters
    ----------
    None

    Returns
    -------
    spec_files : dictionary
        The specification files that have been found in the module 
        and its sub-modules.
    """

    # Extract the directory that the module is generally hosted in.
    module_pathname = get_module_directory()
    module_dir, __, __ = core.strformat.split_pathname(
        pathname=module_pathname)
    
    # Obtain all specification files within that directory.
    spec_file_list = glob.glob(
        core.strformat.combine_pathname(directory=[module_dir, '**'], 
                                        file_name=['*'], 
                                        extension=['.spec']), 
        recursive=True)

    # Constructing the dictionary, the key being the true file name 
    # without extension, the value being the full path.
    spec_files = {}
    for filedex in spec_file_list:
        __, spec_key, spec_ext = core.strformat.split_pathname(
            pathname=filedex)
        # Quick check that the specification file really is one. 
        # (And that the splitting path name is a valid function.)
        assert (spec_ext == '.spec')
        spec_files[spec_key] = filedex

    # The files have been combined.
    return spec_files


def get_script_functions():
    """ This function obtains all possible `script` based 
    functions, returning a dictionary of them. 
    
    The qualifier to be a script function is just to have `script_`
    as the prefix to the function.
    
    Parameters
    ----------
    None

    Returns
    -------
    scripts : dictionary
        The scripts that have been found in the module and its
        sub-modules which have the scripting prefix.
    """
    # This is generally a wrapper around the main function.
    scripts = _get_any_tagged_functions(tag_prefix='script_')
    return scripts

def get_mask_functions():
    """ This function obtains all possible `mask` based 
    functions, returning a dictionary of them. 
    
    The qualifier to be a masking function is just to have `mask_`
    as the prefix to the function.
    
    Parameters
    ----------
    None

    Returns
    -------
    masks : dictionary
        The masking functions that have been found in the module 
        and its sub-modules which have the scripting prefix.
    """
    # This is generally a wrapper around the main function.
    masks = _get_any_tagged_functions(tag_prefix='mask_')
    return masks

def get_filter_functions():
    """ This function obtains all possible `filter` based 
    functions, returning a dictionary of them. 
    
    The qualifier to be a script function is just to have `filter_`
    as the prefix to the function.
    
    Parameters
    ----------
    None

    Returns
    -------
    filters : dictionary
        The filters that have been found in the module and its
        sub-modules which have the filtering prefix.
    """
    # This is generally a wrapper around the main function.
    filters = _get_any_tagged_functions(tag_prefix='filter_')
    return filters

def _get_any_tagged_functions(tag_prefix): 
    """ This function obtains all possible prefix-tagged based 
    functions, returning a dictionary of them. 
    
    The qualifier to be a tagged function is just to have the tag
    as the prefix to the function.
    
    Parameters
    ----------
    None

    Returns
    -------
    tagged_functions : dictionary
        The functions that have been found in the module and its
        sub-modules which have the prefix tag.
    """
    # Extract the directory that the module is generally hosted in.
    module_pathname = get_module_directory()
    module_dir, __, __ = core.strformat.split_pathname(
        pathname=module_pathname)
    
    # Obtain all python files within that directory.
    file_wildcard = core.strformat.combine_pathname(
        directory=[module_dir,'**'], file_name=['*'], extension='.py')
    module_files = glob.glob(file_wildcard, recursive=True)
    
    # A function to loading arbitrary source files (the ones just 
    # found).
    def _load_soruce(file_name, mod_pathname):
        """A function to loading arbitrary source files into the 
        program. 
        
        Credit: https://stackoverflow.com/a/19011259
        """
        __, module_filename, __ = core.strformat.split_pathname(
            pathname=mod_pathname)
        loader = importlib.machinery.SourceFileLoader(module_filename, 
                                                      file_name)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        
        return mod
    
    # Load all of the source files and extract the functions.
    function_list = {}
    for pyfiledex in module_files:
        # Load...
        pymod = _load_soruce(file_name=pyfiledex, 
                             mod_pathname=module_pathname)
        # Gathering all possible functions within the source file.
        function_list.update(
            dict(inspect.getmembers(pymod, inspect.isfunction)))
        # To reuse?
        del pymod

    # All scripts generally will have the same prefix. 
    for keydex, functiondex in copy.deepcopy(function_list).items():
        # Remove those that are not properly prefixed.
        if (tag_prefix != keydex[:len(tag_prefix)]):
            __ = function_list.pop(keydex, None)
        else:
            continue
    
    # For documentation.
    tagged_functions = function_list
    return tagged_functions



# To cache the results so there is less overhead.
@functools.lru_cache()
def extract_runtime_configuration(config_key):
    """ This function extracts the configuration based solely on the 
    key of the configuration value.

    The conversion of 'True'->bool(True) and 'False'->bool(False) is
    implicitly assumed. Letter case doesn't matter.

    Parameters
    ----------
    config_key : string
        The tag of the configuration parameter that is being sought.
    type_convert : boolean
        A flag to determine if type conversion is desired. If False, 
        the raw value is returned instead.

    Returns
    -------
    config_value : object
        The configuration object that is present within the file.  
    """

    # Get the all specification files and obtain the Smeargle one.
    spec_dict = get_specification_files()
    smeargle_spec = spec_dict.get('smeargle_specification')

    # Load the configuration.
    smeargle_config_path = glob.glob(
        os.path.join(get_module_directory(), 
                     '**', 'smeargle_configuration.ini'), 
        recursive=True)
    # There should be only one configuration file.
    if (len(smeargle_config_path) <= 0):
        raise core.error.TerminalError("The `smeargle_configuration.ini` "
                                       "file is missing. This file is "
                                       "required for the operation of this "
                                       "program.")
    elif (len(smeargle_config_path) == 1):
        smeargle_config = core.config.read_configuration_file(
            config_file_name=str(smeargle_config_path[0]), 
            specification_file_name=smeargle_spec)
    elif (len(smeargle_config_path) >= 2):
        raise core.error.AssumptionError("There should only be one "
                                         "`smeargle_configuration.ini` "
                                         "files. Please delete one: {paths}"
                                         .format(paths=smeargle_config_path))
    else:
        raise core.error.BrokenLogicError

    # Get the configuration parameter as desired.
    raw_config_value = core.config.extract_configuration(
        config_object=smeargle_config, keys=config_key)

    # Check if boolean conversion is needed.
    if (isinstance(raw_config_value,str)):
        if (raw_config_value.lower() == 'true'):
            # The boolean is True, so return it as such.
            config_value = True
        elif (raw_config_value.lower() == 'false'):
            # The boolean is False, so return it as such.
            config_value = False
        else:
            # The string is as it is, not a boolean.
            config_value = str(raw_config_value)
    else:
        # The default.
        config_value = raw_config_value
    # Return the configuration
    return config_value


# This is an index of all of the parameters that change at runtime,
# rather than a simple program configuration. These variables are
# used across all scripts, for all functions. Their global nature
# relegates them to this area. 
_smeargle_runtime = {
    # This is the path of the script configuration file.
    'CONFIG_FILE_PATH':None,
    # This is the path of the log file that is being used.
    'LOG_FILE_PATH':None,
    }


