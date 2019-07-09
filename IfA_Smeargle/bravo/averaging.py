
import astropy as ap
import astropy.io.fits as ap_fits
import numpy as np

from IfA_Smeargle.meta import *

"""
This module parses the data cubes, extracting the needed information from the 
first X and last X frames, adapting them and outputting them. 
"""


def average_endpoints(fits_file, start_chunk, end_chunk, frame_exposure_time,
                      write_file=True, alternate_name=None):
    """ This function reads a fits file and computes its end section values.

    This function reads in a fits file of 3 dimensions, averaging some 
    top chunk and bottom chunk of their "temporal" axis, normalizing
    and dividing over a timespan. 

    If there is no temporal axis, this program raises an error.
    
    Parameters
    ----------
    fits_file : string or Astropy HDUList file
        This is the fits file that will be modified, or at least have its
        values calculated from.
    start_chunk : int
        The exact number of frames from the beginning that will be median-ed.
    end_chunk : int
        The exact number of frames from the bottom that will be median-ed.
    frame_exposure_time : float
        The duration, per frame (in seconds), of each exposure.
    write_file : boolean (optional)
        If true, the Astropy HDUL object is written to a fits file.
    alternate_name : string (optional)
        An alternate fits file name to write the data too instead of the 
        first provided one.

    Returns
    -------
    hdu_file : Astropy HDUList file
        The HDUList object of the written file.
    """

    # Test for the different cases of the fits file.
    if (isinstance(fits_file,str)):
        hdu_obj, header, data = meta_faa.smeargle_open_fits_file(fits_file)
    elif (isinstance(fits_file,ap_fits.HDUList)):
        hdu_obj = fits_file 
        header = fits_file[0].header
        data = fits_file[0].data
    elif (isinstance(fits_file,ap_fits.PrimaryHDU)):
        hdu_obj = ap_fits.HDUList([fits_file])
        header = fits_file.header
        data = fits_file.data

    # Check for too many or too little dimensions; it is important as the 
    # array shape of data is assumed.
    if (len(np.array(data).shape) <= 2):
        raise InputError("The data of the input fits file does not have any wavelength or "
                         "temporal axis; to collapse spatially would be incorrect.")
    elif (len(np.array(data).shape) > 3):
        smeargle_warning(InputWarning,("The number of dimensions in the data array is greater "
                                       "than 3, it is assumed that the 0th axis is the temporal "
                                       "axis."))

    # It is unnatural, but not forbidden, to have differing top and bottom 
    # chunk range values.
    if (start_chunk != end_chunk):
        smeargle_warning(ReductionWarning,("The size of the start chunk and end chunk are "
                                           "different sizes, this is unusual but acceptable."))

    # Calculate the medians.
    start_median = np.median(data[-start_chunk:],axis=0)
    end_median = np.median(data[:end_chunk],axis=0)

    # Subtracting and normalizing over the time span, starting and ending
    # at respective midpoints; integer multiplication/division is required  
    # because  of the discrete nature of frames.
    integration_time = (data.shape[0] - (start_chunk//2 + end_chunk//2)) * frame_exposure_time
    final_data = (start_median - end_median)/integration_time

    # Check to see if the user provided an alternate name.
    if ((alternate_name is not None) and (isinstance(alternate_name,str))):
        writing_file_name = alternate_name
    else:
        writing_file_name = fits_file

    # Header information preserves the values used for the beginning and 
    # ending chunks. May be unneeded.
    header['previous_size'] = (data.shape[0], 'How long the temporal axis was in frames.')
    header['start_chunk'] = (start_chunk, 'The length of the starting median block.')
    header['end_chunk'] = (end_chunk, 'The length of the ending median block.')

    if (write_file):
        # Write the file. 
        hdu_file = meta_faa.smeargle_write_fits_file(writing_file_name, header, final_data)

    return hdu_file