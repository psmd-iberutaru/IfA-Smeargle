
"""
This function computes all of the heat-map information needed for
plotting.
"""

import numpy as np
import os

import IfA_Smeargle.core as core
import IfA_Smeargle.analysis as analysis



def analysis_heatmap(data_array, mask_filter=None, run=True):
    """ This generates the dictionary which is the results from the
    analysis of the data to create a heat-map of the data.

    Parameters
    ----------
    data_array : ndarray
        The array of data that will be used to compute the heat-map
        results.
    mask_filter : ndarray (optional)
        The array of mask and filter values to consider in the 
        calculations. True values denote the mask/filter is applied, 
        False otherwise.
    run : boolean (optional)
        If True, the analysis is run, else it is not and will exit
        with None.

    Returns
    -------
    heatmap_results : dictionary
        The results of the heat-map analysis.

    """
    # The data object to store the analysis.
    heatmap_results = {}

    # See if the analysis should even be run.
    if (not run):
        core.error.ifas_info("The `run` flag is False regarding heat-map "
                             "analysis. Nothing is done, the run flag "
                             "in the results is set to False.")
        heatmap_results['heatmap_run'] = False
        return heatmap_results
    else:
        heatmap_results['heatmap_run'] = True
    # Continue with analysis.

    # In truth, there are no hard calculated values needed.
    pass

    # All done.
    return heatmap_results



def script_analysis_heatmap(config):
    """ This is the script form of `analysis_heatmap`. It does all 
    the needed calculations, saves the results as separate fits files
    and also saves parameters that are not easy to save in fits files.
    
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
        config_object=config, keys=['heatmap','heatmap_run'])

    # Extract parameters relevant to the computation of the analysis.
    pass
    # Packaging all of the parameters relevant to this computation.
    analysis_parameters = {}

    # Computation function.
    analysis_function = analysis_heatmap
    
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