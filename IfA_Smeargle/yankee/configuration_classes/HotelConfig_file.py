
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file import BaseConfig

class HotelConfig(BaseConfig):
    """This is the configuration class of the HOTEL line.

    The HOTEL line is mostly responsible for creating good histograms and 
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

    # Basic single plot, plotting functions.
    heatmap_config = {'plot': False, 'data_array':None}
    histogram_config = {'plot': False, 'data_array':None}

    # Complex multi-plot, plotting functions.
    heathist_config = {'plot': False, 'data_array':None}

    # Too hard plotting functions, defaults are really not to be changed. 


