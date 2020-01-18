
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

def auto_avergae_slicing(fits_file, reference_chunk, split_chunks, averaging_function,
                         function_parameters={},
                         write_file=True, post_mask=None):
    """ This function splits the HDU file into different chunks and applies 
    averaging functions provided to said data.

    This is mostly a method of automation than a method of actual value. 
    However, for most pipelines that split data into different chunks, it is
    preferable that this function is used. 

    Parameters
    ----------
    fits_file : string or Astropy HDUList file
        This is the fits file that will be modified, or at least have its
        values calculated from.
    reference_chunk : array-like
        The exact range of frames from the beginning that will be median-ed
        and to be used as the reference chunk for all of the split chunks.
    split_chunks : array-like
        The list of chunk boundaries that will be processed and written as
        different files.
    averaging_function : function
        The averaging function that will be applied to the data. All BRAVO
        averaging functions are supported.
    function_parameters : dictionary
        Extra parameters required by the averaging function.
    write_file : boolean (optional)
        If true, the Astropy HDUL object is written to a fits file with the 
        split parameter in the name.
    post_mask : array-like
        A mask that will be applied at the end of the automatic averaging
        method. 

    Returns
    -------
    nothing
    """

    raise DeprecationError

    # Correct the dimensionality of the split chunks. Embed single chunk 
    # ranges or throw an error for too many indexes.
    split_chunks = np.array(split_chunks)
    if (len(split_chunks.shape) == 1):
        # Assume that it is only one chunk.
        split_chunks = np.array([split_chunks])
    elif (len(split_chunks.shape) == 2):
        # Assume it is fine.
        pass
    else:
        raise InputError("The dimensions of the split chunks are not yield-able. They should "
                         "an array of ranges, specifying each chunk; therefore, the number of "
                         "dimensions shall be three.")

    # Calculating the differing averaging frames.
    for splitdex in split_chunks:
        # Deriving an alternate name.
        alt_name = (fits_file[:-5] 
                    + '__' + 'slice;' + str(splitdex[0]) + '-' + str(splitdex[1]) 
                    + fits_file[-5:])
        # Executing averaging and writing, saving the mask.
        hdu_to_be_written = averaging_function(fits_file, reference_chunk, splitdex, 
                                               write_file=False,
                                               alternate_name=alt_name,
                                               **function_parameters)
        temp_header = hdu_to_be_written[0].header 
        temp_data = np_ma.array(hdu_to_be_written[0].data, mask=post_mask)
        meta_faa.smeargle_write_fits_file(alt_name, temp_header, temp_data, silent=True)

    return None



def median_endpoints(fits_file, start_chunk, end_chunk,
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

    # Evaluate the averaging.
    hdu_file = _primary_median_function(fits_file=fits_file, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=1,
                                        write_file=write_file, alternate_name=alternate_name)
    return hdu_file

def median_endpoints_per_second(fits_file, start_chunk, end_chunk, frame_exposure_time,
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

    # The divisor is naturally the integration time, in seconds, for this
    # function.
    integration_time = ((meta_math.smeargle_mean(end_chunk)-meta_math.smeargle_mean(start_chunk)) 
                        * frame_exposure_time)

    # Evaluate the averaging.
    hdu_file = _primary_median_function(fits_file=fits_file, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=integration_time,
                                        write_file=write_file, alternate_name=alternate_name)
    return hdu_file


def median_endpoints_per_kilosecond(fits_file, start_chunk, end_chunk, frame_exposure_time,
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

    # The divisor is naturally the integration time, in seconds.
    integration_time = ((meta_math.smeargle_mean(end_chunk)-meta_math.smeargle_mean(start_chunk)) 
                        * frame_exposure_time)
    # However, this function desires kiloseconds, therefore, integration time 
    # should be factored down.
    integration_time_kilosecond = integration_time / 1000.0

    # Evaluate the averaging.
    hdu_file = _primary_median_function(fits_file=fits_file, 
                                        start_chunk=start_chunk, end_chunk=end_chunk, 
                                        divisor=integration_time_kilosecond,
                                        write_file=write_file, alternate_name=alternate_name)

    return hdu_file



def _primary_mean_function(*args, **kwargs):
    """ For means. """
    return _primary_combination_function(combining_function=meta_math.smeargle_mean, 
                                         *args, **kwargs)

def _primary_median_function(*args, **kwargs):
    """ For medians. """
    return _primary_combination_function(combining_function=meta_math.smeargle_median, 
                                         *args, **kwargs)

def _primary_combination_function(fits_file, start_chunk, end_chunk, 
                                  divisor, combining_function, 
                                  write_file=False, alternate_name=None):
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
    divisor : float
        An value by which the data frame will be divided by to either act as 
        a normalization or a per-unit factor.
    combining_function : function
        The function that would be used to combine the arrays.
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

    # Check and adapt for a masked array.
    if (np_ma.isMaskedArray(data)):
        raw_data = np_ma.get_data(data)
        data_mask = np_ma.get_mask(data)
    else:
        raw_data = np.array(data)
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

    # Check to see if the user provided an alternate name.
    if ((alternate_name is not None) and (isinstance(alternate_name,str))):
        writing_file_name = alternate_name
    else:
        writing_file_name = fits_file

    # Reapply the mask if there was a mask.
    if (data_mask is not None):
        final_data = np_ma.array(data=final_raw_data, mask=data_mask)
    else:
        final_data = np.array(final_raw_data)

    # Write the file. Also, it is expected that the fits files are 
    # overwritten, suppress the warning that comes with it.
    with warn.catch_warnings():
        warn.simplefilter("ignore", category=OverwriteWarning)
        hdu_file = meta_faa.smeargle_write_fits_file(writing_file_name, header, final_data,
                                                     save_file=write_file)

    return hdu_file