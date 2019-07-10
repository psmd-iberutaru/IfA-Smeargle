
from IfA_Smeargle.meta import *

from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file \
    import read_config_file, write_config_file

class EchoConfig(BaseConfig):
    """ This is the configuration class of the ECHO line.

    The ECHO line is mostly for masking techniques. Each attribute in this class is a
    dictionary entry that contains the parameters for these masking/filtering function.
    
    By default, all of the entries in the configurations are empty. Moreover, each configuration
    attribute only contains the required entries. Optional entries may be added at user 
    discretion (see documentation for such entries).

    Attributes
    ----------
    echo010_config : dictionary
        The configuration parameters for the ECHO-010 mask.

        .
        .
        .
        .

    echo399_config : dictionary
        The configuration parameters for the ECHO-399 mask.
    """

    def __init__(self, file_name=None):

        try:
            provided_config = extract_proper_configuration_class(file_name, EchoConfig)
            self.__dict__.update(provided_config.__dict__)
        except Exception:
            if (file_name is not None):
                smeargle_warning(ImportingWarning,("The configuration file could not be "
                                                   "properly read. Consider using the factory "
                                                   "function. A blank configuration class has "
                                                   "been provided instead."))

            # ECHO-000 class
            ################

            self.echo010_config = {'run':False}

            # ECHO-100 class
            ################

            self.echo120_config = {'run':False, 'x_range': None, 'y_range':None}

            # ECHO-200 class
            ################

            self.echo270_config = {'run':False, 'minimum_value':None}
            self.echo271_config = {'run':False, 'maximum_value':None}
            self.echo275_config = {'run':False, 'top_count':None, 'bottom_count':None}
            self.echo276_config = {'run':False, 'kept_range':None}

            # ECHO-300 class
            ################

            self.echo380_config = {'run':False, 'pixel_list':None}
            self.echo381_config = {'run':False, 'x_ranges':None, 'y_ranges':None}
            self.echo382_config = {'run':False, 'column_list':None}
            self.echo383_config = {'run':False, 'row_list':None}

            self.echo398_config = {'run':False}
            self.echo399_config = {'run':False}

    pass

    
