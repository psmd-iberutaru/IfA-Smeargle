
"""
This is where common functions to all of the analysis 
code is written to.
"""

import os
import copy
import numpy as np
import inspect

import ifa_smeargle.core as core
import ifa_smeargle.masking as mask

def create_filter_from_configuration(data_array, filter_config):
    """
    This function applies all of the filters that are written based 
    on the configurations supplied. 
    
    All filters are obtained automatically from the written code.
    If required configuration parameters are missing for any of the 
    filters, they are automatically skipped.

    Parameters
    ----------
    data_array : ndarray
        The data array by which the filters will be calculated from.
    filter_config : ConfigObj or dictionary-like
        The configuration that the filters will use.
    
    Returns
    -------
    filter_array : ndarray
        The filter, made of each of the individual filters as 
        calculated.
    """

    # Ensure that the data array is a real array; type check the 
    # configuration too for easy usage.
    data_array = np.array(data_array)
    filter_config = dict(filter_config)

    # The dictionary of all of the filters.
    filter_dict = core.runtime.get_filter_functions()

    # Loop through all of the filters, applying them as usual.
    filter_array_list = []
    for namedex, filterdex in copy.deepcopy(filter_dict).items():
        # Attempt to find the run parameter for this function.
        run_key = ''.join(['run_', namedex])
        if (run_key in filter_config):
            run_param = filter_config[run_key]
        else:
            run_param = False
            core.error.ifas_error(core.error.DevelopmentError,
                                  ("The filter `{name}` does not have the "
                                   "run parameter `{param_key}` in the "
                                   "configuration. The filter will be "
                                   "skipped as if it were False."
                                   .format(name=namedex,
                                           param_key=run_key)))

        # All valid parameters for this filter function, extracted.
        filter_args = {}
        valid_keys = [param.name for param 
                      in inspect.signature(filterdex).parameters.values() 
                      if param.kind == param.POSITIONAL_OR_KEYWORD]
        for keydex in valid_keys:
            # The data array is not really a configuration argument.
            if (keydex == 'data_array'):
                continue
            else:
                try:
                    filter_args[keydex] = filter_config[keydex]
                except TypeError:
                    core.error.ifas_warning(core.error.ConfigurationWarning,
                                            ("The configuration parameter "
                                             "{param} does not exist in the "
                                             "configuration. Skipping the "
                                             "{name} filter."
                                             .format(param=keydex, 
                                                     name=namedex)))
                    # This filter will be skipped.
                    run_param = False
                    continue


        # If the script should be run or not.
        if (not run_param):
            # It should not be run, moving on.
            core.error.ifas_info("Skipping the filter `{name}` because the "
                                 "run is False."
                                 .format(name=namedex))
            continue
        else:
            # Attempt to create a filter.
            temp_filter = filterdex(data_array=data_array, **filter_args)

        # Attach it to the rest of the filters.
        filter_array_list.append(temp_filter)

    # Combine all of the filters as they have finished.
    filter_array = mask.base.synthesize_masks(*filter_array_list)

    if (filter_array is None):
        # There were no filters applied, so, just provide a blank 
        # filter instead of nothing.
        filter_array = np.full_like(data_array, False)

    # All done.
    return filter_array

def create_filter_from_directory(data_file, filter_directory):
    """ This function extracts the filter from a filter directory that 
    corresponds to the data file.

    Parameters
    ----------
    data_file : string
        The name of the data file that is going to used as the 
        reference to find any matching filter files. All directory
        information is stripped.
    filter_directory : string
        The directory by which the filters within will be checked if 
        they match to the data file.

    Returns
    -------
    filter_array : ndarray
        The filter, made of each of the individual filters as 
        calculated.
    """

    # Find all of the filter files within the filter directory.
    filter_files = mask.base.get_filter_fits_filenames(
        data_directory=filter_directory, recursive=True)

    # See if the data file name matches any of the names of the 
    # filters.
    __, data_filename, __ = core.strformat.split_pathname(pathname=data_file)
    matching_filter_filenames = []
    for filedex in filter_files:
        # Extract only the file name, trim all directory and 
        # extension non-sense.
        __, filter_filename, __ = core.strformat.split_pathname(
            pathname=filedex)
        # Test if they have any common name.
        if (data_filename in filter_filename):
            # They files are likely a match,
            matching_filter_filenames.append(filedex)
        else:
            continue

    # If there are zero or more than 1 matching file, warn as it
    # cannot be determined which one is the valid one.
    if (len(matching_filter_filenames) == 0):
        core.error.ifas_warning(core.error.MaskingWarning,
                                "For the data file `{file}`, there were no "
                                "appropriate filter files in the directory "
                                "{dir} found. Returning None."
                                .format(file=data_file, dir=filter_directory))
        return None
    elif (len(matching_filter_filenames) == 1):
        # There is only one matching filter, as expected.
        __, __, filter_array = core.io.read_fits_file(
            file_name=matching_filter_filenames[0], silent=True)
        return filter_array
    elif (len(matching_filter_filenames) >= 1):
        # There seems to be more than one filters, it is not clear 
        # which one should be used.
        core.error.ifas_warning(core.error.ImportingWarning,
                                ("There is more than one likely associating "
                                 "filter file with this data file. Returning "
                                 "None."
                                 "Data file: {file}  "
                                 "Matching filters: {filters}."
                                 .format(file=data_file, 
                                         filters=matching_filter_filenames)))
        return None
    else:
        # The program should not reach here as it should have already
        # been caught above.
        raise core.error.BrokenLogicError("The length of the filter "
                                          "filenames is: {length}. The if "
                                          "statements did not catch it "
                                          "correctly."
                                          .format(length=len(
                                              matching_filter_filenames)))
    # The program should also not reach here.
    raise core.error.BrokenLogicError
    return None
    

def create_directory_analysis_files(data_directory, mask_file,
                                    filter_directory, filter_config_file, 
                                    analysis_function, analysis_parameters,
                                    run):
    """ This function is the common function to compute and save the 
    results of analysis functions.

    Parameters
    ----------
    data_directory : string
        The data directory by which all of data for the analysis
        is contained within.
    mask_file : string
        The mask, if desired, that will be applied to this analysis
        run.
    filter_directory : string
        The directory that has all of the synthesized filter files.
        If it does not exist, then the filters will be calculated if
        possible.
    filter_config_file : string
        The configuration file with the filtering parameters. This 
        is used if only the filter is calculated rather than read.
    analysis_function : function
        The analysis function that will be used to calculate the 
        analysis results.
    analysis_parameters : dictionary
        The dictionary for the arguments of the analysis function.
    run : boolean
        This is a flag to ensure that the analysis script should run.
        If it is False, it is not run. 

    Returns
    -------
    None
    
    """

    # The data files.
    data_files = core.io.get_fits_filenames(data_directory=data_directory)

    # Read the mask into file.
    try:
        __, __, mask_array = core.io.read_fits_file(file_name=mask_file, 
                                                    silent=True)
    except Exception:
        __, __, temp_data = core.io.read_fits_files(file_name=data_files[0],
                                                   silent=True)
        mask_array = np.full_like(temp_data, False)
        core.error.ifas_error(core.error.ConfigurationError,
                              ("The mask file `{file}` cannot be read into "
                               "memory. Check the previous error in the "
                               "stack. A False mask will be applied."
                               .format(file=mask_file)))

    # Loop through each file and compute and read back to a new 
    # analysis file.
    for filedex in data_files:
        # Load the data.
        __, hdu_header, hdu_data = core.io.read_fits_file(file_name=filedex,
                                                          silent=True)
        # Compute or find the appropriate filter file.
        if (os.path.isdir(filter_directory)):
            filter_array = create_filter_from_directory(
                data_file=filedex, filter_directory=filter_directory)
        elif (os.path.isfile(filter_config_file)):
            # Read the specification and configuration files.
            filter_spec = (core.runtime.get_specification_files().get(
                'masking_specification', None))
            filter_config_obj = core.config.read_configuration_file(
                config_file_name=filter_config_file, 
                specification_file_name=filter_spec)
            filter_config = dict(core.config.extract_configuration(
                config_object=filter_config_obj, keys=['filter']))
            # Calculate the filter.
            filter_array = create_filter_from_configuration(
                data_array=hdu_data, filter_config=filter_config)
        else:
            core.error.ifas_warning(core.error.MaskingWarning,
                                    ("The filter could not computed or "
                                     "found. A False filter will be "
                                     "applied."))
            filter_array = np.full_like(hdu_data, False)


        # Combine both the filter and the mask. 
        mask_filter_array = mask.base.synthesize_masks(mask_array, 
                                                       filter_array)

        # Compute the analysis for this data file.
        analysis_results = analysis_function(data_array=hdu_data, 
                                             mask_filter=mask_filter_array, 
                                             run=run,
                                             **analysis_parameters)

        # The saved analysis file, should be where masked values 
        # are NaN. Not the best way by Sparrow's account, but it is 
        # done either way.
        saved_data_array = np.where(mask_filter_array, np.nan, hdu_data)
        # The name of the data file.
        temp_dir, temp_file, temp_ext = core.strformat.split_pathname(
            pathname=filedex)
        saved_file_name = core.strformat.combine_pathname(
            directory=[temp_dir], 
            file_name=[temp_file], extension=['.analysis', temp_ext])


        # Save the analyzed fits file. The analysis values can be 
        # saved to the header.
        core.io.write_fits_file(file_name=saved_file_name, 
                                hdu_header=hdu_header, 
                                hdu_data=saved_data_array,
                                save_file=True, overwrite=False, silent=True)

        # Add the extra analysis information.
        core.io.append_astropy_header_card(file_name=saved_file_name, 
                                           header_cards=analysis_results, 
                                           comment_cards=None)

    # All done
    return None


def get_analysis_fits_filenames(data_directory, recursive=False):
    """ This function is to obtain all of the filter fits files 
    within the directory provided. Mask fits files are those that 
    have the extension `.analysis.fits`.
    
    In general, this is a wrapper function around the normal 
    fits file glob function adapted for filters. 

    Parameters
    ----------
    data_directory : string
        The data directory that the filter fits files will be 
        searched from.
    recursive : boolean (optional)
        If True, also search subdirectories for filter fits files.

    Returns
    -------
    analysis_fits_filenames : list
        The list of the analysis fits file names.
    """
    
    # Running to obtain the mask fits file list.
    analysis_fits_filenames = core.io.get_fits_filenames(
        data_directory=data_directory, sub_extension='.analysis', 
        recursive=recursive)
    return analysis_fits_filenames