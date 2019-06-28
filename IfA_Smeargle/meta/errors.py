
"""
Defining custom errors because Python does not have all of the needed error 
categories.
"""

import warnings as warn

# Smeargle Base.
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

class IllogicalProsedure(Smeargle_Exception):
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
    

class Smeargle_Warning(UserWarning):
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

class TimeWarning(Smeargle_Warning):
    """
    This warning is used when any method called may take a long time to 
    compute or execute. This allows the user to stop and change if desired. 
    """
    pass