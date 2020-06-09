"""
This function computes all of the histogram information needed for
plotting.
"""

import numpy as np
import numpy.ma as np_ma

import ifa_smeargle.core as core
import ifa_smeargle.analysis as analysis

def analysis_gaussian_histogram(data_array, bin_width, 
                                mask_filter=None, run=True):
    """ This generates the dictionary which is the results from the
    analysis of the data to create a heat-map of the data.

    Parameters
    ----------
    data_array : ndarray
        The array of data that will be used to compute the heat-map
        results.
    bin_width : float
        The bin width of the histogram bars.
    mask_filter : ndarray (optional)
        The array of mask and filter values to consider in the 
        calculations. True values denote the mask/filter is applied, 
        False otherwise.
    run : boolean (optional)
        If True, the analysis is run, else it is not and will exit
        with None.

    Returns
    -------
    histogram_results : dictionary
        The results of the histogram analysis.

    """
    # The data object to store the analysis.
    histogram_results = {}

    # See if the analysis should even be run.
    if (not run):
        core.error.ifas_info("The `run` flag is False regarding histogram "
                             "analysis. Nothing is done, the run flag "
                             "in the results is set to False.")
        histogram_results['histogram_run'] = False
        return histogram_results
    else:
        histogram_results['histogram_run'] = True
    # Continue with analysis.

    # Check that the bin-width is a usable value.
    if (bin_width <= 0):
        raise core.error.InputError("The bin width must be a positive "
                                    "non-zero number. It is currently: "
                                    "{bin_val}"
                                    .format(bin_val=bin_width))

    # Combine the data and the mask for better management.
    masked_data = np_ma.array(data_array, mask=mask_filter)

    # Calculate the histogram values.
    hist_values, hist_bins = np.histogram(
        masked_data.compressed(), 
        bins=core.math.generate_numpy_bin_width_array(
            data_array=masked_data.compressed(), bin_width=bin_width))
    
    # Save the histogram values to the results. The modified keys
    # are needed as Astropy Header cards cannot use both the HIERARCH 
    # and CONTINUE cards at the same time.
    histogram_results['HIST_BIN'] = str(hist_bins.tolist())
    histogram_results['HIST_VAL'] = str(hist_values.tolist())

    # Calculate the Gaussian fit values. The compressed function
    # allows the histogram to ignore masked values.
    gauss_funct, gauss_param = core.model.fit_histogram_gaussian_function(
        data_array=masked_data.compressed(), bin_width=bin_width)

    # Save the Gaussian values to the results.
    for keydex, paramdex in gauss_param.items():
        histogram_results.update({''.join(['histogram_', keydex]):paramdex})

    # The bin width is also important information for plotting.
    histogram_results['histogram_bin_width'] = bin_width

    # All done.
    return histogram_results


def script_analysis_gaussian_histogram(config):
    """ This is the script form of `analysis_gaussian_histogram`. 
    It does all the needed calculations, saves the results as 
    separate fits files and also saves parameters that are not 
    easy to save in fits files.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """

    # Extract the global parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file = core.config.extract_configuration(
        config_object=config, keys=['mask_file'])
    filter_directory = core.config.extract_configuration(
        config_object=config, keys=['filter_directory'])
    filter_config_file = core.config.extract_configuration(
        config_object=config, keys=['filter_config_file'])

    # Extracting the run parameter.
    run = core.config.extract_configuration(
        config_object=config, keys=['histogram','histogram_run'])

    # Extract parameters relevant to the computation of the analysis.
    bin_width = core.config.extract_configuration(
        config_object=config, keys=['histogram','bin_width'])
    # Packaging all of the parameters relevant to this computation.
    analysis_parameters = {'bin_width':bin_width}

    # Computation function.
    analysis_function = analysis_gaussian_histogram
    
    # Run the analysis off the common function
    analysis.base.create_directory_analysis_files(
        data_directory=data_directory, mask_file=mask_file, 
        filter_directory=filter_directory, 
        filter_config_file=filter_config_file,
        analysis_function=analysis_function, 
        analysis_parameters=analysis_parameters,
        run=run)
    

    # All done.
    return None