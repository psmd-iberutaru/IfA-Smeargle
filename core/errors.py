
"""
Defining custom errors because Python does not have all of the 
needed error categories.
"""

import contextlib
import copy
import logging as log
import warnings as warn

import IfA_Smeargle.core as core

# Ifas Bases.
class Ifas_BaseException(BaseException):
    pass
class Ifas_Exception(Exception):
    pass


#####################################################################
#####################################################################
# Errors
#####################################################################
#####################################################################

class ConfigurationError(Ifas_Exception):
    """
    This error is normally encountered when there are problems with 
    configuration processing (usually because the configuration 
    class is incorrect).
    """
    
class DataError(Ifas_Exception):
    """
    This error is used when there is an issue with the fundamental 
    data that this program or module cannot fix. The user should be 
    able to figure out what is the problem.
    """

class ExportingError(Ifas_Exception):
    """
    This error is used when the program attempts to export data in 
    some way, but is unable to. Named ExportingError to keep with 
    ImportingError.
    """
    pass

class IllogicalProsedureError(Ifas_Exception):
    """
    This error is thrown when the program would attempt something 
    that does not make scene. This is usually due to issues with 
    configuration errors.
    """

class ImprecisionError(Ifas_Exception):
    """
    This error is used when there are critical issues with numerical 
    precision because of the volume of data or the very low/high 
    numbers involved. It is also just used when data may be chaotic.   
    """
    pass

class InputError(Ifas_Exception):
    """
    This error is used when the user does not input a proper or 
    logical entry. 
    """
    pass

class ImportingError(Ifas_Exception):
    """
    This error is used when reading configuration files, or other 
    data files is not going as it should. Named ImportingError to 
    avoid conflicts with ImportError.
    """
    pass

class MaskingError(Ifas_Exception):
    """
    This error is used when a mask cannot be applied or where there 
    are fatal issues with calculating the mask.
    """
    pass

class MagicError(Ifas_Exception):
    """
    This error is used when any routine would utilize 
    magic/hard-coded values for the purposes of any process where 
    said numbers are magic. This is mostly as a programming warning 
    to the user that behavior with magic numbers may not always be 
    expected or logical. This error form is used for higher warning 
    levels, and if the user wants an interrupt when upgrading.
    """

class ModelingError(Ifas_Exception):
    """
    This error is used when there are issues with applying or 
    fitting models to a particular set of data. May be used 
    hand-in-hand with DataError.
    """

#####
# These are the base exceptions; proper programing protocol dictates 
# that Python try-except statements should not catch these. As such, 
# they are reserved for very critical problems within the code 
# itself (it rarely should be the fault of the user's).

class AssumptionError(Ifas_BaseException):
    """
    This error is reserved for instances where something 
    unexpected has occurred because of a flaw in the understanding 
    of assumptions about Python or module functions.
    """
    def __init__(self, message=None):
        if (isinstance(message, str)):
            self.message = ("TERMINAL: " + message
                            + ("\n >> Please contact maintainers or "
                               "Sparrow to resolve this issue."))
        else:
            self.message = ("TERMINAL: An erroneous result has transpired "
                            "because of an incorrect assumption about how "
                            "Python or other Python modules or functions "
                            "work. Please contact maintainers or Sparrow "
                            "to resolve this issue.")

    pass

class BrokenLogicError(Ifas_BaseException):
    """
    This error is encountered when the program enters in a place it 
    should not be able to. Incorporated mostly for safety; usually 
    not the fault of the user. 
    """
    def __init__(self, message=None):
        if (isinstance(message, str)):
            self.message = ("TERMINAL: " + message
                            + ("\n >> Please contact maintainers or Sparrow "
                               "to resolve this issue."))
        else:
            self.message = ("TERMINAL: Something is not right with the "
                            "code's logic. Please contact maintainers or "
                            "Sparrow to resolve this issue.")

    pass

class DeprecatedError(Ifas_BaseException):
    """
    This is used when the code should be using a different 
    equivalent function. This is mostly used for cases where a 
    warning has already been issued, or to clean up the core 
    sections of the code during testing. 
    """

    def __init__(self, message=None):
        if (isinstance(message, str)):
            self.message = ("TERMINAL: " + message
                            + ("\n >> Please contact maintainers or Sparrow "
                               "to resolve this issue if need be."))
        else:
            self.message = ("TERMINAL: This function is terminally "
                            "deprecated. There exists a different and "
                            "equivalent function. Use that function. Please "
                            "contact maintainers or Sparrow to resolve "
                            "this issue.")
    pass

class DevelopmentError(Ifas_BaseException):
    """
    This is used when the code is improperly written as a result of
    development solely by one or many parties. An error here usually
    is because some assumptions on development has been imposed that
    may have been forgotten about.
    """
    def __init__(self, message=None):
        if (isinstance(message, str)):
            self.message = ("TERMINAL: " + message
                            + ("\n >> Please contact maintainers or Sparrow "
                               "to resolve this issue if need be."))
        else:
            self.message = ("TERMINAL: There seems to be an error in the "
                            "development of this code script or library. "
                            "Please contact maintainers or Sparrow to "
                            "resolve this issue.")
    pass

class IncompleteError(Ifas_BaseException):
    """
    This used when the code is trying to use a function that is 
    incomplete or not usable. 
    """
    def __init__(self):
        self.message = ("TERMINAL: This section of the code is incomplete "
                        "and likely does not work at all. Proceeding is "
                        "not allowed. Please contact maintainers "
                        "or Sparrow to resolve this issue.")
    def __str__(self):
        return self.message

class TerminalError(Ifas_BaseException):
    """
    This is used when something has gone terribly wrong. It is best 
    to contact the maintainers or Sparrow. 
    """
    def __init__(self, message=None):
        if (message is None):
            self.message = ("TERMINAL: A general TERMINAL error has "
                            "been raised.")
        elif (isinstance(message, str)):
            self.message = ("TERMINAL: " + message)
        else:
            raise InputError("The message for a TERMINAL error must "
                             "be a string.")
            raise TerminalError("The message for a TERMINAL error must "
                                "be a string. The previous InputError was "
                                "likely caught by a try-except block.")
    
    def __str__(self):
        return self.message

#####################################################################
#####################################################################
# Warnings and other Non-Exceptions
#####################################################################
#####################################################################

def ifas_error(type, message):
    """ This is a wrapper around the logging's error command. 
    However, it does not raise an error. Instead, an error may be 
    sent to and it will be converted into a proper warning.

    Parameters
    ----------
    type : ExecptionsClass
        The error that could be raised, but it is more manageable as 
        a logged error.
    message : string
        The message that the error is to give.

    Returns
    -------
    None
    """
    # Ensure that the type really is an error.
    if (not issubclass(type, Exception)):
        raise AssumptionError("It is assumed that logging errors should "
                              "be raise-able. This type class is not a "
                              "raise-able exception.")
    try:
        error_name = str(type.__name__)
    except Exception:
        error_name = 'UserError'
    finally:
        error_message = ''.join(['[', error_name, ']', '  ', message])
    # Log the error.
    log.error(error_message)
    # ...and inform.
    warn.warn(error_message, ErrorWarning, stacklevel=2)



def ifas_warning(type, message):
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
    None
    """
    warn.warn(message, type, stacklevel=2)
    # Also add it into the logger, but, add information to 
    # indicate that is was a raised warning.
    ifas_log_warning(type=type, message=message)

    return None
    
def ifas_log_warning(type, message):
    """ Just a wrapper function around logging's built-in warn. 
    This is to only log a warning but not to display it as a 
    standard warning.

    Parameters
    ----------
    type : Warnings Class
        The warning class type.
    message : string
        The message that the warning is to give to the user.
    """
    try:
        warning_name = str(type.__name__)
    except Exception:
        warning_name = 'UserWarning'
    finally:
        warning_message = ''.join(['[', warning_name, ']', '  ', message])
    # Log the warning.
    log.warning(warning_message)

# Ifas base.
class Ifas_Warning(UserWarning):
    pass


class ConfigurationWarning(Ifas_Warning):
    """
    This warning is used when there are issues with the 
    configuration class and that data is missing. However, the 
    missing data does not warrant an exception.
    """

class DataWarning(Ifas_Warning):
    """
    This warning is used when there is an issue with the fundamental 
    data that this program or module cannot fix but can still work 
    around. The user should be able to figure out what is the problem.
    """

class DeprecatedWarning(Ifas_Warning):
    """
    This warning is used when there are some functions that are 
    used but have since been replaced with better functions, or 
    where the previous function is not very stable or integrated 
    with the rest of the functions.
    """
    pass

class ExportingWarning(Ifas_Warning):
    """
    This warning is used to warn the user about exports and some 
    things that may be helpful to know about them. Such exports are 
    generally writing files to disk.
    """

class ErrorWarning(Ifas_Warning):
    """
    This warning is to inform that there was an error that was 
    thrown as a warning (either as a critical warning log or 
    something else.
    """

class ImportingWarning(Ifas_Warning):
    """
    This warning is used when there are issues loading a file, but 
    it can be handled using some assumptions.
    """
    pass 

class ImprecisionWarning(Ifas_Warning):
    """
    This warning is used when there may be issues with numerical 
    precision because of the volume of data or the very low/high 
    numbers involved. 
    """
    pass

class InputWarning(Ifas_Warning):
    """
    This warning is used when the user inputs something that is 
    questionable, but not wrong.
    """
    pass

class MagicWarning(Ifas_Warning):
    """
    This warning is used when any routine would utilize 
    magic/hard-coded values for the purposes of any process where 
    said numbers are magic. This is mostly as a programming 
    warning to the user that behavior with magic numbers may not 
    always be expected or logical.
    """

class MaskingWarning(Ifas_Warning):
    """
    This warning is used when any masking or filtering routine 
    (especially in the masking and filtering scripts) fails to 
    mask any pixels or something else is amiss. It is not a bad 
    thing, but it can be helpful to know. 
    """
    pass

class MemoryWarning(Ifas_Warning):
    """
    This warning is used to warn the user that the procedures that 
    follow would require a lot of memory RAM. If instead it would 
    produce a large file(s), StorageWarning should be used.
    """
    pass

class OverwriteWarning(Ifas_Warning):
    """
    This warning is used to warn the user that a file has been 
    overwritten, most likely because of conflicting file names.
    """
    pass


class ReductionWarning(Ifas_Warning):
    """
    This warning is used when normally unusual parameters are 
    used for data reduction. The user is trusted in their procedures.
    """
    pass

class StorageWarning(Ifas_Warning):
    """
    This warning is used when the large file(s) would be written 
    to the hard drive. If instead a lot of RAM would be used, it is 
    better to use MemoryWarning.
    """

class TimeWarning(Ifas_Warning):
    """
    This warning is used when any method called may take a long time 
    to compute or execute. This allows the user to stop and change 
    if desired. 
    """
    pass


####################################################################
####################################################################
# Informational Logging Messages
####################################################################
####################################################################

def ifas_info(message, console_print=None):
    """
    This is a wrapper function to print helpful information.
   
    Printing information as the function(s) go on is very helpful. 
    However, using the normal print function doesn't allow for some 
    level of customization and ease of handling. Hence, function 
    for uniformity.

    Parameters
    ----------
    message : string
        The informational message that is to be printed. 
    console_print : boolean (optional)
        This ensures that the info message is always printed 
        regardless of the logging level set by the logging utility.

    Returns
    -------
    nothing
    """
    # Use the default console print parameter if not specified.
    if (console_print is not None):
        console_print = bool(console_print)
    else:
        console_print = core.runtime.extract_runtime_configuration(
            config_key='CONSOLE_LOG')
    
    # Test if info messages should not be printed given their
    if (ifas_info._silent_mode):
        # Messages should not be printed in general.
        pass
    else:
        # Just a little white space so it is not so cluttered.
        log.info(message)
        if (console_print):
            print("IFAS Info: " + message)
    return None

# This is the default and will set the silent mode parameter for 
# informational printing, but it ensures not to override anything 
# that may already exist.
if (hasattr(ifas_info, '_silent_mode')):
    pass
else:
    ifas_info._silent_mode = False


# The context manager is mostly for stylistic purposes. Given that 
# debug functional printing is more often than not more than one line. 
@contextlib.contextmanager
def ifas_debug_block():
    """ This is a wrapper function for encasing debugging code. 

    The execution of code within a debug block is used to contain 
    easily printed debug information. Debug messages should use the 
    debug function :func:`ifas_debug`
    """

    if (ifas_debug_block._silent_mode):
        pass
    else:
        yield
    return None
# This is the default and will set the silent mode parameter for debug
# printing, but it ensures not to override anything that may already 
# exist.
if (hasattr(ifas_debug_block, '_silent_mode')):
    pass
else:
    ifas_debug_block._silent_mode = True

# The message form of the debug information. 
def ifas_debug(message, console_print=False):
    """ This is a wrapper function for the printing of debug messages. 

    Given the nature of debug messages, it should be clear that it 
    is a debug message, and should also have the proper silencing 
    capabilities.

    Parameters
    ----------
    message : string
        The message that is to be sent as the debug message.
    console_print : boolean (optional)
        This ensures that the info message is always printed 
        regardless of the logging level set by the logging utility. 
        Default is False.
    
    Returns
    -------
    nothing    
    """

    # Test if info messages should not be printed given their
    if (ifas_debug._silent_mode):
        # Messages should not be printed in general.
        pass
    else:
        log.debug(message)
        if (console_print):
            print("IFAS Debug: " + message)
    return None
# This is the default and will set the silent mode parameter for 
# debug printing, but it ensures not to override anything that may 
# already exist.
if (hasattr(ifas_debug, '_silent_mode')):
    pass
else:
    ifas_debug._silent_mode = True


####################################################################
####################################################################
# Enabling/Silencing Context Managers
####################################################################
####################################################################

# To silence a specific type of warning. This is a wrapper function.
@contextlib.contextmanager
def ifas_silence_specific_warnings(silenced_warning_type):
    """ This context manager silences all warnings of a given type. 
    Depending on what was inputed.
    
    Parameters
    ----------
    silenced_warning_type : WarningType
        The warning that should be silenced.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=silenced_warning_type)
        yield

    return None

# To silence Ifas based warnings
@contextlib.contextmanager
def ifas_silence_ifas_warnings():
    """ This context manager silences all Ifas based warnings, all 
    other warnings are still valid.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=Ifas_Warning)
        yield

    return None

# To silence non-Ifas based warnings
@contextlib.contextmanager
def ifas_silence_nonifas_warnings():
    """ This context manager silences all non-Ifas based warnings, 
    all other warnings are still valid.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore")
        warn.simplefilter("default", category=Ifas_Warning)
        yield

    return None

# To silence all warnings
@contextlib.contextmanager
def ifas_silence_all_warnings():
    """ This context manager silences all warnings. Warnings should 
    not be printed.
    """
    with warn.catch_warnings():
        warn.simplefilter("ignore")
        yield

    return None

# To silence all informational messages.
@contextlib.contextmanager
def ifas_silence_info_message():
    """ This context manager silences all informational messages 
    that may be printed.
    """
    # Store previous state.
    previous_state = copy.deepcopy(ifas_info._silent_mode)

    # Trigger silent mode.
    ifas_info._silent_mode = True

    yield

    # Release silent mode, return to default.
    ifas_info._silent_mode = copy.deepcopy(previous_state)
    return None

# To enable debug messages.
@contextlib.contextmanager
def ifas_enable_debug():
    """ This context manager turns all debug messages on for the 
    duration of the context. 
    """
    # Store previous state.
    block_previous_state = copy.deepcopy(ifas_debug_block._silent_mode)
    message_previous_state = copy.deepcopy(ifas_debug._silent_mode)

    # Turn on debugging (releasing from silence)
    ifas_debug_block._silent_mode = False
    ifas_debug._silent_mode = False

    yield
    
    # Release to previous state.
    ifas_debug_block._silent_mode = copy.deepcopy(block_previous_state)
    ifas_debug._silent_mode = copy.deepcopy(message_previous_state)

    return None

# To disable debug messages.
@contextlib.contextmanager
def ifas_disable_debug():
    """ This context manager turns all debug messages off for the 
    duration of the context. Given that debug messages are generally 
    off in the first place, usage may be rare.
    """
    # Store previous state.
    block_previous_state = copy.deepcopy(ifas_debug_block._silent_mode)
    message_previous_state = copy.deepcopy(ifas_debug._silent_mode)

    # Disable by silencing. 
    ifas_debug_block._silent_mode = True
    ifas_debug._silent_mode = True

    yield
    
    # Release to previous state.
    ifas_debug_block._silent_mode = copy.deepcopy(block_previous_state)
    ifas_debug._silent_mode = copy.deepcopy(message_previous_state)

    return None

# To silence everything, warnings, informational, and debug messages.
@contextlib.contextmanager
def ifas_absolute_silence():
    """This context manager silences any and all messages, it 
    basically is a wrapper around all other general Ifas context 
    managers (even if there is some overlap).
    """
    with ifas_silence_ifas_warnings(), \
         ifas_silence_all_warnings(),  \
         ifas_silence_info_message(),  \
         ifas_disable_debug():
            yield 

    return None
