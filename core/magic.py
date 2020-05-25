"""
This is to hold functions that are pure 'magic'. That is, functions 
that perform what they are supposed to do, but, are fragile because 
their operations are not defined by conventional understanding, but 
instead as "it works, I don't know why, but it does".
"""
import numpy as np
import scipy as sp
import scipy.stats as sp_stat
import scipy.signal as sp_sig

import IfA_Smeargle.core as core

def magic_inital_gaussian_parameters(x_data, y_data):
    """
    This is a magic program to derive the guesses of Gaussian fit 
    parameters from an array of values.
    """
    # This is a magical function, it is not optimal and the user 
    # should know they are using magic. It is best to do more than 
    # warn.
    core.error.ifas_error(core.error.MagicError,
                          ("This function (to guess initial Gaussian "
                           "parameters) is a magic function. It is fragile "
                           "and should only be used if there is no better "
                           "implementation."))

    # Filter out some of the bins with very little information, that 
    # is those who's values can be seen more as noise than good data.
    valuecut_index = np.where(y_data >= sp_stat.variation(y_data))
    cut_xdata = np.array(x_data[valuecut_index])
    cut_ydata = np.array(y_data[valuecut_index])

    # Initial guesses...
    def extract_fwhm_estimate(param_fwhm_esti_list, param_cut_ydata):
        """ This is needed to pragmatically deal with the fact that 
        some initial maximum FWHM estimates are very wrong, and that 
        the second highest value would likely be better.
        """
        possible_fwhm_esti = np.nanmax(np.array(param_fwhm_esti_list))
        # Check if the value is too high, compare to the stddev 
        # value of the y-axis values.
        if (possible_fwhm_esti > np.nanstd(param_cut_ydata)):
            # Use the second highest value instead.
            possible_fwhm_esti = np.partition(
                param_fwhm_esti_list.flatten(), -2)[-2]
        return possible_fwhm_esti

    # Reverse calculating from FWHM estimates based on the most 
    # prominent peak found. Using the FWHM number conversion. 
    peak_index, __ = sp_sig.find_peaks(cut_ydata, width=5)
    fwhm_esti_list = sp_sig.peak_widths(cut_ydata, peak_index, 
                                        rel_height=0.5)[0]
    try:
        fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cut_ydata)
    except ValueError:
        # The estimate itself is blank. Remember some Nyquist 
        # principles. If the true data "peak" is only one pixel 
        # big, a misfit doesn't matter too much 
        peak_index, __ = sp_sig.find_peaks(cut_ydata, width=2)
        fwhm_esti_list = sp_sig.peak_widths(cut_ydata, peak_index, 
                                            rel_height=0.5)[0]
        try:
            fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cut_ydata)
        except ValueError:
            # The most scenically lose conditions were not enough. 
            # Just once more, and maybe. However, issue a warning.
            core.error.ifas_warning(core.error.DataWarning,
                                    ("Nyquist peaks cannot be found, "
                                     "relying on 1-bin wide peaks for "
                                     "estimates. Estimates may be off."))
            peak_index, __ = sp_sig.find_peaks(cut_ydata, width=1, 
                                               rel_height=1)
            fwhm_esti_list = sp_sig.peak_widths(cut_ydata, peak_index, 
                                                rel_height=0.5)[0]
            try:
                fwhm_esti = extract_fwhm_estimate(fwhm_esti_list, cut_ydata)
            except ValueError:
                # Inform the user of the failure of peak-finding. 
                # Prevent an UnboundError by assigning a dummy value.
                fwhm_esti = 2.3548200450309493 # For stddev guess to be 1.
                core.error.ifas_warning(core.error.DataWarning,
                                        ("It seems that there is no peak in "
                                         "the data, suggesting a very flat "
                                         "or sparse profile. The Gaussian "
                                         "parameter estimates are likely "
                                         "unreliable."))
    finally:
        guess_stddev = fwhm_esti / 2.3548200450309493 # 2 sqrt(2 ln 2)
    # The peak location where the stddev estimate was calculated is 
    # as good as any.
    try:
        guess_mean = cut_xdata[peak_index[np.argmax(cut_ydata[peak_index])]]
    except ValueError:
        # Just in case the guessing of peaks completely failed, 
        # this is an acceptable backup.
        guess_mean = cut_xdata[np.argmax(cut_ydata)]
    # The highest value is as good as any guess for the amplitude.
    try:
        guess_amplitude = cut_ydata[peak_index[
            np.argmax(cut_ydata[peak_index])]]
    except ValueError:
        # Just in case the guessing of peaks completely failed, 
        # this is an acceptable backup.
        guess_amplitude = np.nanmax(cut_ydata)

    # Return the guess.
    return guess_mean, guess_stddev, guess_amplitude