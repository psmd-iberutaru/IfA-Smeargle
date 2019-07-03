
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

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


    # ECHO-000 class
    ################

    echo010_config = {'run':False}

    # ECHO-100 class
    ################

    echo120_config = {'run':False, 'x_range': None, 'y_range':None}

    # ECHO-200 class
    ################

    echo270_config = {'run':False, 'minimum_value':None}
    echo271_config = {'run':False, 'maximum_value':None}
    echo275_config = {'run':False, 'top_count':None, 'bottom_count':None}
    echo276_config = {'run':False, 'kept_range':None}

    # ECHO-300 class
    ################

    echo380_config = {'run':False, 'pixel_list':None}
    echo381_config = {'run':False, 'x_ranges':None, 'y_ranges':None}
    echo382_config = {'run':False, 'column_list':None}
    echo383_config = {'run':False, 'row_list':None}

    echo398_config = {'run':False}
    echo399_config = {'run':False}
