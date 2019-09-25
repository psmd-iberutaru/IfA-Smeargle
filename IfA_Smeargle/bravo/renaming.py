
"""
This file contains methods used to determine proper naming conventions and
to reformat the fits file names from raw output  (often just timestamps) to
something more useful and accurate to the data.
"""


import copy
import glob
import numpy as np
import os 
import shutil
import time


from IfA_Smeargle import bravo
from IfA_Smeargle.meta import *


def filename_split_by_parameter(path_file_name, ignore_mismatch=False):
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



def parallel_renaming(file_names, file_renames, data_directory=None,
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


def voltage_pattern_rename_fits(data_directory, voltage_pattern, 
                                begin_garbage=0,
                                common_prefix='', common_suffix='',
                                rename=False, archive_data=True):
    """ Renames files according to their voltage pattern specified.

    Some data filename outputs only give timestamps. This function renames
    
    The output files created are according to the voltage pattern that the 
    user specified. This function assumes that the pattern provided is one 
    'set', where a set contains some amount of fits files. Moreover, this
    function weakly determines which are up-mid-down ramps. 

    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to be 
        renamed.
    voltage_pattern : array_like
        These are voltage values, assuming that the first element is the 
        first voltage element to be used, proceeding from there in order.
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count as data.
    common_prefix : string (optional)
        All file renames will contain this prefix before the voltage data.
    common_suffix : string (optional)
        All file renames will contain this suffix after the voltage data.
    rename : boolean (optional)
        If true, the program renames the files as specified, else, it leaves 
        the files untouched; still archived, however, if ``copy_data=True``.
    archive_data : boolean (optional)
        Execute the renaming on a copy of the data, the original data 
        is archived and preserved.

    Returns
    -------
    voltage_string_list : list
        This is the list of the voltage strings applied, given in a parallel 
        ordered form. Does not include prefixes/suffixes.

    """

    if (rename):
        smeargle_warning(DepreciationWarning,("The renaming method contained works as intended; "
                                              "however, it is not optimal and does not play "
                                              "nice with the other naming functions."))
    
    # Minor and fragile input sanitation.
    if (data_directory[-1] == '/'):
        data_directory = copy.deepcopy(data_directory[:-1])
    if ((common_suffix[-5:] != '.fits') and (rename)):
        common_suffix += '.fits'
        smeargle_warning(InputWarning, ("The < common_suffix > does not have a .fits extension; "
                                        "it has been automatically added."))

    # If the user wanted to preserve their data.
    if (archive_data):
        bravo.arc.duplicate_archive_data_files(data_directory)

    # The files that are before the garbage denotation should be labeled as
    # such.
    garbage_names = glob.glob(data_directory + '/*.fits')[:begin_garbage]
    garbage_paths = [os.path.split(garbagepathdex)[0] for garbagepathdex in garbage_names]
    n_garbage_files = len(garbage_names)


    # For the files to be renamed.
    original_names = glob.glob(data_directory + '/*.fits')[begin_garbage:]
    original_paths = [os.path.split(pathdex)[0] for pathdex in original_names]
    n_files = len(original_names)

    
    # Be able to handle the last case by looping back.
    n_voltages = len(voltage_pattern)
    voltage_strings = []
    for voltindex in range(n_voltages):
        temp_voltage_string = ''
    
        # Record the voltage number.
        temp_voltage_string += str(voltage_pattern[voltindex]) + 'V'
    
        # Detecting if the voltage is overall increasing, decreasing, or 
        # peaking. The odd modular division is to handle the last voltage 
        # effectively. 
        if (voltage_pattern[voltindex - 1] == voltage_pattern[voltindex] and 
            voltage_pattern[voltindex] == voltage_pattern[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are equal, this is a flat slope.
            temp_voltage_string += 'mid'
        elif (voltage_pattern[voltindex - 1] <= voltage_pattern[voltindex] and 
              voltage_pattern[voltindex] <= voltage_pattern[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are sloped upwards.
            temp_voltage_string += 'up'
        elif (voltage_pattern[voltindex - 1] >= voltage_pattern[voltindex] and 
              voltage_pattern[voltindex] >= voltage_pattern[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are sloped downwards.
            temp_voltage_string += 'down'
        elif (voltage_pattern[voltindex - 1] <= voltage_pattern[voltindex] and 
              voltage_pattern[voltindex] >= voltage_pattern[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are lower than this voltage.
            temp_voltage_string += 'top'
        elif (voltage_pattern[voltindex - 1] >= voltage_pattern[voltindex] and 
              voltage_pattern[voltindex] <= voltage_pattern[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are higher than this voltage.
            temp_voltage_string += 'bot'
        else:
            # For some reason, it does not fit into the pattern.
            temp_voltage_string += 'null'

        # Label, Windows does not like the colon or pipe, so, we use the 
        # next best thing.
        temp_voltage_string = 'detBias;' + temp_voltage_string


        # Save and record.
        voltage_strings.append(temp_voltage_string)

    # Compile the garbage files.
    garbage_string_list = []
    for fileindex, filenamedex, pathdex in zip(range(n_garbage_files),
                                               garbage_names, garbage_paths):
        garbage_string = 'Garbage' + str(fileindex + 1).zfill(3)
        garbage_string_list.append(garbage_string)

        # If renaming is needed.
        if (rename):
            os.rename(filenamedex,os.path.join(pathdex, garbage_string))
        
        
    # Compile the renames, assume that the sets repeat themselves if there 
    # are more files than voltages . Then actually rename the file.
    voltage_string_list = []
    for fileindex,filenamedex,pathdex in zip(range(n_files),original_names,original_paths):
        volt_string = str(voltage_strings[fileindex%n_voltages])
        # To prevent file name clashes
        if (rename):
            volt_string += (',' + str(fileindex + 1).zfill(3))
        voltage_string_list.append(volt_string)
        
        # Renaming if needed.
        if (rename):
            renamed_file = (common_prefix + '__' + volt_string + '__' + common_suffix)
            os.rename(filenamedex, os.path.join(pathdex, renamed_file))

    # Finished, it is also helpful to return the garbage file names.
    voltage_string_list = garbage_string_list + voltage_string_list

    return voltage_string_list
    