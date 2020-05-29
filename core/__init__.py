"""
This module is dedicated to holding core or common functions to all
other modules related to the IfA-Smeargle library.

In general, these should not be used to manipulate data from 
a pipeline script directly.
"""

from IfA_Smeargle.core import configuration as config
from IfA_Smeargle.core import error as error
from IfA_Smeargle.core import io as io
from IfA_Smeargle.core import magic
from IfA_Smeargle.core import mathematics as math
from IfA_Smeargle.core import modeling as model
from IfA_Smeargle.core import string_formatting as strformat

# This is an alias, the runtime constants are really defined in the 
# main folder, but, it is kind of a core object.
import IfA_Smeargle.runtime as runtime