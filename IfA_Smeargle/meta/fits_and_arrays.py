
"""
This file contains functions dealing with the loading and handling of fits files and their 
associated header and data arrays.
"""

import astropy as ap
import astropy.io.fits as ap_fits
import copy
import numpy as np
import numpy.ma as np_ma
import os

from IfA_Smeargle.meta import *

def smeargle_open_fits_file(file_name, extension=0):
    """ A function to ensure proper loading/reading of fits files.

    This function, as its name, opens a fits file. It returns the Astropy HDU 
    file. This function is mostly done to ensure that files are properly 
    closed. It also extracts the needed data and header information from the 
    file.

    Parameters
    ---------- 
    file_name : string
        This is the path of the file to be read, either relative or absolute.
    extension : int or string (optional)
        The desired extension of the fits file. Defaults to primary structure. 

    Returns
    -------
    hdu_file : HDULists
        The Astropy object representing the fits file.
    hdu_header : Header
        The Astropy header object representing the headers of the given file.
    hdu_data : ndarray
        The Numpy representation of a fits file data.
    """

    with ap_fits.open(file_name) as hdul:
        hdul_file = copy.deepcopy(hdul)
        
        # Just because just in case.
        hdul.close()
        del hdul

    # Read from the extension
    hdu_header = hdul_file[extension].header
    hdu_data = hdul_file[extension].data

    # Check if there is an IfA-Smeargle mask, if so, mutate data to a masked
    # array.
    try:
        data_mask = hdul_file['IFASMASK'].data
        # Because fits files do not handle boolean arrays, convert from the 
        # int 1/0 array in the file.
        data_mask = np.array(np.where(data_mask >= 1, True, False), dtype=bool)

    except KeyError:
        data_mask = None
    finally:
        if (data_mask is not None):
            # Inform that a mask has been found and is going to be used.
            smeargle_warning(InputWarning,("The fits file contains an <IFASMASK> extension, "
                                           "a pixel mask created by this program. It will be "
                                           "applied to the data. The output data will be a "
                                           "Numpy Masked Array."))
            # Apply the mask.
            hdu_data = np_ma.array(hdu_data, mask=data_mask)
        else:
            hdu_data = np.array(hdu_data)

    # Finally return
    return hdul_file, hdu_header, hdu_data


def smeargle_write_fits_file(file_name, hdu_header, hdu_data,
                             hdu_object=None, overwrite=True):
    """ A function to ensure proper writing of fits files.

    This function writes fits files given the data and header file. The 
    file name should be a complete path and must also include the file name.



    Parameters
    ----------
    file_name : string
        This is the path of the file to be written, either relative or 
        absolute.
    hdu_header : Header
        The Astropy header object representing the headers of the given file.
    hdu_data : ndarray
        The Numpy representation of a fits file data.
    hdu_object : Astropy HDUList (optional)
        An astropy HDUList object, if provided, this object takes priority 
        to be written, the rest are ignored.
    overwrite : boolean
        If ``True``, if there exists a file of the same name, overwrite.

    Returns
    -------
    hdul_file : Astropy HDUList
        The file object that was written to disk. If ``hdu_object`` was 
        provided, it is returned untouched.
    """

    # Check if the file name has a fits extension.
    if (file_name[-5:] != '.fits'):
        file_name += '.fits'
        smeargle_warning(InputWarning, ("The fits file name does not have a .fits extension; "
                                        "it has been automatically added."))

    # Create the main HDUL object to write the fits file.
    # Check for the hdu_object.
    if (isinstance(hdu_object,(ap_fits.PrimaryHDU,ap_fits.HDUList))):
        # Astropy can handle PrimaryHDU -> .fits conversion.
        hdul_file = hdu_object
    else:
        # Else, deal with the data.
        hdu = ap_fits.PrimaryHDU(data=np.array(hdu_data), header=hdu_header)
        hdul_file = ap_fits.HDUList([hdu])

    # Check if the data is a masked array, if it is, extract the mask and save
    # it to write in an extension.
    if (isinstance(hdu_data,np_ma.MaskedArray)):
        # Get data mask and convert to int array; apparently fits files do not
        # work well with booleans.
        data_mask = np_ma.getmaskarray(hdu_data)
        data_mask = np.array(np.where(data_mask, int(1), int(0)), dtype=int)
        # Create the HDU object mask.
        data_mask_hdu = ap_fits.ImageHDU(data_mask, name='IFASMASK')
        hdul_file.append(data_mask_hdu)

        # Warn that the mask has been added.
        smeargle_warning(OutputWarning,("The data array provided has been detected to be a "
                                        "masked array. The mask is saved in the fits extension "
                                        "<IFASMASK>. The primary data is not affected."))


    # Check to see if the file exists, if so, then overwrite if provided for.
    if (os.path.isfile(file_name)):
        if (overwrite):
            # It should be overwritten, warn to be nice. 
            smeargle_warning(OverwriteWarning,("There exists a file with the provided name. "
                                               "Overwrite is true; the previous file will "
                                               "be replaced as provided."))
        else:
            # It should not overwritten at this point.
            raise ExportingError("There exists a file with the same name as the previous one. "
                                 "Overwrite is set to False, the new fits file cannot "
                                 "be written.")

    # Write, follow overwrite instructions, assume the user knows what they 
    # are doing. Return object.
    hdul_file.writeto(file_name, overwrite=overwrite)
    return hdul_file
    


def smeargle_extract_subarray(primary_array,x_bounds,y_bounds):
    """ A function to extract a smaller array copy from a larger array.

    Sub-arrays are rather important in the analysis of specific arrays. 
    This function extracts a sub-array from a given primary array specified 
    by the x_bounds and y_bounds.

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

    # Be verbose in accepting reversed (but valid) bounds.
    x_bounds = np.sort(x_bounds)
    y_bounds = np.sort(y_bounds)

    sub_array = primary_array[y_bounds[0]:y_bounds[-1],x_bounds[0]:x_bounds[1]]

    return np.array(sub_array)


def smeargle_masked_array_min_max(masked_array):
    """ This function returns a masked array's minimum and maximum value.

    This function determines the minimum and maximum of a masked arrays 
    between valid, unmasked, values only. Masked values are not considered 
    for min-max evaluation.
    
    Parameters
    ----------
    masked_array : masked ndarray 
        The array that has a mask, and is also the one that will have a 
        min max calculated.

    Returns
    -------
    masked_min : float
        The value of the minimum of the masked array ignoring masking.
    masked_max : float
        The value of the maximum of the masked array ignoring masking.
    """
    
    # Sparrow was wrong when coding the function that required this function.
    # It has scene been reduced to the logical answer and is thus depreciated. 
    smeargle_warning(DepreciationWarning,("This function was built because of the erroneous "
                                          "understanding that it was difficult to get min-max "
                                          "from Numpy Masked Arrays. This function is a "
                                          "wrapper around the easy and proper method."))

    # Execute a copy just in case of damage to the array.
    masked_array = copy.deepcopy(masked_array)

    # Finding the minimum of the array.
    masked_min = masked_array.min()

    # Finding the maximum of the array
    masked_max = masked_array.max()

    return masked_min, masked_max

