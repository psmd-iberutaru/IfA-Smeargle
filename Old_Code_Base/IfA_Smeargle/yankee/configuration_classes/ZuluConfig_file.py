

from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

from IfA_Smeargle.meta import *
# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *


class ZuluConfig(BaseConfig):
    """This is the configuration class of the ZULU line.

    The ZULU line is responsible for collecting all functions for each 
    detector analysis line and grouping them into one method.
    
    By default, all of the entries in the configurations are empty. Moreover, 
    each configuration attribute only contains the required entries. Optional 
    entries may be added at user discretion (see documentation for such 
    entries).

    Note
    ----
    All built-in functions of the configuration classes are inherited from the 
    :py:class:`~IfA_Smeargle.yankee.configuration_classes.BaseConfig_file.BaseConfig`
    class. 

    Configuration classes such as this one is generally wrapped within the 
    :py:class:`~IfA_Smeargle.yankee.yankee_main.SmeargleConfig` class.
    

    Attributes
    ----------

    """

    def __init__(self, file_name=None):
        
        try:
            provided_config = yankee_extract_proper_configuration_class(file_name, YankeeConfig)
            self.__dict__.update(provided_config.__dict__)
        except Exception:
            if (file_name is not None):
                raise ImportingError("The configuration file could not be properly read. "
                                     "Consider using the factory function.")

            pass
        
    pass


