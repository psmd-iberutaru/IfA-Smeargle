
"""
This is used when multiple figures are to be plotted in one file or system.

"""

import matplotlib.pyplot as plt

from IfA_Smeargle.meta import *
from IfA_Smeargle import oscar

def plot_single_heatmap_and_histogram(data_array,
                                      figure_subplot_parameters={'figsize':(9,3.5), 'dpi':100},
                                      plot_heatmap_parameters={},
                                      plot_histogram_parameters={}):
    """ This extracts data from a single data array, plotting a histogram 
    and heatmap.

    This function attempts to plot both a histogram and a heatmap 
    side-by-side given a data array. Although all of the customizable 
    parameters may be sent via the dictionary, this is not the suggested 
    method if extreme customization of the figure is needed. However, if the 
    current arrangement is fine, then so too should this function be.

    Parameters
    ----------
    data_array : ndarray or string
        This is the data array that is expected to be analyzed and have 
        histograms made. It can also be a fits file if desired. 

    figure_subplot_parameters : dictionary <config>
        These are parameters that are passed straight into the subplot 
        routine to make the figure.
    plot_heatmap_parameters : dictionary <config>
        These are parameters that are passed directly into 
        :py:function:`~.plot_array_heatmap_image`.
    plot_histogram_parameters : dictionary <config>
        These are parameters that are passed directly into 
        :py:function:`~.plot_array_histogram`.

    Returns
    -------
    final_figure : Matplotlib Figure
        This is the final figure made of the heatmap and the histogram.
    """

    # Extract proper data.
    data_array = oscar.oscar_funct.oscar_convert_data_inputs(data_array)


    # Generate the figure, also use the user's specifications.
    fig, ax = plt.subplots(1, 2,**figure_subplot_parameters)

    # Plotting both figures in their respective areas side by side. 
    # Again, use user specifications.
    oscar.heatmaps.plot_array_heatmap_image(data_array, 
                                            figure_axes=ax[0], **plot_heatmap_parameters)
    oscar.histograms.plot_array_histogram(data_array, 
                                          figure_axes=ax[1], **plot_histogram_parameters)
    
    # The histogram feels squished unless the axes ratios are modified.
    ax[1].set_aspect(1/(ax[1].get_data_ratio() * 1.5))

    # Visual modifications and cleanup to the final figure.
    fig.tight_layout()
    fig.subplots_adjust(right=0.9)

    # Only done for naming conventions on the documentation.
    final_figure = fig

    return final_figure
