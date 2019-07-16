
from IfA_Smeargle.meta import *

from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file \
    import read_config_file, write_config_file

class OscarConfig(BaseConfig):
    """This is the configuration class of the OSCAR line.

    The OSCAR line is mostly responsible for creating good histograms and 
    heat-maps of pixels and their value for further analysis. 
    
    By default, all of the entries in the configurations are empty. Moreover, 
    each configuration attribute only contains the required entries. Optional  
    entries may be added at user discretion (see documentation for such 
    entries).
    
    Attributes
    ----------
    heatmap_config : dictionary
        These are the parameters which are fed into 
        ``plot_array_heatmap_image``
    histogram_config : dictionary
        These are the parameters which are fed into 
        ``plot_array_histogram``

    heathist_config : dictionary
        These are the parameters which are fed into 
        ``plot_single_heatmap_and_histogram``

    """

    def __init__(self, file_name=None):

        try:
            provided_config = extract_proper_configuration_class(file_name, OscarConfig)
            self.__dict__.update(provided_config.__dict__)
        except Exception:
            if (file_name is not None):
                smeargle_warning(ImportingWarning,("The configuration file could not be "
                                                   "properly read. Consider using the factory "
                                                   "function. A blank configuration class has "
                                                   "been provided instead."))

            # Basic single plot, plotting functions.
            self.general_heatmap_config = {'plot': False, 'data_array':None}
            self.general_histogram_config = {'plot': False, 'data_array':None}

            # Complex multi-plot, plotting functions.

            # Too hard plotting functions, defaults are really not to be changed. 


