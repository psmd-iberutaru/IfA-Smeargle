
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *


class YankeeConfig(BaseConfig):
    """This is the configuration class of the YANKEE line.

    The YANKEE line is mostly responsible for holding, storing, and reading 
    of configuration files and classes that dictate the rest  of the module's 
    behavior. 
    
    By default, all of the entries in the configurations are empty. Moreover, 
    each configuration attribute only contains the required entries. Optional 
    entries may be added at user  discretion (see documentation for such 
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
                smeargle_warning(ImportingWarning,("The configuration file could not be "
                                                   "properly read. Consider using the factory "
                                                   "function. A blank configuration class has "
                                                   "been provided instead."))

            pass
        
    pass


