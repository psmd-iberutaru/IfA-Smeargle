
from .BaseConfig_file import BaseConfig

class BravoConfig(BaseConfig):
    """This is the configuration class of the BRAVO line.

    The BRAVO line is mostly responsible for gathering the data from the 
    raw output of the detector and processing it in a form that the later 
    lines can use.
    
    By default, all of the entries in the configurations are empty. Moreover, 
    each configuration attribute only contains the required entries. Optional 
    entries may be added at user discretion (see documentation for such 
    entries).
    

    Attributes
    ----------
    voltpat_rename_config : dictionary
        These are the parameters fed into ``voltage_pattern_rename_fits``
    """

    # Renaming file
    voltpat_rename_config = {'data_directory':None, 'voltage_pattern':None}



    # Preprocessing of beginning/end data for analysis.
    avg_endpts_config = {'fits_file':None, 'start_chunk':None, 'end_chunk':None, 
                         'frame_exposure_time':None}

    pass


