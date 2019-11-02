
"""
These are some functions for the ECHO line that are helpful.
"""

import astropy as ap
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import scipy as sp

from IfA_Smeargle.meta import *


def echo_numpy_masked_array(data_array, synthesized_mask,
                            masking_dictionary=None):
    """ This function makes a Numpy masked array; a nice built in class for 
    this line.

    The Numpy Masked Array class works very well with masking data values in 
    a given array. It is only natural to use such functionality. This is 
    really a wrapper function for ease of usage with familiarity of 
    IfA-Smeargle's structures.

    Parameters
    ----------
    data_array : ndarray
        The data that is to have its mask made.
    synthesized_mask : ndarray
        The mask that should be applied to the data, it is expected that 
        this is post-synthesis.
    masking_dictionary : dictionary (optional)
        The masking dictionary pre-synthesis. If it is not None, 
        ``synthesized_mask`` is completely ignored in favor of this parameter.
    """

    if (masking_dictionary is not None):
        synthesized_mask = echo_synthesize_mask_dictionary(masking_dictionary)

    # Making the masked array.
    np_masked_data = np_ma.array(data_array, mask=synthesized_mask)

    return np_masked_data


def echo_synthesize_mask_dictionary(masking_dictionary):
    """ This function takes a masking dictionary and returns it with a 
    final overall mask.

    The masking dictionary is made solely because it is helpful to preserve 
    the information as to which mask applied to which pixel. However, in 
    actual visualization, it is not really needed. 
    
    This function makes a deep copy of the input to ensure it is not 
    damaged. The final synthesized mask does not have information about 
    each individual mask.

    Parameters
    ----------
    masking_dictionary : dictionary
        A masking dictionary made by the procedures of the ECHO line.

    Returns
    -------
    synthesized_mask : ndarray
        A boolean array of the finalized mask properties.
    """

    all_masks = np.array(list(masking_dictionary.values()))
    synthesized_mask = np.any(all_masks,axis=0)

    return synthesized_mask


def echo_functioned_mask_returning(pixel_mask, masking_dictionary, filter_name, return_mask_only):
    """ This function is a single implementation for returning masks.

    Because it is an option for the user to return the mask itself, writing 
    the logic for each of the masks will get really old.

    Parameters
    ----------
    pixel_mask : ndarray
        This is the pixel mask, it is not changed, only where it goes.
    masking_dictionary : dictionary
        This is the mask dictionary provided by the user (or blank by default)
    filter_name : string
        This is the name of the filter that is being applied; should be same 
        as the dictionary entry for this filter.
    return_mask_only : boolean
        The decision on if or if not the mask or the dictionary should be 
        returned.

    Returns
    -------
    returning_object : ndarray or dictionary
        The object that is to be returned. It is either the mask or the 
        dictionary based on the boolean value.
    
    """

    # Warn if the mask that would be returned is empty.
    if (not np.any(pixel_mask)):
        smeargle_warning(MaskingWarning,
                         ("The masking routine < {msk_rou} > did not mask any pixels."
                          .format(msk_rou=filter_name)))

    # The object that will be returned.
    returning_object = None

    # Switch between the mask itself or the dictionary of the masks as need
    # be.
    if (return_mask_only):
        returning_object = pixel_mask
    else:
        if (masking_dictionary == None):
            masking_dictionary = {}

        masking_dictionary[filter_name] = pixel_mask
        returning_object = masking_dictionary

    return returning_object


def echo_sort_masking_dictionary(mask_dictionary):
    """ This function just sorts a dictionary by its key.
    
    As the masking dictionary is expected to be in order by its keys, this 
    is sort of needed. It is not too efficient, and it can be disabled. 

    Parameters
    ----------
    mask_dictionary : dictionary
        The unsorted mask dictionary.

    Returns
    -------
    sorted_mask_dictionary : dictionary
        The mask dictionary that is sorted by the ECHO code.
    """

    sorted_mask_dictionary = {}
    sorted_keys = sorted(mask_dictionary)

    for keydex in sorted_keys:
        sorted_mask_dictionary[keydex] = copy.deepcopy(mask_dictionary[keydex])

    return sorted_mask_dictionary


