
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
    
    raise TerminalError("Use Bravo function version")

def parallel_renaming(file_names, file_renames, data_directory=None,
                      file_extensions='.fits'):
    raise TerminalError("Use Bravo function version")




def number_renaming(data_directory, begin_garbage=0, archive_data=True):
    """ Renames files according to their number in order.

    Some data filename outputs only give timestamps. This function renames
    said filenames for better processing.  
    
    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to be 
        renamed.
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count as data.
    archive_data : boolean (optional)
        Execute the renaming on a copy of the data, the original data 
        is archived and preserved.

    Returns
    -------
    number_string_list : list
        This is the list of the numbered strings applied, given in a parallel 
        ordered form. Does not include prefixes/suffixes.
    """

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

    # Each file number, separating the garbage and the non-garbage numbers.
    # There is no reason to lump the two together without denotation.
    garbage_numbers = [(index + 1) for index in range(n_garbage_files)]
    file_numbers = [(index + 1) for index in range(n_files)]

    # Converting the numbers to their new names. The 'garbage' prefix to the 
    # number is a standard. Any file with garbage in the name is not 
    # processed.
    garbage_string_list = ['num;garbage' + str(numdex) for numdex in garbage_numbers]
    file_string_list = ['num;' + str(numdex) for numdex in file_numbers]

    # The completed list.
    number_file_list = garbage_string_list + file_string_list

    return number_file_list


def set_determinization_renaming(data_directory, set_length, 
                                 begin_garbage=0, archive_data=True):
    """ Renames files according to their set number, as determined by the
    number of files in a set. Sets are assumed to be consecutive.

    Some data filename outputs only give timestamps. This function renames
    said filenames for better processing.  
    
    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to be 
        renamed.
    set_length : int 
        This is the length of a set. 
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count as data.
    archive_data : boolean (optional)
        Execute the renaming on a copy of the data, the original data 
        is archived and preserved.

    Returns
    -------
    set_string_list : list
        This is the list of the numbered strings applied, given in a parallel 
        ordered form. Does not include prefixes/suffixes.
    """

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

    # Each file number, separating the garbage and the non-garbage numbers.
    # There is no reason to lump the two together without denotation.
    garbage_numbers = [(index + 1) for index in range(n_garbage_files)]
    file_numbers = [(index + 1) for index in range(n_files)]

    # Converting the numbers to their new names. The 'garbage' prefix to the 
    # number is a standard. Any file with garbage in the name is not 
    # processed.
    garbage_string_list = ['set;garbage' + str((numdex-1)//set_length + 1) 
                           for numdex in garbage_numbers]
    file_string_list = ['set;' + str((numdex-1)//set_length + 1) 
                        for numdex in file_numbers]

    # The completed list.
    set_file_list = garbage_string_list + file_string_list

    return set_file_list


def voltage_pattern_renaming(data_directory, voltage_pattern, 
                             begin_garbage=0, archive_data=True):
    """ Renames files according to their voltage pattern specified.

    Some data filename outputs only give timestamps. This function renames
    said filenames for better processing.

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
    archive_data : boolean (optional)
        Execute the renaming on a copy of the data, the original data 
        is archived and preserved.

    Returns
    -------
    voltage_string_list : list
        This is the list of the voltage strings applied, given in a parallel 
        ordered form. Does not include prefixes/suffixes.

    """
    
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

    # Compile the garbage files. The garbage 'prefix' to the 
    # number is a standard. Any file with garbage in the name is not 
    # processed.
    garbage_string_list = []
    for fileindex, filenamedex, pathdex in zip(range(n_garbage_files),
                                               garbage_names, garbage_paths):
        garbage_string = 'garbage' + str(fileindex + 1).zfill(3)
        garbage_string_list.append(garbage_string)

    # Compile the renames, assume that the sets repeat themselves if there 
    # are more files than voltages . Then actually rename the file.
    voltage_string_list = []
    for fileindex,filenamedex,pathdex in zip(range(n_files),original_names,original_paths):
        volt_string = str(voltage_strings[fileindex%n_voltages])
        voltage_string_list.append(volt_string)

    # Finished, it is also helpful to return the garbage file names.
    voltage_string_list = garbage_string_list + voltage_string_list

    return voltage_string_list
    

def _string_format_slice(reference_frame, averaging_frame):
    """ The formatting for the string alignment for slices. """
    slice_string = ''.join(['slice;', str(reference_frame[0]), ',', str(reference_frame[-1]), 
                            '-', str(averaging_frame[0]), ',', str(averaging_frame[-1])])
    return slice_string