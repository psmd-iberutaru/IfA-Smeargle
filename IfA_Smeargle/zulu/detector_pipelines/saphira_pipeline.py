
"""
This is the entire reduction method for the Saphria based infrared arrays.

"""
import glob
import numpy as np
import numpy.ma as np_ma
import warnings as warn

from IfA_Smeargle import bravo
from IfA_Smeargle import echo
from IfA_Smeargle import oscar
from IfA_Smeargle import yankee

from IfA_Smeargle.meta import *

def saphira_reduction_pipeline(data_directory, configuration_class):
    """This is the entire reduction and analysis pipeline for the SAPHRIA 
    arrays.

    This is the default reduction pipeline for the SAPHIRA array. The
    "outputs" are written to file(s) and arranged in their own directory 
    instead of a Python output, mostly because of the sheer number of outputs.

    Parameters
    ----------
    data_directory : string
        The data directory straight out of the SAPHIRA array. Data 
        preprocessing is internally handled.
    configuration_class : SmeargleConfig class
        The configuration class/options that go along with this reduction
        script. Must be a SmeargleConfig class instance.

    Returns
    -------
    nothing
    """

    # First, run the data reorganization program.
    bravo.bravo_execution_saphira(data_directory, configuration_class)

    
    # Apply the desired masks as needed. Although, the format provided by
    # the BRAVO line states that they should all be in the same directory.
    echo.echo_directory_execution(data_directory, configuration_class, 
                                  overwrite=True)


    # Re-reference the files. This is mostly to ensure any file name changes
    # are taken into account.
    data_files = glob.glob(data_directory + '/*.fits')
    for filedex in data_files:
        oscar_plot = oscar.multi.plot_single_heatmap_and_histogram(filedex, configuration_class)
        # Save the plot.
        file_name = filedex[:-5] + '__plot.pdf' # UPDATE
        plot_title = filedex[:-5] # UPDATE
        meta_plting.smeargle_save_figure_file(oscar_plot, file_name, title=plot_title)

    # That should be it.
    return None


def SA201907281826_reduction_pipeline(data_directory, configuration_class):
    """ This function is the reduction pipeline instructed on 2019-07-28, 
    18:26.

    This reduction line differs from the main branch significantly enough to
    warrant itself its own special function. Its variants are also listed here.
    
    Parameters
    ----------
    data_directory : string
        The data directory straight out of the SAPHIRA array. Data 
        preprocessing is internally handled.
    configuration_class : SmeargleConfig class
        The configuration class/options that go along with this reduction
        script. Must be a SmeargleConfig class instance. Default 
        configurations are stored in the Configuration_Archive

    Returns
    -------
    nothing
    """

    # Obtain parameters, else use hard coded default values.
    try:
        early_frame = configuration_class.ZuluConfig.SA201907281826['early_frame']
        ref_frame = configuration_class.ZuluConfig.SA201907281826['ref_frame']
        sub_avg_frames = configuration_class.ZuluConfig.SA201907281826['sub_avg_frames']
        frame_exposure = configuration_class.ZuluConfig.SA201907281826['frame_exposure']
        early_sigma = configuration_class.ZuluConfig.SA201907281826['early_sigma']
    except (AttributeError, KeyError):
        # Frame 4, account for 0-indexing.
        early_frame = 3

        # Frame index values provided by Don Hall.
        ref_frame = np.array([17,32], dtype=int)
        sub_avg_frames = np.array([(257,272), (513,528), (1025,1040), (2049,2064), (4097,4112)],
                                  dtype=int)

        # How long each frame was exposed for in seconds.
        frame_exposure = 5
        early_sigma = 2


    # Initial renaming of primary files.
    def _saphira_renaming(data_directory, configuration_class):
        # Just a inner function to store the new naming routine. 
        # Be adaptive as to which configuration class is given.
        provided_config = yankee.extract_proper_configuration_class(configuration_class,
                                                                    yankee.BravoConfig)

        # Determine the detector's name.
        if (isinstance(provided_config.detector_name,str)):
            detector_name = provided_config.detector_name
        elif (isinstance(provided_config.detector_name,dict)):
            try:
                detector_name = provided_config.detector_name['name']
            except KeyError:
                raise ConfigurationError("The detector name cannot be found in the "
                                         "configuration file. It must either be a string or a "
                                         "dictionary with the name value referenced by the key "
                                         "<name>.")
        else:
            raise ConfigurationError("The detector name cannot be found in the configuration "
                                     "file. It must either be a string or a dictionary with "
                                     "the name value referenced by the key <name>.")

        # Getting the voltage renames
        voltage_names = bravo.rename.voltage_pattern_rename_fits(
            data_directory, **provided_config.voltpat_rename_config)
        n_files = len(voltage_names)


        # Rename all of the files. The directory structure seems fine.
        final_names = []
        for index, detectdex, voltdex in zip(range(len(voltage_names)),
                                             [detector_name for index in range(n_files)],
                                             voltage_names):
            final_names.append(detectdex
                               + '__' + 'num;' + str(index + 1) 
                               + '__' + voltdex 
                               # + '__'
                               + '.fits')

        bravo.rename.parallel_renaming(None, final_names, data_directory, 
                                       file_extensions='.fits')

        return None
    
    # Run the renaming of the files.
    _saphira_renaming(data_directory, configuration_class)

    # Initial sanitization of files, such as improper or smaller than normal
    # file size.
    bravo.sanitize.same_file_size_sanitization(data_directory, method='largest')


    # Re-obtain file names.
    file_names = glob.glob(data_directory + '/*' + '.fits')
    for filedex in file_names:
        # Load fits file.
        hdul_file, hdu_header, hdu_data = meta_faa.smeargle_open_fits_file(filedex, silent=True)

        # Early frame masking.
        early_mask = echo.masks.echo170_gaussian_truncation(hdu_data[early_frame], early_sigma, 
                                                            bin_size=10,
                                                            return_mask=True)

        # Calculating the differing averaging frames.
        for subavedex in sub_avg_frames:
            # Deriving an alternate name.
            alt_name = (filedex[:-5] 
                        + '__' + str(subavedex[0]) + '-' + str(subavedex[1]) 
                        + '.fits')
            # Executing averaging and writing, saving the mask.
            hdu_to_be_written = bravo.avging.average_endpoints(filedex, ref_frame, subavedex, 
                                                               write_file=False,
                                                               alternate_name=alt_name)
            temp_header = hdu_to_be_written[0].header 
            temp_data = np_ma.array(hdu_to_be_written[0].data, mask=early_mask)
            meta_faa.smeargle_write_fits_file(alt_name, temp_header, temp_data, silent=True)

    # Re-obtain file names, again.
    file_names = glob.glob(data_directory + '/*' + '.fits')
    for filedex in file_names:

        # Extract the fits file, keeping track of the early mask and raw data.
        __, hdu_header, hdu_data = meta_faa.smeargle_open_fits_file(filedex, silent=True)
        raw_data = np_ma.getdata(hdu_data)
        early_mask = np_ma.getmaskarray(hdu_data)

        # Execute the main masks as specified by the EchoConfig.
        __, mask_dictionary = echo.echo_execution(hdu_data, configuration_class, silent=True)


        # Add an entry to the masking dictionary corresponding to the early 
        # mask.
        mask_dictionary['early_mask'] = early_mask

        # Make the final masked fits file.
        hdu_data = echo.numpy_masked_array(raw_data, None, masking_dictionary=mask_dictionary)

        # Write the files once more.
        meta_faa.smeargle_write_fits_file(filedex, hdu_header, hdu_data, silent=True)


    # Re-obtain file names, once again. This is unneeded and can be condensed
    # into the upper loop. However, the loops do not take too much more time
    # so the 'simplification' is likely worth it.
    file_names = glob.glob(data_directory + '/*.fits')
    for filedex in file_names:
        
        # Get rid of annoying 3dim issue with imshow
        __, __, hdu_data = meta_faa.smeargle_open_fits_file(filedex, silent=True)
        if (len(hdu_data.shape) >= 3):
            continue

        oscar_plot = oscar.multi.plot_single_heatmap_and_histogram(filedex, 
                                                                   configuration_class)
        # Save the plot.
        file_name = filedex[:-5] + '__plot.pdf' # UPDATE
        plot_title = filedex[:-5] # UPDATE
        meta_plting.smeargle_save_figure_file(oscar_plot, file_name, title=plot_title)

    # All finished
    return None 
