"""
This covers all of the masking programs, establishing the filters 
and how they operate. In general, they are divided by how they 
are applied. 
"""


# Common or base functions.
import ifa_smeargle.masking.base_functions as base

# The masking functions.
from ifa_smeargle.masking.geometric import *
#from ifa_smeargle.masking.value import *

# Filtering functions.
from ifa_smeargle.masking.filters import *