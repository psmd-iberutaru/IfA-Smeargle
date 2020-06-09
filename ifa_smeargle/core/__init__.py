"""
This module is dedicated to holding core or common functions to all
other modules related to the IfA-Smeargle library.

In general, these should not be used to manipulate data from 
a pipeline script directly.
"""

from ifa_smeargle.core import configuration as config
from ifa_smeargle.core import error as error
from ifa_smeargle.core import io as io
from ifa_smeargle.core import magic
from ifa_smeargle.core import mathematics as math
from ifa_smeargle.core import modeling as model
from ifa_smeargle.core import string_formatting as strformat

# This is an alias, the runtime constants are really defined in the 
# main folder, but, it is kind of a core object.
import ifa_smeargle.runtime as runtime