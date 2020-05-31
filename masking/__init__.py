"""
This covers all of the masking programs, establishing the filters 
and how they operate. In general, they are divided by how they 
are applied. 
"""


# Common or base functions.
import IfA_Smeargle.masking.base_functions as base

# The masking functions.
from IfA_Smeargle.masking.geometric import *
#from IfA_Smeargle.masking.value import *

# Filtering functions.
from IfA_Smeargle.masking.filters import *