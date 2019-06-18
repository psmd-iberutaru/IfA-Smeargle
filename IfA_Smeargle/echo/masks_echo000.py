"""
This file contains the code to calculate which pixel should be masked. Note the masking code
in this file is 000; this file only contains ECHO-000 class masks.
"""

import astropy as ap
import numpy as np
import scipy as sp
import warnings as warn

from . import echo_main
from . import masks_echo100, masks_echo200, masks_echo300 as masks