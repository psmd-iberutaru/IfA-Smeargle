"""
The purpose of this line is for the storage of configuration elements that are used on all 
other lines. The configuration of the entire Smeargle module is read, written, and used from
here.

Though technically a meta-line, as it is a full line in itself, it is not considered to fit 
in the meta functionality.
"""

import copy
import pickle

from ..meta import *

from . import configuration_classes as conclss


class SmeargleConfig(conclss.BaseConfig):
    """ Configuration class of the entire Smeargle pipeline and other properties.
    
    Each different array configuration must have its own reduction method. The purpose of this
    class is to be an organized collection of ALL configuration options possible. That is, 
    this class is read by the main pipeline and all other functions are created.

    Within each argument exists another configuration class specific to each of the Smeargle
    lines. They are defined in their appropriate files. 

    Arguments
    ---------
    EchoConfig : Configuration class
        The configuration class for the ECHO line.
    HotelConfig : Configuration class
        The configuration class for the HOTEL line.
    YankeeConfig : Configuration class
        The configuration class for the YANKEE line.

    BaseConfig : Configuration class
        The base configuration class, should generally not be used. 
    """


    EchoConfig = conclss.EchoConfig()
    HotelConfig = conclss.HotelConfig()
    YankeeConfig = conclss.YankeeConfig()




# Loading/unloading functions.
def write_config_file(config_class, file_name, 
                      protocol=pickle.HIGHEST_PROTOCOL):
    """ Function to write a specific configuration class to a normal file.

    As the entire module more or less depends on configuration classes. It is important to be
    able to save, copy, and reuse configuration classes. Therefore, this allows configuration
    files to be written to file. 

    Parameters
    ----------
    config_class : Configuration class
        The configuration class that is going to be saved as a file.
    file_name : string
        The name of the configuration class. The extension ``.ifaspkl`` is automatically 
        applied. This denotes a Python pickle file from IfA-Smeargle.
    protocol : int
        The pickling protocol value for the pickling function.

    Returns
    -------
    nothing

    """

    # Make sure the proper class is being sent through.
    if (not isinstance(config_class, SmeargleConfig)):
        raise InputError("Provided class is not a SmeargleConfig configuration class. It "
                         "would be improper to read it as one.")

    # Automatically apply extension for good file hygiene.
    if (file_name[-8:] == '.ifaspkl'):
        pass
    else:
        file_name += '.ifaspkl'

    # ...and write.
    with open(file_name, 'wb') as config_file:
        pickle.dump(config_class, config_file, protocol)


def read_config_file(file_name):
    """ Function to read a specific configuration class from a normal file.

    As the entire module more or less depends on configuration classes. It is important to be
    able to save, copy, and reuse configuration classes. Therefore, this allows pre-made/saved 
    configuration files to be read from a file.. 

    Parameters
    ----------
    file_name : string
        The path and name of the file that contains the configuration class. Must have the 
        extension ``.ifaspkl``

    Returns
    -------
    config_class : SmeargleConfig
        The configuration class stored in the file.

    """
    
    # Amateur checking to see the file is associated with IfA-Smeargle.
    if (file_name[-8:] != '.ifaspkl'):
        raise InputError("Provided file name does not have the .ifaspkl extension. This may be "
                         "the wrong file.")

    # Just to make sure that the class and its subclasses are loaded into scope.
    config_class = SmeargleConfig()

    # And load...
    with open(file_name,'rb') as config_file:
        config_class = pickle.load(config_file)
        config_class = copy.deepcopy(config_class)

    return config_class