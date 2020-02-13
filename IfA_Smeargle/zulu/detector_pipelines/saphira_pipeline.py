
"""
This is the entire reduction method for the Saphria based infrared arrays.

"""
import copy
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import os
import warnings as warn

from IfA_Smeargle import bravo
from IfA_Smeargle import echo
from IfA_Smeargle import oscar
from IfA_Smeargle import yankee
from IfA_Smeargle import zulu

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

    # Determine the detector's name.
    if (isinstance(configuration_class.BravoConfig.detector_name,str)):
        detector_name = configuration_class.BravoConfig.detector_name
    elif (isinstance(configuration_class.BravoConfig.detector_name,dict)):
        try:
            detector_name = configuration_class.BravoConfig.detector_name['name']
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
    number_names = bravo.rename.number_renaming(
        data_directory=data_directory, **configuration_class.BravoConfig.number_rename_config)
    set_names = bravo.rename.set_determinization_renaming(
        data_directory=data_directory, 
        **configuration_class.BravoConfig.set_determine_rename_config)
    voltage_names = bravo.rename.voltage_pattern_renaming(
        data_directory=data_directory, **configuration_class.BravoConfig.voltpat_rename_config)
    n_files = len(number_names)

    # Rename all of the files. The directory structure seems fine.
    final_names = []
    for numdex, setdex, detectdex, voltdex in \
        zip(number_names, set_names, [detector_name for index in range(n_files)], voltage_names):
        # Loop for the name of all files.
        final_names.append(detectdex
                           + '__' + numdex
                           + '__' + setdex
                           + '__' + voltdex 
                           # + '__'
                           + '.fits')
    bravo.bravo_rename_parallel(None, final_names, data_directory, file_extensions='.fits')

    # Process all of the files, grabbing the names first.
    fits_file_names = glob.glob(os.path.join(data_directory, '*.fits'))
    for filedex in fits_file_names:
        # Reading the file and providing it with its configuration file, the 
        # proper Zulu IfasDataArray class should always be used with 
        # pipelines.
        detector_frame = zulu.IfasDataArray(pathname=filedex, 
                                            configuration_class=configuration_class,
                                            blank=False)

        # Applying a premask, provided the defined premask parameters in 
        # the configuration class.
        early_mask = detector_frame.echo170_gaussian_truncation(
            frame=detector_frame.config.ZuluConfig.SA201907281826['early_frame'],
            sigma_multiple=detector_frame.config.ZuluConfig.SA201907281826['early_sigma'],
            bin_width=detector_frame.config.ZuluConfig.SA201907281826['early_bin_size'],
            mask_key='premask')        

        # The files now need to be split up according to their reference and 
        # analysis chunks.
        averaging_frames = copy.deepcopy(
            detector_frame.config.ZuluConfig.SA201907281826['averaging_frames'])
        for subframedex in averaging_frames:
            # Extracting a copy for analysis. The normal python deepcopy 
            # may have a bug that made this unusable.
            detector_subframe = detector_frame.deepcopy()

            # Taking the average of the frames provided in the configuration.
            __ = detector_subframe.median_endpoints_per_second(
                start_chunk=detector_subframe.config.ZuluConfig.SA201907281826['refrence_frame'],
                end_chunk=subframedex, 
                frame_exposure_time=detector_subframe.config.ZuluConfig.SA201907281826['frame_exposure'])
            # Updating the file name for differentiation and to record the 
            # chunk. Formatting must match the bravo format.
            detector_subframe.update_pathname(
                append_filename=''.join(['__', bravo.rename._string_format_slice(
                    reference_frame=detector_subframe.config.ZuluConfig.SA201907281826['refrence_frame'],
                    averaging_frame=subframedex)]))
            return {'sub':detector_subframe, 'orig':detector_frame}
            # Applying the next Gaussian mask on each subframe, using the 
            # configuration parameters.
            __ = detector_subframe.echo170_gaussian_truncation(
                sigma_multiple=detector_subframe.config.EchoConfig.echo170_config['sigma_multiple'],
                bin_size=detector_subframe.config.EchoConfig.echo170_config['bin_size'])
            # Compile and synthesize the early mask.
            __ = detector_subframe.echo_synthesize_mask_dictionary()
            __ = detector_subframe.echo_create_masked_array()


            # Create the heatmap and histogram plot, also write it to file.
            figure = detector_subframe.plot_single_heatmap_and_histogram(
                configuration_class=detector_subframe.config)
            meta_io.smeargle_save_figure_file(figure=figure, 
                                              file_name=''.join([detector_subframe.filedirectory,
                                                                 detector_subframe.filename, 
                                                                 "__plot.pdf"]),
                                              title=detector_subframe.filename)
            # Save the fits file. too.
            detector_subframe.write_fits_file()

            # Freeing memory
            del detector_subframe
        # Freeing memory.
        del detector_frame

    # All of the frame based analysis should be complete. Dark current
    # over voltage plots are next. 
    oscar.volt_plot.plotdir_dark_current_over_voltage(data_directory=data_directory, 
                                                      configuration_class=configuration_class)

    # All done.
    return None