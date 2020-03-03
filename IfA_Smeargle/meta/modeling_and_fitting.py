
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma
import scipy.signal as sp_sig
import scipy.stats as sp_stat

from IfA_Smeargle.meta import *


def smeargle_fit_gaussian_function(x_data, y_data, inital_guesses):
    """ This function fits a Gaussian function to a specific set of data.

    Gaussian fitting is hard, this function exists as a port so that 
    all fitting functions use the same algorithm and said algorithm is easy
    to change.
    
    Parameters
    ----------
    x_data : ndarray
        The X data that the Gaussian will be fit over.
    y_data : ndarray
        The Y data that the Gaussian will be fit over.
    inital_guesses : dictionary
        Initial guesses for the Gaussian fitting function.

    Returns
    -------
    gaussian_function : function
        A callable function that when provided an X value, it will return
        the value of the function.
    gaussian_parameters : dictionary
        A compiled dictionary of all of the parameters of the Gaussian fit.
    """

    # Extract the initial guesses.
    try: 
        guess_mean = inital_guesses['mean'] 
    except Exception: 
        guess_mean = 0
    try:
        guess_stddev = inital_guesses['stddev']
    except Exception:
        guess_stddev = 1
    try:
        guess_amplitude = inital_guesses['amplitude']
    except Exception:
        guess_amplitude = 1

    # Plotting/fitting the Gaussian function.  For some reasons beyond 
    # what Sparrow can explain, Astropy seems to have better fitting 
    # capabilities, in this specific application, than Scipy.
    gaussian_init = ap_mod.models.Gaussian1D(amplitude=guess_amplitude, 
                                             mean=guess_mean, 
                                             stddev=guess_stddev)
    gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
    gaussian_fit = gaussian_fit_model(gaussian_init, x_data, y_data)

    # Deriving basic information form Gaussian model to return back to 
    # the user.
    gaussian_mean = gaussian_fit.mean.value
    gaussian_stddev = gaussian_fit.stddev.value
    gaussian_amplitude = gaussian_fit.amplitude.value
    temp_gauss_x_axis = np.linspace(np.nanmin(x_data) - 1, np.nanmax(x_data) + 1, 
                                    x_data.size * 100)
    gaussian_max = np.max(gaussian_fit(temp_gauss_x_axis))
    gaussian_parameters = {'mean': gaussian_mean, 'stddev': gaussian_stddev,
                           'amplitude': gaussian_amplitude,'max' : gaussian_max}

    # The Gaussian function
    gaussian_function = lambda input: gaussian_fit(np.array(input))

    return gaussian_function, gaussian_parameters

def smeargle_fit_histogram_gaussian_function(data_array, bin_width):
    """ This function fits a Gaussian function to a specific set of data.

    Gaussian fitting is hard, this function exists as a port so that 
    all fitting functions use the same algorithm and said algorithm is easy
    to change. This applies it to the histogram of the data.
    
    Parameters
    ----------
    data_array : ndarray
        The data that the histogram Gaussian function is fitting.
    bin_width : float
        The width of the bins to use for the histogram fitting function.

    Returns
    -------
    gaussian_function : function
        A callable function that when provided an X value, it will return
        the value of the function.
    gaussian_parameters : dictionary
        A compiled dictionary of all of the parameters of the Gaussian fit.
    """

    # Be able to accept both masked arrays and standard arrays and be able 
    # to tell.
    if (np_ma.is_masked(data_array)):
        flat_data = data_array.compressed()
    else:
        flat_data = data_array.flatten()

    # For consistent measurements have a lot of bins throughout the values. 
    # Extracting function temporarily.
    from IfA_Smeargle.oscar.oscar_functions import oscar_bin_width
    hist_bins = oscar_bin_width(data_array=flat_data, bin_width=bin_width)
    del oscar_bin_width

    # Extract histogram data from the data.
    hist_data = np.histogram(flat_data, bins=hist_bins)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Middle of bin.
    hist_y = hist_data[0]

    # Filter out some of the bins with very little information, that is
    # those who's values can be seen more as noise than good data.
    valuecut_index = np.where(hist_y >= sp_stat.variation(hist_y))
    cuthist_x = np.array(hist_x[valuecut_index])
    cuthist_y = np.array(hist_y[valuecut_index])

    # Often times the largest bin is just a large collection of bad pixels. 
    # The fit 


    # Initial guesses...
    def extract_fwhm_estimate(param_fwhm_esti_list, param_cuthist_y):
        """ This is needed to pragmatically deal with the fact that some 
        initial maximum FWHM estimates are very wrong, and that the second 
        highest value would likely be better.
        """
        possible_fwhm_esti = np.nanmax(np.array(param_fwhm_esti_list))
        # Check if the value is too high, compare to the stddev value of the
        # y-axis values.
        if (possible_fwhm_esti > np.nanstd(param_cuthist_y)):
            # Use the second highest value instead.
            possible_fwhm_esti = np.partition(param_fwhm_esti_list.flatten(), -2)[-2]
        return possible_fwhm_esti

    # Reverse calculating from FWHM estimates based on the most prominent
    # peak found. Using the FWHM number conversion. 
    peak_index, __ = sp_sig.find_peaks(cuthist_y, width=5)
    fwhm_esti_list = sp_sig.peak_widths(cuthist_y, peak_index, rel_height=0.5)[0]
    try:
        fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cuthist_y)
    except ValueError:
        # The estimate itself is blank. Remember some Nyquist principles. If
        # If the true data "peak" is only one pixel big, a misfit doesn't
        # matter too much 
        peak_index, __ = sp_sig.find_peaks(cuthist_y, width=2)
        fwhm_esti_list = sp_sig.peak_widths(cuthist_y, peak_index, rel_height=0.5)[0]
        try:
            fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cuthist_y)
        except ValueError:
            # The most scenically lose conditions were not enough. Just once
            # more, and maybe. However, raise a warning.
            smeargle_warning(DataWarning,("Nyquist peaks cannot be found, relying on 1-bin "
                                          "wide peaks for estimates. Estimates may be very "
                                          "off."))
            peak_index, __ = sp_sig.find_peaks(cuthist_y)
            fwhm_esti_list = sp_sig.peak_widths(cuthist_y, peak_index, rel_height=0.5)[0]
            try:
                fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cuthist_y)
            except ValueError:
                # Inform the user of the failure of peak-finding. Prevent 
                # an Unbound error by assigning a dummy value.
                fwhm_esti = 0
                raise DataError("It seems that there is no peak in the data, suggesting a very "
                                "flat profile. The Gaussian fit cannot be applied.")
    finally:
        guess_stddev = fwhm_esti / 2.35482 # 2 sqrt(2 ln 2)
    # The peak location where the stddev estimate was calculated is as good 
    # as any.
    try:
        guess_mean = cuthist_x[peak_index[np.argmax(cuthist_y[peak_index])]]
    except ValueError:
        # Just in case the guessing of peaks completely failed, this is an
        # acceptable backup.
        guess_mean = cuthist_x[np.argmax[cuthist_y]]
    # The highest value is as good as any guess for the amplitude.
    try:
        guess_amplitude = cuthist_y[peak_index[np.argmax(cuthist_y[peak_index])]]
    except ValueError:
        # Just in case the guessing of peaks completely failed, this is an
        # acceptable backup.
        guess_amplitude = np.nanmax(cuthist_y)


    # Do the Gaussian fit.
    inital_guesses = {'mean': guess_mean,
                      'stddev': guess_stddev,
                      'amplitude': guess_amplitude}
    gaussian_function, gaussian_parameters = smeargle_fit_gaussian_function(cuthist_x, cuthist_y, 
                                                                            inital_guesses)

    return gaussian_function, gaussian_parameters
