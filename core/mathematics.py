
import numpy as np
import numpy.ma as np_ma

import astropy as ap
import astropy.modeling as ap_mod

import IfA_Smeargle.core as core

def ifas_masked_mean(array, axis=None):
    """ This returns the true mean of the data. It only counts 
    valid data.

    There are outstanding problems with how the masked arrays 
    handle means. For some reason, there is no np.ma.nanmean 
    function. This adds that functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the mean will be
       taken from.
    axis : int 
        The axis that the mean will be taken over.

    Returns
    -------
    true_mean : float or ndarray
        The mean of the array along which ever axis was given. 
    """

    # Fix all invalid data before taking the mean.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise core.error.DataError("The array still contains invalid nan "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")
    if (np.any(np.isinf(valid_array))):
        raise core.error.DataError("The array still contains invalid inf "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")

    # Calculate and return the mean. The masked array version of the 
    # functions seems to properly ignore masks as intended.
    true_mean = np_ma.mean(valid_array, axis=axis)

    return true_mean

def ifas_masked_median(array, axis=None):
    """ This returns the true median of the data. It only counts 
    valid data.

    There are outstanding problems with how the masked arrays 
    handle medians. For some reason, there is no np.ma.nanmedian 
    function. This adds that functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the median will be 
        taken from.
    axis : int 
        The axis that the median will be taken over.

    Returns
    -------
    true_median : float or ndarray
        The median of the array along which ever axis was given. 
    """
    # Fix all invalid data before taking the median.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise core.error.DataError("The array still contains invalid nan "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")
    if (np.any(np.isinf(valid_array))):
        raise core.error.DataError("The array still contains invalid inf "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")

    # Calculate and return the median. The masked array version of 
    # the functions seems to properly ignore masks as intended.
    true_median = np_ma.median(valid_array, axis=axis)

    return true_median

def ifas_masked_std(array, axis=None):
    """ This returns the true standard deviation of the data. It 
    only counts valid data.

    There are outstanding problems with how the masked arrays 
    handle stds. For some reason, there is no np.ma.nanstd 
    function. This adds that functionality.

    Parameters
    ----------
    array : ndarray
        The value or array of values by which the standard deviation 
        will be taken from.
    axis : int 
        The axis that the median will be taken over.

    Returns
    -------
    true_std : float or ndarray
        The standard deviation of the array along which ever axis 
        was given. 
    """

    # Fix all invalid data before taking the median.
    valid_array = np_ma.fix_invalid(array)

    # Test to see if there is any invalid data left.
    if (np.any(np.isnan(valid_array))):
        raise core.error.DataError("The array still contains invalid nan "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")
    if (np.any(np.isinf(valid_array))):
        raise core.error.DataError("The array still contains invalid inf "
                                   "data after the invalid data was fixed. "
                                   "The true mean function will not work "
                                   "as expected.")

    # Calculate and return the standard deviation. The masked array 
    # version of the functions seems to properly ignore masks as 
    # intended.
    true_std = np_ma.std(valid_array, axis=axis)

    return true_std


def ifas_robust_mean(array):
    """ This provides a more robust measurement of the mean of the 
    array of values.

    Parameters
    ----------
    array : ndarray
        The array of values by which the mean will be 
        calculated from.

    Returns
    -------
    robust_mean : float
        The robust mean value.
    """
    # Do not explicitly expect an array.
    if (isinstance(array, np.ndarray)):
        x = array
    else:
        x = np.array(x)

    # This section is provided code from Dr. Mike Bottom.
    y = x.flatten()
    n = len(y)
    y.sort()
    ind_qt1 = round((n+1)/4.)
    ind_qt3 = round((n+1)*3/4.)
    IQR = y[ind_qt3]- y[ind_qt1]
    lowFense = y[ind_qt1] - 1.5*IQR
    highFense = y[ind_qt3] + 1.5*IQR
    ok = (y>lowFense)*(y<highFense)
    yy=y[ok]
        
    # For documentation
    robust_mean = yy.std(dtype='double')
    return robust_mean

def ifas_robust_std(array):
    """ This provides a more robust measurement of the standard 
    deviation of the array of values.

    Parameters
    ----------
    array : ndarray
        The array of values by which the standard deviation will be 
        calculated from.

    Returns
    -------
    robust_std : float
        The robust standard deviation value.
    """
    # Do not explicitly expect an array.
    if (isinstance(array, np.ndarray)):
        x = array
    else:
        x = np.array(x)

    # This section is provided code from Dr. Mike Bottom.
    y = x.flatten()
    n = len(y)
    y.sort()
    ind_qt1 = int(round((n+1)/4.))
    ind_qt3 = int(round((n+1)*3/4.))
    IQR = y[ind_qt3]- y[ind_qt1]
    lowFense = y[ind_qt1] - 1.5*IQR
    highFense = y[ind_qt3] + 1.5*IQR
    ok = (y>lowFense)*(y<highFense)
    yy=y[ok]

    # For documentation
    robust_std = yy.std(dtype='double')
    return robust_std


def ifas_gaussian_function(input, mean, stddev, amplitude):
    """ This is a wrapper function around Astropy's Gaussian
    function. This takes the input of a function, and gives it an
    output according to the Gaussian parameters provided. The 
    function itself is also returned.

    Parameters
    ----------
    input : array
        The input into the Gaussian function.
    mean : float
        The mean of the Gaussian function.
    stddev : float
        The standard deviation of the Gaussian function.
    amplitude : float
        The amplitude to of the Gaussian function.
    
    Returns
    -------
    output : array
        The output when the Gaussian function is calculated from the 
        input.
    gaussian_function : function
        The Gaussian function with the parameters provided already
        given.
    """

    # The Gaussian function itself.
    def gaussian_model(input=None, mean=0, stddev=0, amplitude=0):
        # A wrapper around Astropy's.
        gaussian = ap_mod.models.Gaussian1D(amplitude=amplitude, mean=mean,
                                            stddev=stddev)
        # Evaluation.
        output = gaussian.evaluate(input, amplitude=amplitude, 
                                   mean=mean, stddev=stddev)
        # Return
        return output

    # Return both the function and its evaluation.
    gaussian_function = lambda x: gaussian_model(input=np.array(x), 
                                                 mean=mean, stddev=stddev, 
                                                 amplitude=amplitude)
    output = gaussian_function(x=np.array(input))

    # All done.
    return output, gaussian_function

def generate_numpy_bin_width_array(data_array, bin_width, 
                                   local_minimum=None, local_maximum=None):
    """ Matplotlib does not support having input bin withs; this 
    returns a valid form.

    This function just generates a valid bin value list provided a 
    given bin widths. If the ``local_maximum`` or 
    ``local_minimum value`` is not provided, then the absolute 
    maximum and minimum of the provided array is used. 

    If mod[(max - min), bin_width] != 0, the last/highest bin is 
    disenfranchised. This function can adapt to masked arrays. 

    Parameters
    ----------
    data_array : ndarray
        The data to which the bins will be calculated from; 
        ignored if the two local maximum and minimum parameters are 
        provided.
    bin_width : float
        The width of the bins.
    local_minimum : float (optional)
        A predefined minimum that the calculating function 
        should use.
    local_maximum : float (optional)
        A predefined maximum that the calculating function 
        should use. 

    Returns
    -------
    bin_list_values : ndarray
        A list of values that can be fed into matplotlib to emulate 
        binning by a value width.
    """

    # Test if the user provided their own minimum or maximums.
    if ((local_minimum is not None) and (local_maximum is not None)):
        # They have, apply the minimum and maximums.
        minimum = local_minimum
        maximum = local_maximum
    else:
        # They have not, or at least, it is not a usable set.
        if (not isinstance(data_array,np.ndarray)):
            data_array = np.array(data_array)
            # Do not count data that is masked, or 
            # MaskedArray.compressed() only returns unmasked values.
            flat_data = (data_array.compressed() 
                         if np_ma.is_masked(data_array) 
                         else data_array.flatten())
        # Nans normally clog up the computation of maximums 
        # and minimums.
        minimum = np.nanmin(data_array)
        maximum = np.nanmax(data_array)

    # Calculate the bins based off of the width provided. Numpy 
    # is pretty good with this.
    bin_list_values = np.arange(minimum, maximum, bin_width)
    bin_list_values = np.append(bin_list_values, maximum)

    # All done, return.
    return bin_list_values