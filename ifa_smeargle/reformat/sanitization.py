
import copy
import glob
import numpy as np
import os

import ifa_smeargle.core as core


def sanitize_file_size(data_directory, method='largest', delete=False, 
                       exact_size=None):
    """ A function to clean the data directory of any file 
    abnormalities stemming from incomplete or over-complete files.

    It is often to have too large files or too small files in a data 
    set. These files hold no consequence for removal and would only 
    contaminate or crash the pipeline if they went through. The 
    good files are kept, and the bad files are deleted. This method 
    only affects ``.fits`` files.

    Parameters
    ----------
    data_directory : string
        The directory of the data that is to be sanitized with the 
        non-conforming files deleted.
    method : string (optional)
        The current available methods for determining the file size 
        that is proper.

            * 'largest'
                The largest ``.fits`` file is considered 
                to be the right file size (default).
            * 'smallest'
                The smallest ``.fits`` file is considered 
                to be the right file size.
            * 'exact'
                The ``.fits`` file that is exactly the 
                size specified.

    delete : boolean (optional)
        If True, then all bad files found by this method are deleted.
    exact_size : int (optional)
        The exact size a proper file size should be (unit is in 
        bytes). Only applied if the method used is `exact`

    Returns
    -------
    bad_file_list : list
        The list of all of the file names/paths that are flagged for 
        sanitization.
    """

    # Type checking the method, and ensuring that case does not 
    # matter for selection.
    method = str(method).lower()
    
    # Deciding on how to calculate the proper file size.
    proper_file_size = None
    if (method == 'largest'):
        # The largest fits file is the right one.
        data_files = core.io.get_fits_filenames(
            data_directory=data_directory, recursive=True)
        # Obtaining file sizes.
        file_sizes = []
        for filedex in data_files:
            file_sizes.append(os.path.getsize(filedex))
        file_sizes = np.array(file_sizes)
        # Largest file size.
        proper_file_size = np.nanmax(file_sizes)
    elif (method == 'smallest'):
        # The smallest fits file is the right one.
        data_files = core.io.get_fits_filenames(
            data_directory=data_directory, recursive=True)
        # Obtaining file sizes.
        file_sizes = []
        for filedex in data_files:
            file_sizes.append(os.path.getsize(filedex))
        file_sizes = np.array(file_sizes)
        # Largest file size.
        proper_file_size = np.nanmin(file_sizes)
    elif (method == 'exact'):
        # The file size should be exactly specified.
        if (exact_size is None):
            raise core.error.InputError("The method of file size "
                                        "sanitization is exact size. A "
                                        "size must be specified.")
        else:
            proper_file_size = int(exact_size)
    # None of the methods were valid, this likely means that the 
    # user did not input the correct method.
    else:
        raise core.error.InputError("The method provided does not exist or "
                                    "it cannot be understood in the form "
                                    "provided. Inputted method: {method}"
                                    .format(method=method))


    def find_improper_file_sizes(data_directory, proper_file_size):
        """ This is the main deleting method for removing the 
        improper file sizes.
        """

        # Obtaining only fits files for processing. 
        data_files = core.io.get_fits_filenames(
            data_directory=data_directory, recursive=True)

        # Assume all files are bad data files as the clean ones will 
        # be removed after, ensuring that no bad file is missed.
        bad_data_files = copy.deepcopy(data_files)

        # Run through all files, removing the file names that are 
        # valid, the rest to be deleted.
        for filedex in data_files:
            # Test for ideal file size, if so, remove from bad file 
            # list.
            if (os.path.getsize(filedex) == proper_file_size):
                bad_data_files.remove(filedex)
            else:
                # File is likely bad, note that it is a bad file.
                core.error.ifas_info(("The fits file {bad_fits} did not "
                                      "pass file size sanitation."
                                      .format(bad_fits=str(filedex))))

        return bad_data_files

    # Find the bad files.
    bad_data_files = find_improper_file_sizes(
        data_directory=data_directory, proper_file_size=proper_file_size)

    # Do basic checks before deleting the files to warn of 
    # inconsistencies.
    if (len(data_files) == len(bad_data_files)):
        core.error.ifas_warning(core.error.DataWarning,
                                ("All files within the given directory have "
                                 "been marked as bad by "
                                 "`sanitize_file_size`. Please double check "
                                 "parameters."))
    if (proper_file_size == 0):
        core.error.ifas_error(core.error.InputError,
                              ("The proper file size for "
                               "`sanitize_file_size` is 0 bytes."))
    # Next check if there were any bad files that were found in 
    # the first place.
    if (len(bad_data_files) == 0):
        core.error.ifas_info("Success! There were no bad files found "
                             "by `sanitize_file_size`.")
        # We can exit now, there is no need to continue.
        return bad_data_files
    elif (len(bad_data_files) >= 1):
        # There are some bad files.
        core.error.ifas_log_warning("The following files are flagged for "
                                    "sanitization by `sanitize_file_size`: "
                                    "\n {flagged_files} "
                                    .format(flagged_files='\n'.join(
                                        [str(filedex) 
                                         for filedex in bad_data_files])))
        # See if the user wanted them deleted.
        if (delete):
            core.error.ifas_info("Deleting flagged files.")
            _sanitize_files(file_list=bad_data_files)
        
        # Return the bad file list in the event they need to use it.
        return bad_data_files

    else:
        raise core.error.AssumptionError("There is no reason for the length "
                                         "of a list to be less than 0.")

    # The code should not have reached here as the bad files should
    # have already been returned.
    raise core.error.BrokenLogicError
    return None
        


def _sanitize_files(file_list):
    """ This function basically is a wrapper for deleting files that 
    are listed in a list.
    """

    # Copy just in case.
    file_list = copy.deepcopy(file_list)
    for filedex in file_list:
        # Deleting the files.
        os.remove(filedex)
    # Finished.
    return None


def script_sanitize_file_size(config):
    """ The scripting version of `sanitize_file_size`. This function 
    sanitizes the documents as prescribed by the configuration and 
    the inner function.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """

    # Extract the parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    method = core.config.extract_configuration(
        config_object=config, keys=['sanitization', 'filesize', 'method'])
    exact_size = core.config.extract_configuration(
        config_object=config, keys=['sanitization', 'filesize', 'exact_size'])
    delete = core.config.extract_configuration(
        config_object=config, keys=['sanitization', 'delete'])

    # Execute the inner function.
    __ = sanitize_file_size(data_directory=data_directory, method=method, 
                            delete=delete, exact_size=exact_size)

    # Finished
    return None
