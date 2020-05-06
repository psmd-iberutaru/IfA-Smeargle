
"""
This function computes all of the histogram information needed for
plotting.
"""

import numpy as np

import IfA_Smeargle.core as core



def analysis_heatmap(data_array, mask_array=None, filter_array=None, 
                     run=True):
    """ This generates the dictionary which is the results from the
    analysis of the data to create a heat-map of the data.

    Parameters
    ----------
    data_array : ndarray
        The array of data that will be used to compute the heat-map
        results.
    mask_array : ndarray (optional)
        The array of mask values to consider in the calculations.
        True values denote the mask is applied, False otherwise.
    filter_array : ndarray (optional)
        The array of filter values to consider in the calculations.
        True values denote the filter is applied, False otherwise.
    run : boolean (optional)
        If True, the analysis is run, else it is not and will exit
        with None.

    Returns
    -------
    heatmap_results : dictionary

    """
    # The data object to store the analysis.
    heatmap_results = {}

    # See if the analysis should even be run.
    if (not run):
        core.error.ifas_info("The `run` flag is False regarding heat-map "
                             "analysis. Nothing is done, the run flag "
                             "in the results is set to False.")
        heatmap_results['heatmap__run'] = False
        return heatmap_results
    # Continue with analysis.

    # The state on if or if not this function was ran.
    heatmap_results['heatmap__run'] = True
    # The data that the heat-map should use to be created.
    heatmap_results['heatmap__data_array'] = np.array(data_array)
    # The mask that the heat-map should also apply.
    heatmap_results['heatmap__mask_array'] = np.array(mask_array, dtype=bool)
    # The mask that the heat-map should also apply.
    heatmap_results['heatmap__filter_array'] = np.array(filter_array, 
                                                        dtype=bool)

    # All done.
    return heatmap_results






def script_analysis_heatmap(config):
    """
    
    
    """