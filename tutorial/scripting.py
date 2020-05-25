
"""
This is where all of the scripts that create different tutorials
for each different type of detector lies.
"""

import copy
import os
import time

import IfA_Smeargle.core as core
import IfA_Smeargle.tutorial as tutorial

def script_generate_saphria_tutorial(config):
    """ This function generates a tutorial directory for new users
    to experiment with.

    This script generates a tutorial for the SAPHRIA detectors and
    what kind of data they would spit out.

    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None    
    """
    # Extract global parameters.
    tutorial_directory = core.config.extract_configuration(
        config_object=config, keys=['tutorial_directory'])
    tutorial_creation_override = core.config.extract_configuration(
        config_object=config, keys=['tutorial_creation_override'])

    # Extract parameters dedicated to the generation of the
    # tutorial.
    number_of_fits_files = core.config.extract_configuration(
        config_object=config, keys=['generation','number_of_fits_files'])
    generation_mode = core.config.extract_configuration(
        config_object=config, keys=['generation','generation_mode'])
    fill_value = core.config.extract_configuration(
        config_object=config, keys=['generation','fill_value'])
    seed = core.config.extract_configuration(
        config_object=config, keys=['generation','seed'])
    minimum_range = core.config.extract_configuration(
        config_object=config, keys=['generation','minimum_range'])
    maximum_range = core.config.extract_configuration(
        config_object=config, keys=['generation','maximum_range'])
    data_shape = core.config.extract_configuration(
        config_object=config, keys=['generation','data_shape'])

    config_destination = core.config.extract_configuration(
        config_object=config, keys=['generation','config_destination'])

    # Compiling the configurations into forms recognized by the 
    # functions that they are used for.
    generation_range = [minimum_range, maximum_range]
    # If the configuration destination is not provided, then default 
    # to the tutorial directory. If it is invalid, let it raise an
    # error elsewhere.
    if ((isinstance(config_destination, str)) and 
        (len(config_destination) != 0)):
        config_destination = config_destination
    else:
        config_destination = tutorial_directory


    # First thing is to see if the tutorial directory exists, and,
    # if it does not, if it should be created.
    if (os.path.isdir(tutorial_directory)):
        # The directory exists, files may be overwritten, warn and
        # proceed if creation is mandated.
        if (tutorial_creation_override):
            core.error.ifas_error(core.error.InputError,
                                  ("The tutorial directory provided already "
                                   "exists. However, the creation flag is "
                                   "True so creation will continue. Files "
                                   "may be overwritten."))
            # Continue.
            pass
        else:
            # The directory exists, and the creation flag is not 
            # there to override.
            raise core.error.InputError("The tutorial directory provided "
                                        "already exists. The creation flag "
                                        "is False, no override will happen.")
    else:
        # It does not exist, so, it may be created based on the 
        # creation override.
        if (tutorial_creation_override):
            core.error.ifas_info("The tutorial directory does not exist. "
                                 "The creation flag is True, so, this makes "
                                 "sense. The directory will be created.")
            # Making the directory.
            os.makedirs(tutorial_directory)
        else:
            # The directory does not exist, and no override is 
            # provided for proper execution.
            raise core.error.InputError("The tutorial directory does not "
                                        "exist. The creation flag is False "
                                        "so the tutorial directory will not "
                                        "be made.")

    # Within the tutorial directory, make the fits data files.
    # Making a dedicated directory for the data.
    fits_data_directory = core.strformat.combine_pathname(
        directory=[tutorial_directory,'tutorial_data'])
    os.makedirs(fits_data_directory, exist_ok=True)
    # Creating the data files.
    for index in range(number_of_fits_files):
        # The seed itself doesn't need to be always the same number,
        # but for pseudo-random, it needs to be predictable. 
        # Incrementing it for every file ensures reproducible, but
        # not the same, fits files for more than one fits generation.
        used_seed = seed + index if isinstance(seed, (int,float)) else None

        # Generating a data file based on the configuration.
        hdu_object = tutorial.generation.tutorial_generate_fits_file(
            generation_mode=generation_mode, data_shape=data_shape,
            fill_value=fill_value, seed=used_seed, range=generation_range)
        # The fits file should also have a name that more or less 
        # simulates real data. SAPHRIA detectors use time-stamps for
        # sequential data images. Dummy timestamps should work fine.
        current_time = time.strftime("%Y%m%d_%H", time.localtime())
        random_minuite_second = core.strformat.random_string(
            characters='0123456', length=4)
        fits_file_name = ''.join([current_time, random_minuite_second])
        fits_path_name = core.strformat.combine_pathname(
            directory=[fits_data_directory], 
            file_name=[fits_file_name], extension=['.fits'])
        # Save the fits file 
        core.io.write_fits_file(
            file_name=fits_path_name, 
            hdu_header=None, hdu_data=None, hdu_object=hdu_object, 
            overwrite=tutorial_creation_override, silent=False)

    # All possible configuration files that have been created should 
    # also be copied over.
    # If the directory does not exist, create it if overriding is 
    # available.
    if (not os.path.isdir(config_destination)):
        if (tutorial_creation_override):
            core.error.ifas_info("The configuration destination does "
                                 "not exist. Creating it as the creation "
                                 "override is True.")
            # Create the directory(s) needed so that the 
            # configuration files may be copied into there.
            os.makedirs(config_destination)
        else:
            core.error.ifas_warning(core.error.InputWarning,
                                    "The configuration destination does "
                                    "not exist. The creation override "
                                    "False, the tutorial directory will be "
                                    "used instead.")
            config_destination = tutorial_directory

    for configkeydex, __ in core.runtime.get_configuration_files().items():
        # Each configuration may need a file name too. Prefixing them
        # with tutorial serves to indicate that they are for the 
        # tutorial. (Not that it really matters.)
        config_file_name = core.strformat.combine_pathname(
            file_name=['tutorial_', configkeydex])

        # Loop through and generate the configuration files for each
        # configuration type. It is automatically copied into the 
        # correct directory.
        tutorial.generation.tutorial_copy_configuration_file(
            config_type=configkeydex, destination=config_destination,
            file_name=config_file_name)

    # It should be all done.
    return None