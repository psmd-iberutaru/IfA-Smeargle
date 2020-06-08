
"""
All testing functions should be available through this module. There
does not seem a reason to break them down further into submodules
within the testing submodule.
"""

# These are tests that are global and apply to the entire library
# rather than a subset of it.
from IfA_Smeargle.testing.test_global import *


# These are numerical based tests, they check for the accuracy of
# computed values through this library.
from IfA_Smeargle.testing.test_numerical_masking import *