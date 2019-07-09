
"""
Defining custom errors because Python does not have all of the needed error 
categories.
"""

import warnings as warn

# Smeargle Bases.
class Smeargle_BaseException(BaseException):
    pass
class Smeargle_Exception(Exception):
    pass


# Errors
class BrokenLogicError(Smeargle_Exception):
    """
    This error is encountered when the program enters in a place it should 
    not be able to. Incorporated mostly for safety; usually not the fault of 
    the user. 
    """
    pass

class ConfigurationError(Smeargle_Exception):
    """
    This error is normally encountered when there are problems with 
    configuration processing (usually because the configuration class is
    incorrect).
    """

class ExportingError(Smeargle_Exception):
    """
    This error is used when the program attempts to export data in some way,
    but is unable to. Named ExportingError to keep with ImportingError.
    """
    pass

class IllogicalProsedureError(Smeargle_Exception):
    """
    This error is thrown when the program would attempt something that does 
    not make scene. This is usually due to issues with configuration errors.
    """

class ImprecisionError(Smeargle_Exception):
    """
    This error is used when there are critical issues with numerical 
    precision because of the volume of data or the very low/high numbers 
    involved. 
    """
    pass

class InputError(Smeargle_Exception):
    """
    This error is used when the user does not input a proper or logical entry. 
    """
    pass

class ImportingError(InputError):
    """
    This error is used when reading configuration files, or other data files
    is not going as it should. Named ImportingError to avoid conflicts with 
    ImportError.
    """
    pass

#####

class IncompleteError(Smeargle_BaseException):
    """
    This used when the code is trying to use a function that is incomplete or
    not usable. 
    """
    def __init__(self):
        self.message = ("TERMINAL: This section of the code is incomplete and likely does not "
                        "work at all. Proceeding is not allowed. ")
    def __str__(self):
        return self.message

class TerminalError(Smeargle_BaseException):
    """
    Something has gone terribly wrong. It is best to contact Sparrow. 
    """
    def __init__(self, message):
        self.message = ("TERMINAL:  " + message)
    def __str__(self):
        return self.message


# Warnings

def smeargle_warning(type, message):
    """ Just a wrapper function around the warning's warn command.

    This wrapper was really only for the logical flow of Sparrow.

    Parameters
    ----------
    type : Warnings Class
        The warning class type.
    message : string
        The message that the warning is to give to the user.

    Returns
    -------
    nothing
    
    """
    warn.warn(message, type, stacklevel=2)
    

# Smeargle base.
class Smeargle_Warning(UserWarning):
    pass


class ConfigurationWarning(Smeargle_Warning):
    """
    This warning is used when there are issues with the configuration class
    and that data is missing. However, the missing data does not warrant an
    exception.
    """

class DepreciationWarning(Smeargle_Warning):
    """
    This warning is used when there are some functions that are used but
    have since been replaced with better functions, or where the previous 
    function is not very stable or integrated with the rest of the functions.
    """
    pass

class ImportingWarning(Smeargle_Warning):
    """
    This warning is used when there are issues loading a file, but it can
    be handled using some assumptions.
    """
    pass 

class ImprecisionWarning(Smeargle_Warning):
    """
    This warning is used when there may be issues with numerical precision 
    because of the volume of data or the very low/high numbers involved. 
    """
    pass

class InputWarning(Smeargle_Warning):
    """
    This warning is used when the user inputs something that is questionable, 
    but not wrong.
    """
    pass

class MaskingWarning(Smeargle_Warning):
    """
    This warning is used when any masking routine (especially in the ECHO 
    line) fails to mask any pixels. It is not a bad thing, but it can be 
    helpful to know.
    """
    pass

class OverwriteWarning(Smeargle_Warning):
    """
    This warning is used to warn the user that a file has been overwritten,
    most likely because of conflicting file names.
    """
    pass


class ReductionWarning(Smeargle_Warning):
    """
    This warning is used when normally unusual parameters are used for data 
    reduction. The user is trusted in their procedures.
    """
    pass


class TimeWarning(Smeargle_Warning):
    """
    This warning is used when any method called may take a long time to 
    compute or execute. This allows the user to stop and change if desired. 
    """
    pass