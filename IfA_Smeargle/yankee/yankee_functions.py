
"""
These functions just provide a nice and easy place to put functions whose
purpose is to allow for the proper reading of different possible arrangements
of the configuration parameters.
"""
import copy
import inspect
import os
import pickle

import IfA_Smeargle.yankee as yankee

from IfA_Smeargle.meta import *

def yankee_configuration_factory_function(desired_class, file_name=None, silent=False):
    """ A function that will always open or load the proper configuration
    class.

    This is considered the safest method of loading a configuration class 
    from file. This function returns the desired configuration file if it is
    contained within the file; else, it returns a blank configuration.

    Please note, this does not write the configuration class to file, ever.

    Parameters
    ----------
    desired_class : Configuration class type
        The desired configuration class type that should be extracted from the 
        file.
    file_name : string (optional)
        The name of the configuration file. 
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.
    
    Returns
    -------
    config_class : Configuration class
        The desired configuration class instance.
    """
    # Check if the user didn't want any warnings or info messages.
    if (silent):
        with smeargle_absolute_silence():
            return yankee_configuration_factory_function(desired_class, file_name=file_name)

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
        smeargle_warning(InputWarning, ("A file name has not be provided; this "
                                        "factory will return a blank configuration "
                                        "class."))
        config_class = desired_class()

    elif (isinstance(file_name,str)):
        # It may or may not be a class?
        if (os.path.isfile(file_name)):
            try:
                config_class = yankee_read_config_file(file_name)
            except Exception:
                # It did not seem to work.
                smeargle_warning(InputWarning, ("The file could not be read "
                                                "properly; this factory will return "
                                                "a blank configuration class."))
                config_class = desired_class()
        else:
            # The provided path was not correct, the file does not exist.
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


def yankee_extract_proper_configuration_class(configuration_class, desired_class,
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
    desired_class : Any BaseConfig based class except for BaseConfig type
        The desired class.
    deep_copy : boolean (optional)
        If a deep copy of the class is desired, then set to True.

    Returns
    -------
    extracted_class : Any BaseConfig based class (same class as desired class)
        A copy of the desired configuration class.
    """

    # Test to see if it is a file name, if it is: load.
    if (isinstance(configuration_class, str)):
        configuration_class = yankee_read_config_file(configuration_class)

    # Test if the class is a base class, the base class has no configuration
    # value.
    if (desired_class is yankee.BaseConfig):
        raise ConfigurationError("The BaseConfig class does not have any configuration elements "
                                 "attached to it. In the case that it does for your code, "
                                 "it is suggested that it is changed.")
    # Test if useless to proceed because it is already finished.
    elif (type(configuration_class) == desired_class):
        # If the user really wants a deep copy.
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
    raise BrokenLogicError("The configuration class extraction should have failed and raised "
                           "an InputError. It is unknown why this is not the case. ")
    return None


def yankee_fast_forward_configuration_class(configuration_class):
    """This functions updates the configuration class to the most compatible
    version.

    One of the byproducts of how the YANKEE line is coded is that 
    configuration files made in previous versions of IfA-Smeargle will not
    work by default. This function fixes that, returning an updated 
    configuration class that can be used with the current installed version.

    Parameters
    ----------
    configuration_class : Configuration Class
        The configuration class that is to be updated and fast-forwarded into
        its future.

    Returns
    -------
    updated_configuration_class : Configuration Class
        The configuration class that should be updated and compatible with
        the current version.
    """

    # Assume that the current module installation has the right class; if not
    # then that is a big issue with the maintainers.
    class_name = type(configuration_class).__name__
    
    # Obtain all of the possible configuration classes from YANKEE.
    yankee_classes = dict(inspect.getmembers(yankee, inspect.isclass))
    
    # Extract the default class instance from said list.
    default_class = yankee_classes[class_name]()

    # Update the old class with the new class, overwriting defaults with the
    # provided class.
    updated_configuration_class = yankee_overwrite_configuration_class(default_class,
                                                                configuration_class)

    # Finished and return
    return updated_configuration_class


def yankee_overwrite_configuration_class(inferior_class, superior_class):
    """ This function combines two configuration classes by overwriting some 
    parts with a more recent class.
    
    This function allows for two configuration classes to be combined. Where
    the two configuration classes collide, the ``superior`` class will 
    overwrite the ``inferior`` class objects.

    Parameters
    ----------
    inferior_class : Configuration Class
        The configuration class that is to be updated and conflicting 
        attributes be overwritten.
    superior_class : Configuration Class
        The configuration class that is to be added to and overwrite any 
        conflicts to the other class.  

    Returns
    -------
    combined_configuration_class : Configuration Class
        The configuration class that should be the correct combination of 
        both classes.
    """
    # Dictionaries are easier to use, as are copies.
    inferior_class = copy.copy(inferior_class)
    superior_class = copy.copy(superior_class)
    superior_class_dict = superior_class.__dict__
    inferior_class_dict = inferior_class.__dict__

    # Both classes should be YANKEE configuration classes, if not, then this
    # function doesn't make sense. 
    if (not isinstance(inferior_class, yankee.BaseConfig)):
        raise InputError("The inferior class must be a configuration class instance, that is, "
                         "any inherited class from BaseConfig.")
    if (not isinstance(superior_class, yankee.BaseConfig)):
        raise InputError("The superior class must be a configuration class instance, that is, "
                         "any inherited class from BaseConfig.")

    # Check to see if both classes are the same, if not, then it doesn't make
    # sense to combine them.
    if (type(inferior_class) is not type(superior_class)):
        raise TypeError("Both the inferior and superior class must have the same type. If one "
                         "is embedded in another, please extract them before combining.")

    # Cycle through all of the parameters in the class; replace inferior
    # class defaults with superior entries. 
    for inferior_keydex in inferior_class_dict.keys():
        # Replace inferior attributes with provided superior attributes.
        if (inferior_keydex in superior_class_dict):
            # BaseConfig-like objects should not be replaced completely, dig
            # deeper and replace only what is needed. 
            if (isinstance(superior_class_dict[inferior_keydex], yankee.BaseConfig)):
                # Iterate deeper, the deep copy may not be needed.
                replacing_value = copy.deepcopy(
                    yankee_overwrite_configuration_class(inferior_class_dict[inferior_keydex],
                                                  superior_class_dict[inferior_keydex]))
                inferior_class_dict.update({inferior_keydex:replacing_value})
            else:
                # Deep copy may not be needed.
                replacing_value = copy.deepcopy(superior_class_dict[inferior_keydex])
                inferior_class_dict.update({inferior_keydex:replacing_value})
        else:
            # There is no common object, keep inferior entries.
            pass

    # The ZULU configuration class must be handled a bit differently because
    # by design, there is no "template" that the above method can sort through.
    try:
        inferior_zulu = yankee_extract_proper_configuration_class(inferior_class, yankee.ZuluConfig)
        inferior_zulu_dict = inferior_zulu.__dict__
    except AttributeError:
        # The class to be updated does not contain a ZuluConfig configuration
        # class.
        inferior_zulu_dict = {}
    try:
        superior_zulu = yankee_extract_proper_configuration_class(superior_class, yankee.ZuluConfig)
        superior_zulu_dict = superior_zulu.__dict__
    except AttributeError:
        # The class to be updated does not contain a ZuluConfig configuration
        # class.
        superior_zulu_dict = {}
    try:
        inferior_class.ZuluConfig.__dict__.update({**inferior_zulu_dict, **superior_zulu_dict})
    except AttributeError:
        # The to be final class still does not have a ZuluConfig. So, add one.
        setattr(inferior_class, 'ZuluConfig', yankee.ZuluConfig())
        inferior_class.ZuluConfig.__dict__.update({**inferior_zulu_dict, **superior_zulu_dict})

    # All done, renaming for documentation sake. The inferior class elements 
    # were overwritten with the superior elements. 
    combined_configuration_class = copy.deepcopy(inferior_class)
    return combined_configuration_class


# Loading/unloading functions.
def yankee_write_config_file(config_class, file_name, 
                             overwrite=False, protocol=pickle.HIGHEST_PROTOCOL):
    """ Function to write a specific configuration class to a normal file.

    As the entire module more or less depends on configuration classes. It 
    is important to be able to save, copy, and reuse configuration classes. 
    Therefore, this allows configuration files to be written to file. 

    Parameters
    ----------
    config_class : Configuration class
        The configuration class that is going to be saved as a file.
    file_name : string
        The name of the configuration class. The extension ``.ifaspkl``  
        is automatically applied. This denotes a Python pickle file from 
        IfA-Smeargle.
    overwrite : boolean
        If true, the writing of the configuration class will overwrite any
        existing file.
    protocol : int
        The pickling protocol value for the pickling function.

    Returns
    -------
    nothing

    """

    # Ensure that the file name is actually a string.
    if (not isinstance(file_name,str)):
        raise InputError("Inputted class name variable is not a string. It cannot be converted "
                         "to a file name to write the configuration file.")

    # Make sure the proper class is being sent through.
    if (not isinstance(config_class, yankee.BaseConfig)):
        raise ExportingError("Provided class is not a Smeargle BaseConfig configuration class. It "
                             "would be improper to write it as one.")

    # Automatically apply extension for good file hygiene.
    if (os.path.splitext(file_name)[-1] == '.ifaspkl'):
        pass
    else:
        # It is missing the extension, add, but warn.
        smeargle_warning(InputWarning,("The provided file name is missing the .ifaspkl file "
                                       "extension. It has been automatically appended."))
        file_name += '.ifaspkl'

    # Check to see if the file exists, if so, then overwrite if provided for.
    if (os.path.isfile(file_name)):
        if (overwrite):
            # It should be overwritten, warn to be nice. 
            smeargle_warning(OverwriteWarning,("There exists a file with the provided name. "
                                               "Overwrite is true; the previous file will "
                                               "be replaced as provided."))
        else:
            # It should not overwritten at this point.
            raise ExportingError("There exists a file with the same name as the previous one. "
                                 "Overwrite is set to False; the new configuration file cannot "
                                 "be written.")

    # ...and write.
    with open(file_name, 'wb') as config_file:
        pickle.dump(config_class, config_file, protocol)


def yankee_read_config_file(file_name):
    """ Function to read a specific configuration class from a normal file.

    As the entire module more or less depends on configuration classes. It is 
    important to be able to save, copy, and reuse configuration classes.  
    Therefore, this allows pre-made/saved configuration files to be read from 
    a file.

    Parameters
    ----------
    file_name : string
        The path and name of the file that contains the configuration class. 
        Must have the extension ``.ifaspkl``

    Returns
    -------
    config_class : SmeargleConfig
        The configuration class stored in the file.

    """

    # Ensure that the file name is actually a string.
    if (not isinstance(file_name,str)):
        raise InputError("Inputted class name variable is not a string. It cannot be converted "
                         "to a file name to read the configuration file.")
    
    # Amateur checking to see the file is associated with IfA-Smeargle.
    if (os.path.splitext(file_name)[-1] != '.ifaspkl'):
        raise InputError("Provided file name does not have the .ifaspkl extension. This may be "
                         "the wrong file.")

    # And load...
    with open(file_name,'rb') as config_file:
        
        # Test if the class is defined.
        try:
            config_class = pickle.load(config_file)
        except AttributeError:
            raise ImportingError("The configuration class objects have not been imported "
                                 "properly. The depickleing has no template to use. Consider "
                                 "importing the configuration classes to __main__.")

    return config_class

