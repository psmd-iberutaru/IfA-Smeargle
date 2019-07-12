
"""
These functions just provide a nice and easy place to put functions whose
purpose is to allow for the proper reading of different possible arrangements
of the configuration parameters.
"""
import copy
import os

import IfA_Smeargle.yankee as yankee

from IfA_Smeargle.meta import *

from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file \
    import read_config_file, write_config_file




def extract_proper_configuration_class(configuration_class, desired_class,
                                       deep_copy=False):
    """ This function extracts the proper configuration class from a 
    collection of configuration classes.
    
    The whole point of this function is to retain the flexibility and ease
    of using differing configuration classes and the structure of the 
    configuration classes themselves. 

    Parameters
    ----------
    configuration_class : Any BaseConfig based class or string
        The main configuration class that should contain the desired class. 
        It may also be a file name.
    desired_class : Any BaseConfig based class execpt for BaseConfig
        The desired class.
    deep_copy : boolean (optional)
        If a deep copy of the class is desired, then set to True.

    Returns
    -------
    extracted_class : Any BaseConfig based class (same class as desired class)
        A copy of the desired configuration class.
    """

    # Test to see if it is a file name, if it is: load.
    if (isinstance(configuration_class,str)):
        configuration_class = read_config_file(configuration_class)

    # Test if the class is a base class, the base class has no configuration
    # value.
    if (desired_class is yankee.BaseConfig):
        raise ConfigurationError("The BaseConfig class does not have any configuration elements "
                                 "attached to it. In the case that it does for your code, "
                                 "it is suggested that it is changed.")
    # Test if useless to proceed because it is already finished.
    elif (type(configuration_class) == desired_class):
        # If the user really wants a deepcopy.
        if (deep_copy):
            extracted_class = copy.deepcopy(configuration_class)
        else:
            extracted_class = configuration_class
        return extracted_class
    # Test for subclasses:
    elif (isinstance(configuration_class,(yankee.BaseConfig,yankee.SmeargleConfig))):
        try:
            desired_class_name = desired_class.__name__
            extracted_class = getattr(configuration_class, desired_class_name)
            # If the user really wants a deep copy.
            if (deep_copy):
                extracted_class = copy.deepcopy(extracted_class)
            else:
                extracted_class = extracted_class
            return extracted_class

        except AttributeError:
            raise AttributeError("The configuration class provided does not have the desired "
                                 "configuration class. \n"
                                 "Config: {config}     Desired: {desire}".format(
                                     config=type(configuration_class),
                                     desire=desired_class))
    else:
        raise InputError("The class object provided is not a configuration class that is "
                         "easily understood by this program. We cannot proceed reading it.")

    # Function should not get here.
    raise BrokenLogicError("Something is broken, contact the software maintainers.")
    return None


def configuration_factory_function(desired_class, file_name=None,
                                   silent=False):
    """ A function that will always open or load the proper configuration
    class.

    This is considered the safest method of loading a configuration class 
    from file. This function returns the desired configuration file if it is
    contained within the file; else, it returns a blank configuration.

    Please note, this does not write the configuration class to file, ever.

    Parameters
    ----------
    desired_class : Configuration class
        The desired configuration class type that should be extracted from the 
        file.
    file_name : string (optional)
        The name of the configuration file. 
    silent : boolean (optional)
        If True, no warning(s) will be printed.
    
    Returns
    -------
    config_class : Configuration class
        The desired configuration class instance.
    """
    # Check that the desired class is actually a valid configuration class.
    if (not issubclass(desired_class,yankee.BaseConfig)):
        # Try one's best to deal with an instance of a configuration class.
        if (isinstance(desired_class,yankee.BaseConfig)):
            desired_class = type(desired_class)
        else:
            raise InputError("The desired class must be a member/sub class of the BaseConfig "
                             "class by which all IfA-Smeargle configuration classes are built "
                             "upon. The factory does not know what to return.")

    # Check if the file exists.
    if (file_name is None):
        # They did not specify a file at all.
        if (not silent):
            smeargle_warning(InputWarning, ("A file name has not be provided; this "
                                            "factory will return a blank configuration "
                                            "class."))
        config_class = desired_class()

    elif (isinstance(file_name,str)):
        # It may or may not be a class?
        if (os.path.isfile(file_name)):
            try:
                config_class = read_config_file(file_name)
            except Exception:
                # It did not seem to work.
                if (not silent):
                    smeargle_warning(InputWarning, ("The file could not be read "
                                                    "properly; this factory will return "
                                                    "a blank configuration class."))
                config_class = desired_class()
        else:
            # The provided path was not correct, the file does not exist.
            if (not silent):
                smeargle_warning(InputWarning, ("The file specified by file_name does not "
                                                "exist; this factory will return a blank "
                                                "configuration class."))
            config_class = desired_class()

    else:
        # The file_name parameter is un-useable in its current form.
        smeargle_warning(InputWarning, ("The file_name parameter is not understandable by "
                                        "this factory; this factory will return a blank "
                                        "configuration class."))
        config_class = desired_class()

    # Finally, return
    return config_class