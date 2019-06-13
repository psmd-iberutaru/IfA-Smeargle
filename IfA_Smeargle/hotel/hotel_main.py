"""
    The main objective of the HOTEL line is to create plots and histograms displaying and 
    categorizing different elements of arrays and specifically defined sub-arrays.

    Most of the procedures derived from this module element is derived from 
    https://github.com/tinowells/ifa, as an extension and generalization of said project. 
"""

import astropy as ap
import astropy.io.fits as ap_fits
import astropy.modeling as ap_mod
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp


def open_fits_file(file_name, extension=0):
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


def extract_subarray(primary_array,x_bounds,y_bounds):
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
        An array containing only data within the xy bounds provided.
    
    """

    # Be verbose in accepting revered (but valid) bounds.
    x_bounds = np.sort(x_bounds)
    y_bounds = np.sort(y_bounds)

    sub_array = primary_array[y_bounds[0]:y_bounds[-1],x_bounds[0]:x_bounds[1]]

    return np.array(sub_array)


def plot_array_histogram(data_array, 
                         figure_axes=None, 
                         histogram_plot_paramters={'bins':50, 'range':[-10,10]}):
    """ A function to create and plot histogram plots for better analysis of a given array.

    This function replicates the histogram plotting functionality of Tino Well's program. 
    (Found here: https://github.com/tinowells/ifa). More specifically, it attempts to plot 
    histograms of pixel data; then, the program attempts to fit a Gaussian function. 

    Parameters
    ----------
    data_array : ndarray
        This is the data array that is expected to be analyzed and have histograms made. 
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have the histogram plot 
            to. This defaults to either making new ones, or using the currently defined axes.

    histogram_plot_parameters : dictionary
        This is options the user may use to pass customization parameters into the histogram plot
        functionality. 

    Returns:
    --------
    histogram_plot_axes : Matplotlib Axes
        This is the histogram plot made on the (provided, borrowed, or generated) plotting axes. 
    gaussian_fit_atributes : dictionary
        This is a dictionary of the mean, stddev, amplitude, and maximum of the computed/fit 
        Gaussian model.

    """

    # First, figure out what type of Matplotlib axes to use.
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()

    # Derive histogram data, and double as plotting functionality.
    hist_data = ax.hist(data_array.flatten(), label='Counts Histogram', **histogram_plot_paramters)
    hist_x = (hist_data[1][0:-1] + hist_data[1][1:]) / 2 # Derive middle of bin.
    hist_y = hist_data[0]
    # Personally, I do not find this helpful.
    ax.plot(hist_x,hist_y, label='Counts')

    # Plotting/fitting the Gaussian function.  For some reasons beyond what I can explain, Astropy
    # seems to have better fitting capabilities in this specific application than Scipy.
    gaussian_init = ap_mod.models.Gaussian1D(amplitude=1., mean=0, stddev=1.)
    gaussian_fit_model = ap_mod.fitting.LevMarLSQFitter()
    gaussian_fit = gaussian_fit_model(gaussian_init, hist_x, hist_y)
    # For better plotting resolution.
    temp_gauss_x_axis = np.linspace(histogram_plot_paramters['range'][0] - 1, 
                                    histogram_plot_paramters['range'][-1] + 1,
                                    hist_x.size * 10)
    ax.plot(temp_gauss_x_axis, gaussian_fit(temp_gauss_x_axis), 
            linewidth=2.5, color='black', label='Gaussian')

    # Deriving basic information form Gaussian model to return back to the user.
    gaussian_mean = gaussian_fit.mean.value
    gaussian_stddev = gaussian_fit.stddev.value
    gaussian_amplitude = gaussian_fit.amplitude.value
    gaussian_max = np.max(gaussian_fit(temp_gauss_x_axis))
    gaussian_fit_atributes = {'mean': gaussian_mean, 'stddev': gaussian_stddev,
                              'amplitude': gaussian_amplitude,'max' : gaussian_max}

    # Center line and +/- 1 or 2 sigma vertical lines.
    mean_stddev_lines = gaussian_mean + gaussian_stddev * np.array([-2,-1,0,1,2])
    line_patterns = ['dotted','dashed','solid','dashed','dotted']
    for linedex, patterndex in zip(mean_stddev_lines, line_patterns):
        ax.axvline(x=linedex,linestyle=patterndex, color='red', alpha=0.5)
    # Gaussian peak value horizontal line.
    ax.axhline(y=gaussian_max, color='red', alpha=0.5)

    # Basic axis labels.
    ax.set_xlabel('Pixel Values')
    ax.set_ylabel('Count Quantity')


    # That should be it.
    return ax, gaussian_fit_atributes