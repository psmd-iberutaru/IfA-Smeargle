

"""
These are functions common to the reformatting module.
"""

import IfA_Smeargle.core as core

def format_slice_appending_name(reference_frame, averaging_frame):
    """ The formatting for the string alignment for slices. """
    # This is the delimiter string.
    RENAMING_DELIMITER = str(core.runtime.extract_runtime_configuration(
        config_key='RENAMING_DELIMITER'))

    slice_string = ''.join(['_slice', RENAMING_DELIMITER,
                            str(reference_frame[0]), ',', 
                            str(reference_frame[-1]), '-', 
                            str(averaging_frame[0]), ',', 
                            str(averaging_frame[-1])])
    return slice_string