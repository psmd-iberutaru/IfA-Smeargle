
"""
This file contains functions dealing with the loading and handling of fits files and their 
associated header and data arrays.
"""

import astropy as ap
import astropy.io.fits as ap_fits
import copy
import numpy as np



def smeargle_open_fits_file(file_name, extension=0):
    """ A function to ensure proper loading/reading of fits files.

    This function, as its name, opens a fits file. It returns the Astropy HDU file. This function 
    is mostly done to ensure that files are properly closed. It also extracts the needed data and 
    header information from the file.

    Parameters
    ----------
    file_name : string
        This is the path of the file to be read, either relative or absolute.
    extension : int or string (optional)
        The desired extension of the fits file. Defaults to primary structure. 

    Returns
    -------
    hdu_file : HDUList
        The Astropy object representing the fits file.
    hdu_header : Header
        The Astropy header object representing the headers of the given file.
    hdu_data : ndarray
        The Numpy representation of a fits file data.
    """

    with ap_fits.open(file_name) as hdul:
        hdu_file = copy.deepcopy(hdul)
        
        # Just because just in case.
        hdul.close()
        del hdul


    return hdu_file, hdu_file[extension].header, hdu_file[extension].data


def smeargle_extract_subarray(primary_array,x_bounds,y_bounds):
    """ A function to extract a smaller array copy from a larger array.

    Sub-arrays are rather important in the analysis of specific arrays. This function extracts a
    sub-array from a given primary array specified by the x_bounds and y_bounds.

    Parameters
    ----------
    primary_array : ndarray
        This is the data array that is desired to be sliced.
    x_bounds : list-like
        The bounds of the x-axis of a given array. 
    y_bounds : list-like
        The bounds of the y-axis of a given array.

    Returns
    -------
    sub_array : ndarray
        An array containing only data within the xy-bounds provided.
    
    """

    # Be verbose in accepting revered (but valid) bounds.
    x_bounds = np.sort(x_bounds)
    y_bounds = np.sort(y_bounds)

    sub_array = primary_array[y_bounds[0]:y_bounds[-1],x_bounds[0]:x_bounds[1]]

    return np.array(sub_array)