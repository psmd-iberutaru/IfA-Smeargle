
"""
All testing functions should be available through this module. There
does not seem a reason to break them down further into submodules
within the testing submodule.
"""
# Common functions.
import ifa_smeargle.testing.base_functions as base

# These are tests that are global and apply to the entire library
# rather than a subset of it.
from ifa_smeargle.testing.test_global import *


# These are numerical based tests, they check for the accuracy of
# computed values through this library.
from ifa_smeargle.testing.test_numerical_masking import *
from ifa_smeargle.testing.test_numerical_filters import *