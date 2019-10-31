"""
The purpose of this line is for the storage of configuration elements that are used on all 
other lines. The configuration of the entire Smeargle module is read, written, and used from
here.

Though technically a meta-line, as it is a full line in itself, it is not considered to fit 
in the meta functionality.
"""

import copy
import pickle

from IfA_Smeargle.meta import *

from IfA_Smeargle.yankee import configuration_classes as configclass

# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *


class SmeargleConfig(configclass.BaseConfig):
    """ Configuration class of the entire Smeargle pipeline and other 
    properties.
    
    Each different array configuration must have its own reduction method. 
    The purpose of this class is to be an organized collection of ALL  
    configuration options possible. That is, this class is read by the main 
    pipeline and all other functions are created.

    Within each argument exists another configuration class specific to each 
    of the Smeargle lines. They are defined in their appropriate files. 

    Arguments
    ---------
    BravoConfig : Configuration class
        The configuration class for the BRAVO line.
    EchoConfig : Configuration class
        The configuration class for the ECHO line.
    OscarConfig : Configuration class
        The configuration class for the OSCAR line.
    YankeeConfig : Configuration class
        The configuration class for the YANKEE line.

    BaseConfig : Configuration class
        The base configuration class, should generally not be used to store
        parameters.
    """

    def __init__(self, file_name=None):
        try:
            self.__dict__.update(extract_proper_configuration_class(file_name,
                                                                    SmeargleConfig).__dict__)
        except Exception:
            if (file_name is not None):
                smeargle_warning(ImportingWarning,("The configuration file could not be "
                                                   "properly read. Consider using the factory "
                                                   "function. A blank configuration class has "
                                                   "been provided instead."))

            self.BravoConfig = configclass.BravoConfig()
            self.EchoConfig = configclass.EchoConfig()
            self.OscarConfig = configclass.OscarConfig()
            self.YankeeConfig = configclass.YankeeConfig()
            self.ZuluConfig = configclass.ZuluConfig()

            self.BaseConfig = configclass.BaseConfig()




