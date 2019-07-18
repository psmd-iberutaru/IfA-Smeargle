
import astropy as ap
import astropy.io.fits as ap_fits
import numpy as np
import warnings as warn

from IfA_Smeargle.meta import *

"""
This module parses the data cubes, extracting the needed information from the 
first X and last X frames, adapting them and outputting them. 
"""


def average_endpoints(fits_file, start_chunk, end_chunk,
                      write_file=True, alternate_name=None):
    """ This function reads a fits file and computes its end section values.

    This function reads in a fits file of 3 dimensions, averaging some 
    top chunk and bottom chunk of their "temporal" axis.

    If there is no temporal axis, this program raises an error.
    
    Parameters
    ----------
    fits_file : string or Astropy HDUList file
        This is the fits file that will be modified, or at least have its
        values calculated from.
    start_chunk : array-like
        The exact range of frames from the beginning that will be median-ed.
    end_chunk : array-like
        The exact range of frames from the bottom that will be median-ed.
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
    if (isinstance(fits_file, str)):
        hdu_obj, header, data = meta_faa.smeargle_open_fits_file(fits_file)
    elif (isinstance(fits_file, ap_fits.HDUList)):
        hdu_obj = fits_file 
        header = fits_file[0].header
        data = fits_file[0].data
    elif (isinstance(fits_file, ap_fits.PrimaryHDU)):
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

    # Allow for swapped, but valid ranges.
    start_chunk = np.sort(start_chunk)
    end_chunk = np.sort(end_chunk)
    # Check if the chunks overlap, if they do, this is a problem.
    if (start_chunk[1] >= end_chunk[0]):
        raise InputError("The end of the start_chunk is after the start of the end_chunk. The "
                         "overlap is improper and should be fixed.")
    # It is unnatural, but not forbidden, to have differing top and bottom 
    # chunk range values.
    if (start_chunk.ptp() != end_chunk.ptp()):
        smeargle_warning(ReductionWarning,("The size of the start chunk and end chunk are "
                                           "different sizes, this is unusual but acceptable."))

    # Calculate the medians.
    start_median = np.median(data[start_chunk[0]:start_chunk[-1]],axis=0)
    end_median = np.median(data[end_chunk[0]:end_chunk[-1]],axis=0)

    # Subtracting and normalizing over the time span, starting and ending
    # at respective midpoints; integer multiplication/division is required  
    # because  of the discrete nature of frames.
    final_data = end_median - start_median

    # Check to see if the user provided an alternate name.
    if ((alternate_name is not None) and (isinstance(alternate_name,str))):
        writing_file_name = alternate_name
    else:
        writing_file_name = fits_file

    if (write_file):
        # Write the file. Also, it is expected that the fits files are 
        # overwritten, suppress the warning that comes with it.
        with warn.catch_warnings():
            warn.simplefilter("ignore", category=OverwriteWarning)
            hdu_file = meta_faa.smeargle_write_fits_file(writing_file_name, header, final_data)

    return hdu_file



def average_endpoints_per_second(fits_file, start_chunk, end_chunk, frame_exposure_time,
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
    start_chunk : array-like
        The exact range of frames from the beginning that will be median-ed.
    end_chunk : array-like
        The exact range of frames from the bottom that will be median-ed.
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
    if (isinstance(fits_file, str)):
        hdu_obj, header, data = meta_faa.smeargle_open_fits_file(fits_file)
    elif (isinstance(fits_file, ap_fits.HDUList)):
        hdu_obj = fits_file 
        header = fits_file[0].header
        data = fits_file[0].data
    elif (isinstance(fits_file, ap_fits.PrimaryHDU)):
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

    # Check for too many or too little dimensions; it is important as the 
    # array shape of data is assumed.
    if (len(np.array(data).shape) <= 2):
        raise InputError("The data of the input fits file does not have any wavelength or "
                         "temporal axis; to collapse spatially would be incorrect.")
    elif (len(np.array(data).shape) > 3):
        smeargle_warning(InputWarning,("The number of dimensions in the data array is greater "
                                       "than 3, it is assumed that the 0th axis is the temporal "
                                       "axis."))

    # Allow for swapped, but valid ranges.
    start_chunk = np.sort(start_chunk)
    end_chunk = np.sort(end_chunk)
    # Check if the chunks overlap, if they do, this is a problem.
    if (start_chunk[1] >= end_chunk[0]):
        raise InputError("The end of the start_chunk is after the start of the end_chunk. The "
                         "overlap is improper and should be fixed.")
    # It is unnatural, but not forbidden, to have differing top and bottom 
    # chunk range values.
    if (start_chunk.ptp() != end_chunk.ptp()):
        smeargle_warning(ReductionWarning,("The size of the start chunk and end chunk are "
                                           "different sizes, this is unusual but acceptable."))

    # Calculate the medians.
    start_median = np.median(data[start_chunk[0]:start_chunk[-1]],axis=0)
    end_median = np.median(data[end_chunk[0]:end_chunk[-1]],axis=0)

    # Subtracting and normalizing over the time span, starting and ending
    # at respective midpoints; integer multiplication/division is required  
    # because  of the discrete nature of frames.
    integration_time = ((np.mean(end_chunk) - np.mean(start_chunk)) * frame_exposure_time)
    final_data = (end_median-start_median)/integration_time

    # Check to see if the user provided an alternate name.
    if ((alternate_name is not None) and (isinstance(alternate_name,str))):
        writing_file_name = alternate_name
    else:
        writing_file_name = fits_file

    if (write_file):
        # Write the file. Also, it is expected that the fits files are 
        # overwritten, suppress the warning that comes with it.
        with warn.catch_warnings():
            warn.simplefilter("ignore", category=OverwriteWarning)
            hdu_file = meta_faa.smeargle_write_fits_file(writing_file_name, header, final_data)

    return hdu_file


def average_endpoints_per_kilosecond(fits_file, start_chunk, end_chunk, frame_exposure_time,
                                     write_file=True, alternate_name=None):
    """ This function reads a fits file and computes its end section values.

    This function reads in a fits file of 3 dimensions, averaging some 
    top chunk and bottom chunk of their "temporal" axis, normalizing
    and dividing over a timespan. The time is measured in kilo-seconds. This
    is basically a wrapper function around the per second version.

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

    # If frame_exposure_time is in per seconds, this converts it to per 
    # kilosecond, as desired. 
    new_frame_exposure_time = frame_exposure_time * 0.001 

    # Feed it through.
    hdu_file = average_endpoints_per_second(fits_file, start_chunk, end_chunk, 
                                            new_frame_exposure_time,
                                            write_file=write_file, alternate_name=alternate_name)

    return hdu_file