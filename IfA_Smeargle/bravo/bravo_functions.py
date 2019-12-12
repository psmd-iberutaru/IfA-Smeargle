import copy
import glob
import numpy as np
import os 
import shutil
import time


from IfA_Smeargle import bravo
from IfA_Smeargle.meta import *


def bravo_filename_split_by_parameter(path_file_name, ignore_mismatch=False):
    """ Takes a standard file name made by the BRAVO class and splits it into
    a more workable dictionary.

    The filenames of each and every .fits file that comes from BRAVO contains 
    information. This functions allows for the extraction of the information
    based on the standard file name tags.

    Parameters
    ----------
    path_file_name : string
        The name of the file that is to be split.
    ignore_mismatch : boolean (optional)
        If true, this function will raise a warning rather than an error if 
        there is a parameter that is in the filename, but not processable in 
        the dictionary. Defaults to False.

    Returns
    -------
    file_dictionary : dictionary
        The dictionary that contains all of the file parameters.
    """
    # All that is needed is the actual data filename, not the entire path.
    file_name = copy.deepcopy(os.path.splitext(os.path.split(path_file_name)[-1])[0])

    # If the file is considered garbage, then it doesn't have any purpose 
    # being split upon.
    if (('garbage' in file_name.lower()) and (not ignore_mismatch)):
        smeargle_warning(InputWarning,("The filename has been marked as garbage. The splitting "
                                       "will yield good or bad information about a bad data "
                                       "set. Nothing will be done."))
        return None

    # Split by the BRAVO standard method of separating elements.
    split_filename = str(file_name).split('__')

    # The name of the detector is always the first element, the others are not
    # always the order.
    det_name = split_filename.pop(0)

    # Cycle through all of the other elements
    file_dictionary = {'detName': det_name}
    for paramdex in split_filename:
        # Data file number.
        if ('num' in paramdex):
            # Extract the data number knowing that the semicolon separates.
            datafile_num = int(paramdex.split(';')[-1])
            file_dictionary['num'] = datafile_num
        # Data set number.
        elif ('set' in paramdex):
            # Extract the data set number knowing that the semicolon separates.
            datafile_set = int(paramdex.split(';')[-1])
            file_dictionary['set'] = datafile_set
        # Detector voltage, return as a tuple of value and up.down,etc
        elif ('detBias' in paramdex):
            # Extract based on separators semicolon and the V for up,down,etc
            voltage = (paramdex.split(';')[-1]).split('V')
            file_dictionary['detBias'] = (float(voltage[0]), str(voltage[-1]))
        # The detector slice range.
        elif ('slice' in paramdex):
            # The subsection of data the data frame focuses on.
            slice_range = (paramdex.split(';')[-1]).split('-')
            file_dictionary['slice'] = (int(slice_range[0]), int(slice_range[-1]))
        # The element doesn't fit into the standard naming conventions of BRAVO.
        else:
            # The user likely knows this is the case, so, stopping is not 
            # warranted.
            if (ignore_mismatch):
                smeargle_warning(InputWarning,("The filename parameter <{param}> does not have "
                                               "a corresponding BRAVO line interpretation, it "
                                               "is being ignored as stipulated."
                                               .format(param=str(paramdex))))
            else:
                raise InputError("The filename parameter <{param}> does not have a "
                                 "corresponding BRAVO line interpretation, it cannot be "
                                 "processed."
                                 .format(param=str(paramdex)))

    # Always include the file name too for completeness.
    file_dictionary['filename'] = path_file_name

    # Finally return.
    return file_dictionary


def bravo_rename_parallel(file_names, file_renames, data_directory=None,
                          file_extensions='.fits'):
    """ Renames files provided parallel name arrays.

    Given two same length lists of file names, one pre-rename and one 
    post-rename, this function renames them accordingly. A directory is also
    an option, and the file name list will be derived from that.

    This only works for one type of file extension, or leave the string blank
    for all files.

    Parameters
    ----------
    file_names : array_like
        The list of the file names that is to be renamed.
    file_renames : array_like
        The list of the file names that are going to be used for the renaming
        process.
    data_directory : string (optional)
        A directory that contains all of the files that are going to be 
        renamed. Does not handle directories recursively. 
    file_extensions : string (optional)
        The file extension of the files that are going to be renamed. Defaults
        to a .fits file.

    Returns
    -------
    nothing
    """

    # Extraction of the directory if provided. Paths should be conserved.
    if (data_directory is not None):
        # For the files to be renamed.
        original_names = glob.glob(data_directory + '/*' + file_extensions)
        original_paths = [os.path.split(pathdex)[0] for pathdex in original_names]
        n_files = len(original_names)
        
        # Overwrite
        file_names = original_names

    # Check for length issues.
    if (len(file_names) != len(file_renames)):
        raise RuntimeError("The number of file names and the number of file renames are not "
                           "the same; therefore, these are not parallel arrays.")


    # Rename, the two cases are needed for the presence of the data directory
    # or not.
    if (data_directory is not None):
        for pathdex,filenamedex,filerenamedex in zip(original_paths,
                                                     file_names,
                                                     file_renames):
            # Check for automatic file name extension.
            if (filerenamedex[-len(file_extensions):] != file_extensions):
                os.rename(filenamedex, os.path.join(pathdex, filerenamedex + file_extensions))
            else:
                os.rename(filenamedex, os.path.join(pathdex, filerenamedex))
    else:
        for filenamedex,filerenamedex in zip(file_names,file_renames):
           # Check for automatic file name extension.
            if (filerenamedex[-len(file_extensions):] != file_extensions):
                os.rename(filenamedex, filerenamedex + file_extensions)
            else:
                os.rename(filenamedex, filerenamedex)

    return None

