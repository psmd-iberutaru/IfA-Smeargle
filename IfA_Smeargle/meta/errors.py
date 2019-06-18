
"""
Defining custom errors because Python does not have all of the needed error categories.
"""

# Smeargle Base.
class Smeargle_Exception(Exception):
    pass


# Errors
class BrokenLogicError(Smeargle_Exception):
    """
    This error is encountered when the program enters in a place it should not be able to.
    Incorporated mostly for safety; usually not the fault of the user. 
    """
    pass

class InputError(Smeargle_Exception):
    """
    This error is used when the user does not input a proper or logical entry. 
    """
    pass




# Warnings