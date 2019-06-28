
import astropy as ap
import astropy.io.fits as ap_fits
import numpy as np

from ..meta import *

"""
This module parses the data cubes, extracting the needed information from the 
first X and last X frames, adapting them and outputting them. 
"""


def average_endpoints(fits_file, top_chunk, bottom_chunk, frame_exposure_time,
                      alternate_name=None):
    """ This function reads a fits file and computes its end section values.

    This function reads in a fits file of 3 dimensions, averaging some 
    top chunk and bottom chunk of their "temporal" axis, normalizing
    and dividing over a timespan. 
    
    Parameters
    ----------
    fits_file : string or Astropy HDUList file
        This is the fits file that will be modified, or at least have its
        values calculated from.
    top_chunk : int
        The exact number of frames from the top that will be median-ed.
    bottom_chunk : int
        The exact number of frames from the bottom that will be median-ed.
    frame_exposure_time : float
        The duration, per frame (in seconds), of each exposure.
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

    # Calculate the medians.
    top_median = np.median(data[-16:],axis=0)
    bottom_median = np.median(data[:16],axis=0)

    # Subtracting and normalizing over the time span.
    integration_time = (data.shape[0] - (top_chunk + bottom_chunk)) * frame_exposure_time
    final_data = (top_median - bottom_median)/integration_time

    # Check to see if the user provided an alternate name.
    if ((alternate_name is not None) and (isinstance(alternate_name,str))):
        writing_file_name = alternate_name
    else:
        writing_file_name = fits_file

    # Write the file.
    hdu_file = meta_faa.smeargle_write_fits_file(writing_file_name, header, final_data)
    return hdu_file