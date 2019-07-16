"""
    The main objective of the OSCAR line is to create plots and histograms displaying and 
    categorizing different elements of arrays and specifically defined sub-arrays.

    Most of the procedures derived from this module element is derived from 
    https://github.com/tinowells/ifa, as an extension and generalization of said project. 
"""

import astropy as ap
import astropy.io.fits as ap_fits
import astropy.modeling as ap_mod
import copy
import matplotlib as mpl
import matplotlib.cm as mpl_cm
import matplotlib.patches as mpl_patch
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import scipy as sp

from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar


