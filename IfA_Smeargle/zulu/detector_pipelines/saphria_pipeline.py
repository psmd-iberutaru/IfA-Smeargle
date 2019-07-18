
"""
This is the entire reduction method for the Saphria based infrared arrays.

"""
import glob
import warnings as warn

from IfA_Smeargle import bravo
from IfA_Smeargle import echo
from IfA_Smeargle import oscar

from IfA_Smeargle.meta import *

def saphria_reduction_pipeline(data_directory, configuration_class):
    """This is the entire reduction and analysis pipeline for the SAPHRIA 
    arrays.

    This is the default reduction pipeline for the Saphria array. The
    "outputs" are written to file(s) and arranged in their own directory 
    instead of a Python output, mostly because of the sheer number of outputs.

    Parameters
    ----------
    data_directory : string
        The data directory straight out of the Saphria array. Data 
        preprocessing is internally handled.
    configuration_class : SmeargleConfig class
        The configuration class/options that go along with this reduction
        script. Must be a SmeargleConfig class instance.

    Returns
    -------
    nothing
    """

    # First, run the data reorganization program.
    bravo.bravo_execution_saphria(data_directory, configuration_class)

    
    # Apply the desired masks as needed. Although, the format provided by
    # the BRAVO line states that they should all be in the same directory.
    # Recursive is unneeded but still added.
    data_files = glob.glob(data_directory + '/*.fits')
    with warn.catch_warnings():
        # Limit warnings, the files should be overwritten and should also
        # have the mask contained within.
        warn.simplefilter("ignore", category=OverwriteWarning)
        warn.simplefilter("ignore", category=OutputWarning)

        # Loop over all files.
        for filedex in data_files:
            # Execute the mask; catch the dictionary, it is unneeded though.
            masked_array, __ = echo.echo_execution(filedex, configuration_class,
                                                   hushed=True)

            # Write the file, because masked arrays do not harm the original data
            # it is acceptable to overwrite. The Header should remain unchanged;
            # it is read and reused from the file itself. 
            temp_header = meta_faa.smeargle_open_fits_file(filedex)[1]
            meta_faa.smeargle_write_fits_file(filedex, temp_header, masked_array)



    # Re-reference the files. This is mostly to ensure any file name changes
    # are taken into account.
    data_files = glob.glob(data_directory + '/*.fits')
    for filedex in data_files:
        oscar_plot = oscar.multi.plot_single_heatmap_and_histogram(filedex, configuration_class)
        # Save the plot.
        file_name = filedex + '__plot.pdf' # UPDATE
        plot_title = filedex[:-5] # UPDATE
        meta_plting.smeargle_save_figure_file(oscar_plot, file_name, title=plot_title)

    # That should be it.
    return None