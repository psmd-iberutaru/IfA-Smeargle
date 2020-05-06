"""
This is the common functions that are used through the masking
modules.
"""

import numpy as np
import os
import string

import IfA_Smeargle.core as core
import IfA_Smeargle.masking as mask

def get_mask_fits_filenames(data_directory, recursive=False):
    """ This function is to obtain all of the mask fits files within
    the directory provided. Mask fits files are those that have the 
    extension `.mask.fits`.
    
    In general, this is a wrapper function around the normal 
    fits file glob function adapted for masks. 

    Parameters
    ----------
    data_directory : string
        The data directory that the mask fits files will be search 
        from.
    recursive : boolean (optional)
        If True, also search subdirectories for mask fits files.

    Returns
    -------
    mask_fits_filenames : list
        The list of the mask fits file names.
    """
    
    # Running to obtain the mask fits file list.
    mask_fits_filenames = core.io.get_fits_filenames(
        data_directory=data_directory, sub_extension='.mask', 
        recursive=recursive)
    return mask_fits_filenames

def get_filter_fits_filenames(data_directory, recursive=False):
    """ This function is to obtain all of the filter fits files 
    within the directory provided. Mask fits files are those that 
    have the extension `.filter.fits`.
    
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
    filter_fits_filenames : list
        The list of the filter fits file names.
    """
    
    # Running to obtain the mask fits file list.
    filter_fits_filenames = core.io.get_fits_filenames(
        data_directory=data_directory, sub_extension='.filter', 
        recursive=recursive)
    return filter_fits_filenames


def create_directory_mask_file(data_directory, mask_function, mask_arguments,
                               mask_file_name, recursive, subfolder):
    """ This function is the common function to create a mask 
    for the data within the data directory.

    Parameters
    ----------
    data_directory : string
        The data directory that contain the data which the mask are
        for.
    mask_function : function
        The masking function which contains the main code operations
        for creating the mask.
    mask_arguments : dictionary
        The dictionary for the arguments of the masking function.
    recursive : boolean (optional)
        If True, then the subdirectories of the data_directory will
        also be searched for data.
    subfolder : boolean (optional)
        If True, a sub-folder containing all of the masks will be 
        created. If it exists, then the masks are added to it.

    Returns
    -------
    None
    """

    # Inform the user about the mask that is being applied.
    param_str = '  '.join([''.join([str(keydex),'=',str(valuedex)]) 
                           for keydex, valuedex in mask_arguments.items()])
    core.error.ifas_info("The mask `{mask_type}` is being created. The "
                         "data directory is `{data_dir}`. The parameters "
                         "are:  {param}"
                         .format(mask_type=str(mask_function.__name__),
                                 data_dir=str(data_directory),
                                 param=param_str))

    # Get the file names of all of the fits data files.
    data_files = core.io.get_fits_filenames(data_directory=data_directory, 
                                            sub_extension=None, 
                                            recursive=recursive)

    # Masks only need to derive their shape based on one data frame
    # based on their size and shape. However, ensure that the size
    # and shape of all files are valid. Assume that the first data
    # file is always the correct one.
    core.error.ifas_info("Creating a mask based on the data shape of "
                         "{correct_file}. This is the first file obtained "
                         "and shall be dogmatically assumed correct."
                         .format(correct_file=data_files[0]))
    __, hdu_header, hdu_data = core.io.read_fits_file(
        file_name=data_files[0], extension=0, silent=True)
    correct_shape = hdu_data.shape
    correct_size = hdu_data.size
    # Loop through all others to test the other data arrays.
    for filedex in data_files:
        # Load the file temporarily.
        __, __, temp_data = core.io.read_fits_file(file_name=filedex,
                                                   extension=0, silent=True)
        if (temp_data.size != correct_size):
            # Inform the user that these files have different number
            # of data points.
            core.error.ifas_error(core.error.DataError,
                                  "The data file `{data_file}` has "
                                  "{data_pts} data points. The first, "
                                  "correct, data file has {correct_pts}. "
                                  .format(data_file=str(filedex),
                                          data_pts=temp_data.size,
                                          correct_pts=correct_size))
        if (temp_data.shape != correct_shape):
            # The two shapes of the data files are incorrect. As the 
            # masks themselves are based on dimensions, it cannot 
            # be ignored.
            raise core.error.DataError("The data file `{data_file}` has the "
                                       "shape: {data_shape}. The assumed "
                                       "correct shape is: {correct_shape}. "
                                       "A single uniform mask cannot be "
                                       "applied to data files with "
                                       "different dimensional shapes."
                                       .format(data_file=str(filedex),
                                               data_shape=temp_data.shape,
                                               correct_shape=correct_shape))
        

    # The files, if here, are of correct shape, and correct-enough 
    # size. Create the mask itself.
    data_mask = mask_function(data_array=hdu_data, **mask_arguments)
    # Astropy fits files do not like booleans, convert to 1/0
    int_data_mask = np.where(data_mask, 1, 0)


    # If the user didn't create a valid mask name, provide one 
    # for them.
    if ((len(str(mask_file_name)) == 0) or (mask_file_name is None)):
        # A valid name has not been provided, creating a random name.
        mask_file = core.strformat.random_string(
            string.ascii_lowercase, 8)
        core.error.ifas_warning(core.error.InputWarning,
                                ("A valid masking name has not been "
                                 "provided. The random name `{rand_name}` "
                                 "shall be used instead."
                                 .format(rand_name=mask_file)))
    else:
        # In the event that there is any path information within the 
        # mask file name; removing it and modify it to its proper 
        # form.
        __, mask_file, __ = core.strformat.split_pathname(
            pathname=mask_file_name)

    if (subfolder):
        # The masks are in a sub-folder.
        subfolder_dir = core.strformat.combine_pathname(
            directory=[data_directory, 
                       core.runtime.extract_runtime_configuration(
                           config_key='MASKING_SUBDIR')])
        if (not os.path.isdir(subfolder_dir)):
            # The mask directory doesn't exist, create one.
            core.error.ifas_info("The mask sub-folder does not exist. The "
                                 "sub-folder flag is True, creating a "
                                 "masking sub-folder at:  {mask_subfolder}."
                                 .format(mask_subfolder=subfolder_dir))
            os.mkdir(subfolder_dir)
        # Finally construct the new mask file name.
        mask_filename = core.strformat.combine_pathname(
            directory=[subfolder_dir], file_name=[mask_file], 
            extension=['.mask','.fits'])
    else:
        # Construct the mask file name without the sub-folder 
        # addition.
        mask_filename = core.strformat.combine_pathname(
            directory=[data_directory], file_name=[mask_file], 
            extension=['.mask','.fits'])
    

    # The mask file will be saved. However, the header information
    # is important.
    header_cards = {
        'MASKTYPE':str(mask_function.__name__),
        'N_MASKED':int(np.count_nonzero(data_mask)),
        'REF_FILE':str(data_files[0]),
        'MASKFILE':str(mask_file_name)
        }
    comment_cards = {
        'MASKNAME':'The name of the mask type this is.',
        'N_MASKED':'The number of pixels masked.',
        'REF_FILE':'The reference data file that this mask was derived from.',
        'MASKFILE':'The name of this mask file itself when created.'
        }
    # It is also helpful to include the configuration parameters 
    # for this mask.
    for keydex, valuedex in mask_arguments.items():
        header_cards[keydex] = valuedex
        comment_cards[keydex] = 'A configuration used for this mask.'


    # Write the file to disk, then the header information.
    core.io.write_fits_file(file_name=mask_filename, 
                            hdu_header=hdu_header, hdu_data=int_data_mask,
                            save_file=True, overwrite=False, silent=True)
    core.io.append_astropy_header_card(file_name=mask_filename, 
                                       header_cards=header_cards, 
                                       comment_cards=comment_cards)
    core.error.ifas_info("The `{mask_type}` mask has been written "
                         "to `{mask_path}`."
                         .format(mask_type=str(mask_function.__name__),
                                 mask_path=mask_filename))
    # All done.
    return None

def create_directory_filter_files(data_directory, filter_function, 
                                  filter_arguments, filter_file_tag, 
                                  recursive, subfolder):
    """ This function is the common function to create filters 
    for the data within the data directory.

    Parameters
    ----------
    data_directory : string
        The data directory that contain the data which the mask are
        for.
    filter_function : function
        The filtering function which contains the main code 
        operations for creating the filter.
    filter_arguments : dictionary
        The dictionary for the arguments of the filtering function.
    recursive : boolean (optional)
        If True, then the subdirectories of the data_directory will
        also be searched for data.
    subfolder : boolean (optional)
        If True, a sub-folder containing all of the masks will be 
        created. If it exists, then the filters are added to it.

    Returns
    -------
    None
    """
    # Inform the user about the filter that is being applied.
    param_str = '  '.join([''.join([str(keydex),'=',str(valuedex)]) 
                           for keydex, valuedex in filter_arguments.items()])
    core.error.ifas_info("The filter `{filter_type}` is being created. The "
                         "data directory is `{data_dir}`. The parameters "
                         "are:  {param}"
                         .format(filter_type=str(filter_function.__name__),
                                 data_dir=str(data_directory),
                                 param=param_str))

    
    # Get the file names of all of the fits data files.
    data_files = core.io.get_fits_filenames(data_directory=data_directory, 
                                            sub_extension=None, 
                                            recursive=recursive)
    
    # If the user didn't create a valid filter tag, provide one 
    # for them. It must be out of the loop to remain the same across
    # this run.
    if ((len(str(filter_file_tag)) == 0) or (filter_file_tag is None)):
        # A valid name has not been provided, creating a random name.
        filter_tag = core.strformat.random_string(
            string.ascii_lowercase, 8)
        core.error.ifas_warning(core.error.InputWarning,
                                ("A valid filter tag name has not been "
                                 "provided. The random name "
                                 "`{rand_name}` shall be used instead."
                                 .format(rand_name=filter_tag)))
    else:
        # In the event that there is any path information within  
        # the filter tag name; removing it and modify it to its 
        # proper form.
        __, filter_tag, __ = core.strformat.split_pathname(
            pathname=filter_file_tag)


    # Calculate the filter and save it to file, for each of the 
    # data files.
    for filedex in data_files:
        # Read the data file.
        __, hdu_header, hdu_data = core.io.read_fits_file(file_name=filedex, 
                                                          silent=True)

        # Compute the filter itself.
        data_filter = filter_function(data_array=hdu_data, **filter_arguments)
        # Astropy fits files do not like booleans, convert to 1/0
        int_data_filter = np.where(data_filter, 1, 0)


        # Generating the filter file name based on the need for 
        # sub-folders and the filter name.
        if (subfolder):
            # The filters are in a sub-folder.
            subfolder_dir = core.strformat.combine_pathname(
                directory=[data_directory, 
                           core.runtime.extract_runtime_configuration(
                               config_key='FILTERING_SUBDIR'), 
                           ''.join(['FILTER_',filter_tag])])
            if (not os.path.isdir(subfolder_dir)):
                # The filter directory doesn't exist, create one.
                core.error.ifas_info("The filter sub-folder does not exist. "
                                     "The sub-folder flag is True, creating "
                                     "a filtering sub-folder at:  "
                                     "{filter_subfolder}."
                                     .format(filter_subfolder=subfolder_dir))
                os.makedirs(subfolder_dir)
            # Finally construct the new mask file name.
            __, datafilename, __ = core.strformat.split_pathname(
                pathname=filedex)
            filter_filename = core.strformat.combine_pathname(
                directory=[subfolder_dir], 
                file_name=[datafilename, '__', filter_tag], 
                extension=['.filter','.fits'])
        else:
            # Construct the mask file name without the sub-folder 
            # addition.
            __, datafilename, __ = core.strformat.split_pathname(
                pathname=filedex)
            filter_filename = core.strformat.combine_pathname(
                directory=[subfolder_dir], 
                file_name=[datafilename, '__', filter_tag], 
                extension=['.filter','.fits'])


        # Compile the header file information for the filter. It 
        # is important for documentation.
        header_cards = {
            'FLTRTYPE':str(filter_function.__name__),
            'N_FLTRED':int(np.count_nonzero(data_filter)),
            'DATAFILE':str(filedex),
            'FLTRFILE':str(filter_filename)
            }
        comment_cards = {
            'FLTRTYPE':'The name of the filter type this is.',
            'N_FLTRED':'The number of pixels filtered out.',
            'DATAFILE':'The data file that this filter was calculated from.',
            'FLTRFILE':'The name of this filter file itself when created.'
            }
        # It is also helpful to include the configuration parameters 
        # for this filter.
        for keydex, valuedex in filter_arguments.items():
            header_cards[keydex] = valuedex
            comment_cards[keydex] = 'A configuration used for this filter.'

        # Write the file to disk, then the header information.
        core.io.write_fits_file(file_name=filter_filename, 
                                hdu_header=hdu_header, 
                                hdu_data=int_data_filter,
                                save_file=True, overwrite=False, silent=True)
        core.io.append_astropy_header_card(file_name=filter_filename, 
                                           header_cards=header_cards, 
                                           comment_cards=comment_cards)
        core.error.ifas_info("The `{filter_type}` mask for {data_file} has "
                             "been written to `{filter_path}`."
                             .format(filter_type=str(filter_function.__name__),
                                     data_file=str(filedex),
                                     filter_path=filter_filename))

    # All done
    return None


def synthesize_masks(*args, **kwargs):
    """ This is a function to combine many masks into one single mask.
    This argument does not take any keyword arguments. All of the
    masks must be the same size. (In general, the first mask is 
    considered the correct mask.)

    Parameters
    ----------
    *args : list
        This should be a collection of array based masks.
    **kwargs : dictionary
        This catches any keyword arguments sent through.

    Returns
    -------
    synthesized_mask : array
        The combined mask made of all of the inputted masks.
    """

    # Check for any keyword arguments. There should be none.
    if (len(kwargs) > 0):
        core.error.ifas_error(core.error.InputError,
                              ("There should be no keyword argument inputs. "
                               "They will be ignored when synthesizing the "
                               "masks."))
    # If there is only one input array, there is no real synthesis.
    if (len(args) == 0):
        core.error.ifas_error(core.error.InputError,
                              ("There are no input masks to synthesize, "
                               "returning None."))
        return None
    elif (len(args) == 1):
        core.error.ifas_warning(core.error.InputWarning,
                                ("There is only one input mask, "
                                 "synthesizing is not needed."))
        return np.array(*args, dtype=bool)
    else:
        # It is assumed that there are masks to synthesize.
        # Assume that the first mask is the correct size and shapes, 
        # and shall be the template.
        synthesized_mask = np.zeros_like(np.array(args[0]), dtype=bool)
        correct_size = synthesized_mask.size
        correct_shape = synthesized_mask.shape
        for maskdex, index in zip(args, range(len(args))):
            # Numpy conversion.
            mask_array = np.array(maskdex, dtype=bool)
            # Test for the size and shape.
            if (mask_array.shape != correct_shape):
                raise core.eroor.DataError("The {num}th mask is not the "
                                           "correct shape. "
                                           "Correct shape:  {corr_shp}"
                                           "Nth shape: {curr_shp}"
                                           .format(num=index,
                                                   corr_shp=correct_shape,
                                                   curr_shp=mask_array.shape))
            if (mask_array.size != correct_size):
                core.error.ifas_error(core.eroor.DataError, 
                                      ("The {num}th mask is not the correct "
                                       "size. Correct shape:  {corr_sze} "
                                       "Nth shape: {curr_sze}"
                                       .format(num=index, 
                                               corr_sze=correct_shape,
                                               curr_sze=mask_array.shape)))
            # Otherwise, combine the two masks.
            synthesized_mask = np.array((synthesized_mask + mask_array),
                                        dtype=bool)
        # Finished with synthesizing.
        return synthesized_mask

    # The program should not reach here as it should have been caught
    # by the else.
    raise core.error.BrokenLogicError
    return None
