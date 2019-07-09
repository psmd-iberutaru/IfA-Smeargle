
from IfA_Smeargle.meta import *

from .BaseConfig_file import BaseConfig

# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *
from IfA_Smeargle.yankee.configuration_classes.BaseConfig_file \
    import read_config_file, write_config_file

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
    detector_name : dictionary or string
        The name of the detector that is being processed.
    voltpat_rename_config : dictionary
        These are the parameters fed into ``voltage_pattern_rename_fits``
    avg_endpts_config : dictionary
        These are the parameters fed into ``average_endpoints``.
    """

    def __init__(self, file_name=None):

        try:
            provided_config = extract_proper_configuration_class(file_name, BravoConfig)
            self.__dict__.update(provided_config.__dict__)
        except Exception:
            if (file_name is not None):
                smeargle_warning(ImportingWarning,("The configuration file could not be "
                                                   "properly read. Consider using the factory "
                                                   "function. A blank configuration class has "
                                                   "been provided instead."))

            # The name of the detector.
            self.detector_name = {'name':None}

            # Renaming file
            self.voltpat_rename_config = {'voltage_pattern':None}


            # Preprocessing of beginning/end data for analysis.
            self.avg_endpts_config = {'start_chunk':None, 'end_chunk':None, 
                                      'frame_exposure_time':None}

    pass


