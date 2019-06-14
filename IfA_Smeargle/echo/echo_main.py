
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
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

import masks_echo000, masks_echo100, masks_echo200, masks_echo300 as masks


def _sort_masking_dictionary(mask_dictionary):
    """ This function just sorts a dictionary by its key.
    
    As the dictionary is expected to be in order by its keys, this is sort of needed. It is
    not too efficient, and it can be disabled. 

    Parameters
    ----------
    mask_dictionary : dictionary
        The unsorted mask dictionary.

    Returns
    -------
    sorted_mask_dictionary : dictionary
        The mask dictionary that is sorted by the code.
    """

    sorted_mask_dictionary = {}
    sorted_keys = sorted(mask_dictionary)

    for keydex in sorted_keys:
        sorted_mask_dictionary[keydex] = copy.deepcopy(mask_dictionary[keydex])

    return sorted_mask_dictionary