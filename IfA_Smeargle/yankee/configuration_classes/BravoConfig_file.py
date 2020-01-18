
from IfA_Smeargle.meta import *

from .BaseConfig_file import BaseConfig

from IfA_Smeargle.meta import *
# Pulling deeper functions into the light.
from IfA_Smeargle.yankee.yankee_functions import *

class BravoConfig(BaseConfig):
    """This is the configuration class of the BRAVO line.

    The BRAVO line is mostly responsible for gathering the data from the 
    raw output of the detector and processing it in a form that the later 
    lines can use.
    
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
    detector_name : dictionary or string
        The name of the detector that is being processed.
    voltpat_rename_config : dictionary
        These are the parameters fed into ``voltage_pattern_rename_fits``
    avg_endpts_config : dictionary
        These are the parameters fed into ``average_endpoints``.

    """

    def __init__(self, file_name=None):

        try:
            provided_config = yankee_extract_proper_configuration_class(file_name, BravoConfig)
            self.__dict__.update(provided_config.__dict__)
        except Exception:
            if (file_name is not None):
                raise ImportingError("The configuration file could not be properly read. "
                                     "Consider using the factory function.")

            # The name of the detector.
            self.detector_name = {'name':None}

            # Sanitizing the data directory input.
            self.same_file_size_sanitization_config = {'method':None}

            # Renaming file
            self.number_rename_config = {}
            self.set_determine_rename_config = {'set_length':None}
            self.voltpat_rename_config = {'voltage_pattern':None}


            # Preprocessing of beginning/end data for analysis.
            self.median_endpoints_config = {'start_chunk':None, 'end_chunk':None}
            self.median_endpts_persec_config = {'start_chunk':None, 'end_chunk':None, 
                                             'frame_exposure_time':None}
            self.median_endpts_perksec_config = {'start_chunk':None, 'end_chunk':None, 
                                              'frame_exposure_time':None}

    pass


