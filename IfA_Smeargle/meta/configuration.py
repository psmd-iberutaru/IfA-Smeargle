
"""
These functions just provide a nice and easy place to put functions whose
purpose is to allow for the proper reading of different possible arrangements
of the configuration parameters.
"""
import copy

from IfA_Smeargle.meta import *
import IfA_Smeargle.yankee as yankee


def extract_proper_configuration_class(configuration_class, desired_class,
                                       deep_copy=False):
    """ This function extracts the proper configuration class from a 
    collection of configuration classes.
    
    The whole point of this function is to retain the flexibility and ease
    of using differing configuration classes and the structure of the 
    configuration classes themselves. 

    Parameters
    ----------
    configuration_class : Any BaseConfig based class
        The main configuration class that should contain the desired class.
    desired_class : Any BaseConfig based class execpt for BaseConfig
        The desired class.
    deep_copy : boolean (optional)
        If a deep copy of the class is desired, then set to True.

    Returns
    -------
    extracted_class : Any BaseConfig based class (same class as desired class)
        A copy of the desired configuration class.
    """

    # Test if the class is a base class, the base class has no configuration
    # value.
    if (desired_class is yankee.BaseConfig):
        raise ConfigurationError("The BaseConfig class does not have any configuration elements "
                                 "attached to it. In the case that it does for your code, "
                                 "it is suggested that it is changed.")
    # Test if useless to proceed because it is already finished.
    elif (configuration_class is desired_class):
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
            extracted_class = getattr(configuration_class,desired_class_name)
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
