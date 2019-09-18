
"""
Defining custom errors because Python does not have all of the needed error 
categories.
"""

import contextlib
import warnings as warn

# Smeargle Bases.
class Smeargle_BaseException(BaseException):
    pass
class Smeargle_Exception(Exception):
    pass


##############################################################################
##############################################################################
# Errors
##############################################################################
##############################################################################

class ConfigurationError(Smeargle_Exception):
    """
    This error is normally encountered when there are problems with 
    configuration processing (usually because the configuration class is
    incorrect).
    """

class DataError(Smeargle_Exception):
    """
    This error is used when there is an issue with the fundamental data that
    this program or module cannot fix. The user should be able to figure out 
    what is the problem.
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
    involved. It is also just used when data may be chaotic.   
    """
    pass

class InputError(Smeargle_Exception):
    """
    This error is used when the user does not input a proper or logical entry. 
    """
    pass

class ImportingError(Smeargle_Exception):
    """
    This error is used when reading configuration files, or other data files
    is not going as it should. Named ImportingError to avoid conflicts with 
    ImportError.
    """
    pass

class MaskingError(Smeargle_Exception):
    """
    This error is used when a mask cannot be applied or where there are 
    fatal issues with calculating the mask.
    """
    pass

class ModelingError(Smeargle_Exception):
    """
    This error is used when there are issues with applying or fitting models
    to a particular set of data. May be used hand-in-hand with DataError.
    """

#####
# These are the base exceptions; proper programing protocol dictates that 
# Python try-except statements should not catch these. As such, they are 
# reserved for very critical problems within the code itself (rarely should
# the fault be the user's).

class BrokenLogicError(Smeargle_BaseException):
    """
    This error is encountered when the program enters in a place it should 
    not be able to. Incorporated mostly for safety; usually not the fault of 
    the user. 
    """
    def __init__(self, message=None):
        if (isinstance(message, str)):
            self.message = ("TERMINAL: " + message
                            + "\n >> Please contact maintainers or Sparrow to resolve this issue.")
        else:
            self.message = ("TERMINAL: Something is not right with the code's logic. Please "
                            "contact maintainers or Sparrow to resolve this issue.")

    pass

class IncompleteError(Smeargle_BaseException):
    """
    This used when the code is trying to use a function that is incomplete or
    not usable. 
    """
    def __init__(self):
        self.message = ("TERMINAL: This section of the code is incomplete and likely does not "
                        "work at all. Proceeding is not allowed. Send the call stack to "
                        "maintainers or Sparrow to resolve this issue.")
    def __str__(self):
        return self.message

class TerminalError(Smeargle_BaseException):
    """
    Something has gone terribly wrong. It is best to contact Sparrow. 
    """
    def __init__(self, message=None):
        if (message is None):
            self.message = "TERMINAL: A general TERMINAL error has been raised."
        elif (isinstance(message, str)):
            self.message = ("TERMINAL: " + message)
        else:
            raise TerminalError("The message for a TERMINAL error must be a string.")
    
    def __str__(self):
        return self.message

##############################################################################
##############################################################################
# Warnings
##############################################################################
##############################################################################

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
    return None
    

# Smeargle base.
class Smeargle_Warning(UserWarning):
    pass


class ConfigurationWarning(Smeargle_Warning):
    """
    This warning is used when there are issues with the configuration class
    and that data is missing. However, the missing data does not warrant an
    exception.
    """

class DataWarning(Smeargle_Warning):
    """
    This warning is used when there is an issue with the fundamental data that
    this program or module cannot fix but can still work around. The user 
    should be able to figure out what is the problem.
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

class MagicWarning(Smeargle_Warning):
    """
    This warning is used when any routine would utilize magic/hard-coded 
    values for the purposes of any process where said numbers are magic. This
    is mostly as a programming warning to the user that behavior with magic
    numbers may not always be expected or logical.
    """

class MaskingWarning(Smeargle_Warning):
    """
    This warning is used when any masking routine (especially in the ECHO 
    line) fails to mask any pixels. It is not a bad thing, but it can be 
    helpful to know. 
    """
    pass

class MemoryWarning(Smeargle_Warning):
    """
    This warning is used to warn the user that the procedures that follow 
    would require a lot of memory RAM. If instead it would produce a large 
    file(s), StorageWarning should be used.
    """
    pass

class OutputWarning(Smeargle_Warning):
    """
    This warning is used to warn the user about outputs and some things that
    may be helpful to know about them. Such outputs are generally writing 
    file outputs.
    """

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

class StorageWarning(Smeargle_Warning):
    """
    This warning is used when the large file(s) would be written to the hard
    drive. If instead a lot of RAM would be used, it is better to use 
    MemoryWarning.
    """

class TimeWarning(Smeargle_Warning):
    """
    This warning is used when any method called may take a long time to 
    compute or execute. This allows the user to stop and change if desired. 
    """
    pass


##############################################################################
##############################################################################
# Informational Messages
##############################################################################
##############################################################################

def smeargle_info(message):
    """
    This is a wrapper function to print helpful information.
   
    Printing information as the function(s) go on is very helpful. However,
    using the normal print function doesn't allow for some level of 
    customization and ease of handling. Hence, function for uniformity.

    Parameters
    ----------
    message : string
        The informational message that is to be printed. 

    Returns
    -------
    nothing
    """
    
    # Test if info messages should not be printed given their
    if (smeargle_info._silent_mode):
        # Messages should not be printed in general.
        pass
    else:
        print("IFAS Info: " + message)
    return None

# This is the default and will set the silent mode parameter for informational
# printing, but it ensures not to override anything that may already exist.
if (hasattr(smeargle_info, '_silent_mode')):
    pass
else:
    smeargle_info._silent_mode = False


# The context manager is mostly for stylistic purposes. Given that debug 
# functional printing is more often than not more than one line. 
@contextlib.contextmanager
def smeargle_debug_block():
    """ This is a wrapper function for encasing debugging code. 

    The execution of code within a debug block is used to contain easily 
    printed debug information. Debug messages should use the debug function
    :func:`smeargle_debug_message`
    """

    if (smeargle_debug_block._silent_mode):
        pass
    else:
        yield
    return None
# This is the default and will set the silent mode parameter for debug
# printing, but it ensures not to override anything that may already exist.
if (hasattr(smeargle_debug_block, '_silent_mode')):
    pass
else:
    smeargle_debug_block._silent_mode = True

# The message form of the debug information. 
def smeargle_debug_message(message):
    """ This is a wrapper function for the printing of debug messages. 

    Given the nature of debug messages, it should be clear that it is a debug
    message, and should also have the proper silencing capabilities.

    Parameters
    ----------
    message : string
        The message that is to be sent as the debug message.
    
    Returns
    -------
    nothing    
    """

    # Test if info messages should not be printed given their
    if (smeargle_debug_message._silent_mode):
        # Messages should not be printed in general.
        pass
    else:
        print("IFAS Debug: " + message)
    return None
# This is the default and will set the silent mode parameter for debug
# printing, but it ensures not to override anything that may already exist.
if (hasattr(smeargle_debug_message, '_silent_mode')):
    pass
else:
    smeargle_debug_message._silent_mode = True


##############################################################################
##############################################################################
# Enabling/Silencing Context Managers 
##############################################################################
##############################################################################

# To silence a specific type of warning. This is a wrapper function.
@contextlib.contextmanager
def smeargle_silence_specific_warnings(silenced_warning_type):
    """ This context manager silences all warnings of a given type. Depending
    on what was inputed.
    
    Parameters
    ----------
    silenced_warning_type : WarningType
        The warning that should be silenced.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=silenced_warning_type)
        yield

    return None

# To silence Smeargle based warnings
@contextlib.contextmanager
def smeargle_silence_ifas_warnings():
    """ This context manager silences all Smeargle based warnings, all other 
    warnings are still valid.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=Smeargle_Warning)
        yield

    return None

# To silence non-Smeargle based warnings
@contextlib.contextmanager
def smeargle_silence_nonifas_warnings():
    """ This context manager silences all non-Smeargle based warnings, all 
    other warnings are still valid.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore")
        warn.simplefilter("default", category=Smeargle_Warning)
        yield

    return None

# To silence all warnings
@contextlib.contextmanager
def smeargle_silence_all_warnings():
    """ This context manager silences all warnings. Warnings should not be 
    printed.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore")
        yield

    return None

# To silence all informational messages.
@contextlib.contextmanager
def smeargle_silence_info_message():
    """ This context manager silences all informational messages that may
    be printed.
    """
    # Trigger silent mode.
    smeargle_info._silent_mode = True

    yield

    # Release silent mode, allowing for future messages to be implemented.
    smeargle_info._silent_mode = False
    return None

# To enable debug messages.
@contextlib.contextmanager
def smeargle_enable_debug():
    """ This context manager turns all debug messages on for the duration of 
    the context. 
    """
    # Turn on debugging (releasing from silence)
    smeargle_debug_block._silent_mode = False
    smeargle_debug_message._silent_mode = False

    yield
    
    # Disable by silencing. 
    smeargle_debug_block._silent_mode = True
    smeargle_debug_message._silent_mode = True

    return None

# To disable debug messages.
@contextlib.contextmanager
def smeargle_disable_debug():
    """ This context manager turns all debug messages off for the duration of 
    the context. Given that debug messages are generally off in the first 
    place, usage may be rare.
    """
    # Disable by silencing. 
    smeargle_debug_block._silent_mode = True
    smeargle_debug_message._silent_mode = True

    yield
    
    # Disable by silencing. 
    smeargle_debug_block._silent_mode = True
    smeargle_debug_message._silent_mode = True

    return None

# To silence everything, warnings, informational, and debug messages.
@contextlib.contextmanager
def smeargle_absolute_silence():
    """This context manager silences any and all messages, it basically 
    it is wrapper around all other general Smeargle context managers (even 
    if there is some overlap).
    """
    with smeargle_silence_ifas_warnings(), \
         smeargle_silence_all_warnings(),  \
         smeargle_silence_info_message(),  \
         smeargle_disable_debug():
            yield 