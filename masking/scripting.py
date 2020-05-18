
"""
This contains the scripts of the masking functions.
"""
import numpy as np
import os
import string

import IfA_Smeargle.core as core
import IfA_Smeargle.masking as mask


# The scripts of the masks.
def script_mask_single_pixels(config):
    """ The scripting version of `mask_single_pixels`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_single_pixels'])
    # Extract the masking programs configuration parameters.
    column_indexes = core.config.extract_configuration(
        config_object=config, keys=['geometric','pixel_column_indexes'])
    row_indexes = core.config.extract_configuration(
        config_object=config, keys=['geometric','pixel_row_indexes'])

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_single_pixels

    # Compiling the arguments that the masking function uses.
    masking_arguments = {'column_indexes':column_indexes,
                         'row_indexes':row_indexes}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_rectangle(config):
    """ The scripting version of `mask_rectangle`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_rectangle'])
    # Extract the masking programs configuration parameters.
    column_range = core.config.extract_configuration(
        config_object=config, keys=['geometric','rectangle_column_range'])
    row_range = core.config.extract_configuration(
        config_object=config, keys=['geometric','rectangle_row_range'])

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_rectangle

    # Compiling the arguments that the masking function uses.
    masking_arguments = {'column_range':column_range,
                         'row_range':row_range}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_subarray(config):
    """ The scripting version of `mask_subarray`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_subarray'])
    # Extract the masking programs configuration parameters.
    column_range = core.config.extract_configuration(
        config_object=config, keys=['geometric','subarray_column_range'])
    row_range = core.config.extract_configuration(
        config_object=config, keys=['geometric','subarray_row_range'])

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_subarray

    # Compiling the arguments that the masking function uses.
    masking_arguments = {'column_range':column_range,
                         'row_range':row_range}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_columns(config):
    """ The scripting version of `mask_columns`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_columns'])
    # Extract the masking programs configuration parameters.
    column_list = core.config.extract_configuration(
        config_object=config, keys=['geometric','column_list'])

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_columns

    # Compiling the arguments that the masking function uses.
    masking_arguments = {'column_list':column_list}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_rows(config):
    """ The scripting version of `mask_rows`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_rows'])
    # Extract the masking programs configuration parameters.
    row_list = core.config.extract_configuration(
        config_object=config, keys=['geometric','row_list'])

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_rows

    # Compiling the arguments that the masking function uses.
    masking_arguments = {'row_list':row_list}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_nothing(config):
    """ The scripting version of `mask_nothing`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_nothing'])
    # Extract the masking programs configuration parameters.
    pass

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_nothing

    # Compiling the arguments that the masking function uses.
    masking_arguments = {}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

def script_mask_everything(config):
    """ The scripting version of `mask_everything`. This function 
    applies the mask to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels masked for this mask.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['geometric','run_mask_everything'])
    # Extract the masking programs configuration parameters.
    pass

    # The function that is being used to calculate the masks.
    masking_function = mask.mask_everything

    # Compiling the arguments that the masking function uses.
    masking_arguments = {}

    # Create masks within the data directory, provided the 
    # configuration.
    mask.base.create_directory_mask_file(data_directory=data_directory,
                                         mask_function=masking_function,
                                         mask_arguments=masking_arguments,
                                         mask_file_name=mask_file_name,
                                         recursive=recursive, 
                                         subfolder=subfolder,
                                         run=run_flag)

    # All done.
    return None

# The scripts of the filters.
def script_filter_sigma_value(config):
    """ The scripting version of `filter_sigma_value`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_sigma_value'])
    # Extract the filter programs configuration parameters.
    sigma_multiple = core.config.extract_configuration(
        config_object=config, keys=['filter','sigma_multiple'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_sigma_value

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'sigma_multiple':sigma_multiple}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_percent_truncation(config):
    """ The scripting version of `filter_percent_truncation`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_percent_truncation'])
    # Extract the filter programs configuration parameters.
    top_percent = core.config.extract_configuration(
        config_object=config, keys=['filter','top_percent'])
    bottom_percent = core.config.extract_configuration(
        config_object=config, keys=['filter','bottom_percent'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_percent_truncation

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'top_percent':top_percent, 
                        'bottom_percent':bottom_percent}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_pixel_truncation(config):
    """ The scripting version of `filter_pixel_truncation`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_pixel_truncation'])
    # Extract the filter programs configuration parameters.
    top_count = core.config.extract_configuration(
        config_object=config, keys=['filter','top_count'])
    bottom_count = core.config.extract_configuration(
        config_object=config, keys=['filter','bottom_count'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_pixel_truncation

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'top_count':top_count, 'bottom_count':bottom_count}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_maximum_value(config):
    """ The scripting version of `filter_maximum_value`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_maximum_value'])
    # Extract the filter programs configuration parameters.
    maximum_value = core.config.extract_configuration(
        config_object=config, keys=['filter','maximum_value'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_maximum_value

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'maximum_value':maximum_value}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_minimum_value(config):
    """ The scripting version of `filter_minimum_value`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_minimum_value'])
    # Extract the filter programs configuration parameters.
    minimum_value = core.config.extract_configuration(
        config_object=config, keys=['filter','minimum_value'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_minimum_value

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'minimum_value':minimum_value}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_exact_value(config):
    """ The scripting version of `filter_exact_value`. This function 
    applies the filter to the entire directory (or single file). It 
    also adds the tags to the header file of each fits file 
    indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','run_filter_exact_value'])
    # Extract the filter programs configuration parameters.
    exact_value = core.config.extract_configuration(
        config_object=config, keys=['filter','exact_value'])

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_exact_value

    # Compiling the arguments that the masking function uses.
    filter_arguments = {'exact_value':exact_value}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None

def script_filter_invalid_value(config):
    """ The scripting version of `filter_invalid_value`. This 
    function applies the filter to the entire directory (or single 
    file). It also adds the tags to the header file of each fits 
    file indicating the number of pixels filtered for this filter.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    filter_tag_name = core.config.extract_configuration(
        config_object=config, keys=['filter_tag_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])

    # Extract the run flag for this particular script.
    run_flag = core.config.extract_configuration(
        config_object=config, keys=['filter','filter_invalid_value'])
    # Extract the filter programs configuration parameters.
    pass

    # The function that is being used to calculate the masks.
    filter_function = mask.filter_invalid_value

    # Compiling the arguments that the masking function uses.
    filter_arguments = {}

    # Create the filters from the directory.
    mask.base.create_directory_filter_files(data_directory=data_directory,  
                                            filter_function=filter_function,
                                            filter_arguments=filter_arguments,
                                            filter_file_tag=filter_tag_name,
                                            recursive=recursive, 
                                            subfolder=subfolder,
                                            run=run_flag)
    # All done.
    return None



# The script versions of other masking utilities.
def script_synthesize_masks(config):
    """ The scripting version of `synthesize_masks`. This function 
    applies the mask to the entire directory (or single file). It
    combines the mask files from the data directory.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    mask_file_name = core.config.extract_configuration(
        config_object=config, keys=['mask_file_name'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])
    
    # If there is a sub-folder, then check the sub-folder itself as
    # default.
    data_directory = (core.strformat.combine_pathname(
        directory=[data_directory, 
                   core.runtime.extract_runtime_configuration(config_key='MASKING_SUBDIR')])
                      if subfolder else data_directory)

    # Obtain the list of masks that will need to be synthesized.
    mask_file_list = mask.base.get_mask_fits_filenames(
        data_directory=data_directory, recursive=recursive)

    # If there are no mask files, then inform and return with 
    # nothing.
    if (len(mask_file_list) == 0):
        core.error.ifas_error(core.error.ImportingError,
                              ("There are no mask files found in "
                               "`{data_dir}`. Recursive is {recur}. Nothing "
                               "shall be written, None is returned."
                               .format(data_dir=data_directory,
                                       recur=recursive)))
        return None

    # Extract the mask themselves.
    mask_data_list = []
    header_data_list = []
    for filedex in mask_file_list:
        __, temp_header, temp_data = core.io.read_fits_file(file_name=filedex, 
                                                            silent=True)
        header_data_list.append(temp_header)
        mask_data_list.append(np.array(temp_data, dtype=bool))

    # Combine all of the masks 
    synthesized_mask = mask.base.synthesize_masks(*mask_data_list) 

    # If the user didn't create a valid mask name, provide one 
    # for them.
    if ((len(str(mask_file_name)) == 0) or (mask_file_name is None)):
        # A valid name has not been provided, creating a random name.
        mask_file_name = 'SYNTHESIZED'
        core.error.ifas_warning(core.error.InputWarning,
                                ("A valid masking name has not been "
                                 "provided. The defined name `{def_name}` "
                                 "shall be used instead."
                                 .format(def_name=mask_file_name)))

    # Read out the mask file into the main data directory.
    mask_pathname = core.strformat.combine_pathname(
        directory=data_directory, file_name=mask_file_name, 
        extension=['.mask','.fits'])
    core.io.write_fits_file(file_name=mask_pathname, 
                            hdu_header=None, hdu_data=synthesized_mask, 
                            hdu_object=None, 
                            save_file=True, overwrite=True, silent=True)
    core.error.ifas_info("The `{mask_type}` mask has been written "
                         "to `{mask_path}`."
                         .format(mask_type='synthesized',
                                 mask_path=mask_pathname))

    return None

def script_synthesize_filters(config):
    """ The scripting version of `synthesize_masks`. This function 
    applies the filter to the entire directory (or single file). It
    combines the filter files from the data directory.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the global configuration parameters, including 
    # the directory.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    recursive = core.config.extract_configuration(
        config_object=config, keys=['recursive'])
    subfolder = core.config.extract_configuration(
        config_object=config, keys=['subfolder'])
    
    # Get all of the data fits file in the directory to work on.
    data_fits = core.io.get_fits_filenames(data_directory=data_directory, 
                                           recursive=recursive)

    # Get all of the filter files within this directory too.
    # sub-folder forces the filters into subdirectories which are 
    # custom made, so the recursive is forced True.
    if ((subfolder) and (not recursive)):
        core.error.ifas_info("The `recursive` flag is False but `subfolder` "
                             "is True. As filter scripts with sub-folders "
                             "allow custom sub-sub-folder names for each "
                             "filter, the `recursive` flag is forced True "
                             "for the searching of filter files.")
        defacto_recursive = True
    # Getting the filter files.
    filter_files = mask.base.get_filter_fits_filenames(
        data_directory=data_directory, recursive=defacto_recursive)

    # Compile and combine all of the filter files that used a given
    # data file as its base. We assume that it can be determined
    # from just name matching.
    for datafiledex in data_fits:
        # The real data array.
        __, hdu_header, hdu_data = core.io.read_fits_file(
            file_name=datafiledex, extension=0, silent=True)
        # The data filter, assume by default all pixels are good.
        hdu_filter = np.full_like(hdu_data, False)

        # Search through all filter files.
        for filterfiledex in filter_files:
            # Extract the base file names of these files to allow 
            # for comparison to ensure that the files use the same 
            # source data file.
            __, data_filename, __ = core.strformat.split_pathname(
                pathname=datafiledex)
            __, filter_filename, __ = core.strformat.split_pathname(
                pathname=filterfiledex)

            if (data_filename in filter_filename):
                # They have a large common name; they likely share 
                # the same data file. Read the fits in.
                __, filter_header, filter_data = core.io.read_fits_file(
                    file_name=filterfiledex, extension=0, silent=True)

                # Combine this filter with the other ones extracted.
                # Ignore the mask part, it works perfectly well with
                # filters.
                hdu_filter = mask.base.synthesize_masks(hdu_filter,
                                                        filter_data)
                # Move on to the next filter.


            else:
                # These files don't likely share the same data file.
                continue

        # Deriving the name of the filter file to be written. It 
        # changes depending on user's data directory and the 
        # sub-folder status.
        dir, file, ext = core.strformat.split_pathname(pathname=datafiledex)
        filter_dir_name = core.runtime.extract_runtime_configuration(
            config_key='FILTERING_SUBDIR')
        synth_filter_filename = core.strformat.combine_pathname(
            directory=([dir, filter_dir_name, 'FILTER_SYNTHESIZE'] 
                       if subfolder else [dir]), 
            file_name=[file, '__SYNTHESIZED'], extension=['.filter','.fits'])
        # Also check if the folder exists, if not, then make it.
        if (not os.path.isdir(core.strformat.combine_pathname(
            directory=([dir, filter_dir_name, 'FILTER_SYNTHESIZE'] 
                       if subfolder else [dir]) ))):
            # Creating the directory.
            os.makedirs(core.strformat.combine_pathname(
                directory=([dir, filter_dir_name, 'FILTER_SYNTHESIZE'] 
                       if subfolder else [dir])))

        # All of the filters have been added to the sum total. Save
        # the sum total.
        core.io.write_fits_file(file_name=synth_filter_filename, 
                                hdu_header=None, hdu_data=hdu_filter,
                                save_file=True, overwrite=False, silent=True)

    # All done.
    return None
