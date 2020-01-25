
import astropy as ap
import astropy.io.fits as ap_fits
import numpy as np
import numpy.ma as np_ma
import warnings as warn

from IfA_Smeargle.meta import *

"""
This module parses the data cubes, extracting the needed information from the 
first X and last X frames, adapting them and outputting them. 
"""


def median_endpoints(data_array, start_chunk, end_chunk):
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
    final_data : ndarray
        The final data array of the median-ed frames as desired.
    """

    # Evaluate the averaging.
    final_data = _primary_median_function(data_array=data_array, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=1)
    return final_data

def median_endpoints_per_second(data_array, start_chunk, end_chunk, frame_exposure_time):
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

    Returns
    -------
    final_data : ndarray
        The final data array of the median-ed frames as desired.
    """

    # The divisor is naturally the integration time, in seconds, for this
    # function.
    integration_time = ((meta_math.smeargle_mean(end_chunk)-meta_math.smeargle_mean(start_chunk)) 
                        * frame_exposure_time)

    # Evaluate the averaging.
    final_data = _primary_median_function(data_array=data_array, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=integration_time,
                                        write_file=write_file, alternate_name=alternate_name)
    return final_data


def median_endpoints_per_kilosecond(data_array, start_chunk, end_chunk, frame_exposure_time):
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

    Returns
    -------
    final_data : ndarray
        The final data array of the median-ed frames as desired.
    """

    # The divisor is naturally the integration time, in seconds.
    integration_time = ((meta_math.smeargle_mean(end_chunk)-meta_math.smeargle_mean(start_chunk)) 
                        * frame_exposure_time)
    # However, this function desires kiloseconds, therefore, integration time 
    # should be factored down.
    integration_time_kilosecond = integration_time / 1000.0

    # Evaluate the averaging.
    final_data = _primary_median_function(data_array=data_array, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=integration_time_kilosecond,
                                        write_file=write_file, alternate_name=alternate_name)

    return final_data



def _primary_mean_function(*args, **kwargs):
    """ For means. """
    return _primary_combination_function(combining_function=meta_math.smeargle_mean, 
                                         *args, **kwargs)

def _primary_median_function(*args, **kwargs):
    """ For medians. """
    return _primary_combination_function(combining_function=meta_math.smeargle_median, 
                                         *args, **kwargs)

def _primary_combination_function(data_array, start_chunk, end_chunk, 
                                  divisor, combining_function):
    """ This function takes a 3D array and computes its end section values.

    This function reads in an array of 3 dimensions, averaging some 
    top chunk and bottom chunk of their "temporal" axis.

    If there is no temporal axis, this program raises an error.
    
    Parameters
    ----------
    data_array : ndarray
        This is the data array that will be modified, or at least have its
        values calculated from.
    start_chunk : array-like
        The exact range of frames from the beginning that will be median-ed.
    end_chunk : array-like
        The exact range of frames from the bottom that will be median-ed.
    divisor : float
        An value by which the data frame will be divided by to either act as 
        a normalization or a per-unit factor.
    combining_function : function
        The function that would be used to combine the arrays.

    Returns
    -------
    final_data : ndarray
        The final data array of the median-ed frames as desired.
    """

    # Check and adapt for a masked array.
    if (np_ma.isMaskedArray(data_array)):
        raw_data = np_ma.get_data(data_array)
        data_mask = np_ma.get_mask(data_array)
    else:
        raw_data = np.array(data_array)
        data_mask = None

    # Check for too many or too little dimensions; it is important as the 
    # array shape of data is assumed.
    if (len(np.array(raw_data).shape) <= 2):
        raise InputError("The data of the input fits file does not have any wavelength or "
                         "temporal axis; to collapse spatially would be incorrect.")
    elif (len(np.array(raw_data).shape) > 3):
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

    # Calculate the medians. The custom median functions are needed to handle
    # both nans and masked arrays.
    start_median = combining_function(raw_data[start_chunk[0]:start_chunk[-1]],axis=0)
    end_median = combining_function(raw_data[end_chunk[0]:end_chunk[-1]],axis=0)

    # Subtracting and normalizing over the time span, starting and ending
    # at respective midpoints; integer multiplication/division is required  
    # because of the discrete nature of frames.
    final_raw_data = (end_median - start_median) / divisor

    # Reapply the mask if there was a mask.
    if (data_mask is not None):
        final_data = np_ma.array(data=final_raw_data, mask=data_mask)
    else:
        final_data = np.array(final_raw_data)

    return final_data