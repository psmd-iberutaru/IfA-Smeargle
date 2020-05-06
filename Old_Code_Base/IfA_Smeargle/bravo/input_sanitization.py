
import copy
import glob
import numpy as np
import os

from IfA_Smeargle.meta import *


def same_file_size_sanitization(data_directory, method='largest'):
    """ A function to clean the data directory of any file abnormalities
    stemming from incomplete or over-complete files.

    It is often to have too large files or too small files in a data set.
    These files hold no consequence for removal and would only contaminate or
    crash the pipeline if they went through. The good files are kept, and the
    bad files are deleted. This method only affects ``.fits`` files.

    Parameters
    ----------
    data_directory : string
        The directory of the data that is to be sanitized with the 
        non-conforming files deleted.
    method : string (optional)
        The current available methods for determining the file size that is
        proper.

            * 'largest' : The largest ``.fits`` file is considered to be the 
                          right file size (default).
            * 'smallest' : The smallest ``.fits`` file is considered to be the 
                           right file size.
            * 'exact' : The ``.fits`` file that is exactly the size specified.


    Returns
    -------
    nothing
    """

    # Ensure there are fits files to use in the data directory.
    if (len(glob.glob(data_directory + '/*.fits', recursive=True)) == 0):
        raise DataError("There is no usable data to run. Please check that there are .fits "
                        "files in the data directory.")

    # Deciding on how to calculate the proper file size.
    proper_file_size = None
    if (method == 'largest'):
        # The largest fits file is the right one.
        data_files = glob.glob(data_directory + '/*.fits', recursive=True)
        # Obtaining file sizes.
        file_sizes = []
        for filedex in data_files:
            file_sizes.append(os.path.getsize(filedex))
        file_sizes = np.array(file_sizes)
        # Largest file size.
        proper_file_size = np.nanmax(file_sizes)
    elif (method == 'smallest'):
        # The smallest fits file is the right one.
        data_files = glob.glob(data_directory + '*.fits', recursive=True)
        # Obtaining file sizes.
        file_sizes = []
        for filedex in data_files:
            file_sizes.append(os.path.getsize(filedex))
        file_sizes = np.array(file_sizes)
        # Largest file size.
        proper_file_size = np.nanmin(file_sizes)

    # None of the methods were valid, this likely means that the user did not
    # input the correct method.
    else:
        # There are two different types of errors that it could be depending
        # on input.
        if (isinstance(method,str)):
            raise InputError("There is no method selection that matches the input. Please "
                             "check and try again.")
        else:
            # Assume the user wanted to execute the function more than the
            # mistaken input's error chance.
            smeargle_warning("The method input cannot be understood in its current form. "
                             "defaulting to the default.")
            return same_file_size_sanitization(data_directory)


    def delete_improper_file_sizes(data_directory, proper_file_size):
        """ This is the main deleting method for removing the improper file
        sizes.
        """

        # Obtaining only fits files for processing. 
        data_files = glob.glob(data_directory + '/*.fits', recursive=True)

        # Assume all files are bad data files as the clean ones will be 
        # removed after, ensuring that no bad file is missed.
        bad_data_files = copy.deepcopy(data_files)

        # Run through all files, removing the file names that are valid, the
        # rest to be deleted.
        for filedex in data_files:
            # Test for ideal file size, if so, remove from bad file list.
            if (os.path.getsize(filedex) == proper_file_size):
                bad_data_files.remove(filedex)
            else:
                # File is likely bad.
                pass

        # It wouldn't make any sense to remove the entire data directory,
        # something must be wrong.
        if (len(data_files) == len(bad_data_files)):
            raise DataError("It seems that all of the data files is considered to be bad and "
                            "should be deleted. Please check the proper_file_size criterion or "
                            "method of selection.")
        # ... nor would a file size of zero.
        if (proper_file_size == 0):
            raise InputError("It does not make sense to have a proper file size of 0 bytes.")
        # If raised, this means that none of the methods were chosen, but it
        # did not spit out an error before.
        if (proper_file_size is None):
            raise BrokenLogicError("None of the proper file size selection methods were "
                                   "chosen, nor was any errors to prevent it being passed "
                                   "were raised.")


        # Delete bad files. Also, log deletions.
        log_del_names = []
        log_del_sizes = []
        for badfiledex in bad_data_files:
            # Logging deletions
            log_del_names.append(badfiledex)
            log_del_sizes.append(os.path.getsize(badfiledex))

            os.remove(badfiledex)

        # Compile and write the log.
        message = str(
            ">>" "Improper File Size Sanitization, Deleted Files"
            "\n" "Proper file size = " + str(proper_file_size) + " bytes"
            "\n" "<Size, bytes>  |  Filename"
            "\n" "--------------------------"
            "\n" + ("\n".join(
                        ["<{size}> | {name}".format(size=s,name=n) 
                        for s,n in zip(log_del_sizes, log_del_names)]))
            )
        _log_sanitization(data_directory, message)

        return None
    # Execute the deleting of non-conforming files.
    output = delete_improper_file_sizes(data_directory, proper_file_size=proper_file_size)

    # There really shouldn't be anything.
    return output


def _log_sanitization(data_directory, message):
    """ This is a unified function for creating the sanitization log file.
    """

    # If file doesn't exist, make one and add header.
    if (not os.path.isfile(data_directory + "/ifas_sanitization.log")):
        with open(data_directory + "/ifas_sanitization.log", 'x') as logfile:
            logfile.write(
                ">>> IFAS Sanitization Log. \n"
                "This log just outlines which data files were removed from data \n"
                "sanitization, and which method was used to remove said files. \n"
                "\n\n\n"
                )
        # Write the actual log message.
        _log_sanitization(data_directory, message)
    else:
        with open(data_directory + "/ifas_sanitization.log", 'a') as logfile:
            logfile.write(message + "\n\n\n")
            