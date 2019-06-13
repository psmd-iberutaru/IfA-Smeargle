
"""
    The main objective of the ECHO line is to develop and apply masks to array data, tagging
    and removing bad pixel values based on predetermined rules. These masks are stored as boolean
    arrays contained within a Python dictionary.
    
    The codes for each mask determine its order in the overall pipeline and how fundamental it
    is. The lower the code value, the more fundamental it is. 

    All of the actual code documenting the masks can be found in py:module::`~.masks`. This
    file is for executing said masks and applying it properly to the final output.

"""

import astropy as ap
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import masks