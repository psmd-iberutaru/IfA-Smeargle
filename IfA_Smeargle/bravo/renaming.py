
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

from IfA_Smeargle.meta import *


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


def voltage_pattern_rename_fits(data_directory, voltage_pattern, 
                                common_prefix='', common_suffix='',
                                rename=False, copy_data=True):
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
    common_prefix : string (optional)
        All file renames will contain this prefix before the voltage data.
    common_suffix : string (optional)
        All file renames will contain this suffix after the voltage data.
    rename : boolean (optional)
        If true, the program renames the files as specified, else, it leaves 
        the files untouched; still archived, however, if ``copy_data=True``.
    copy_data : boolean (optional)
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


    if (copy_data):
        # Warn just in case.
        smeargle_warning(TimeWarning,("Archiving and copying particularly a lot of large fits "
                                      "files may take a very long time. It is still suggested, "
                                      "but do outside Python. Disable via < copy_data=False >."))

        # Preserve the files just in case, work on a copy data set. Date-time 
        # to distinguish, by format __YYYYMMDD_HHMMSS, from other BravoArchives
        archive_name = 'BravoArchive' + time.strftime("__%Y%m%d_%H%M%S", time.localtime())
        shutil.make_archive(data_directory + '/../' + archive_name, 'zip', data_directory + '/')
        # For some reason, if the archive is made in the same directory, it 
        # recursively archives until its way too big. Making it outside then 
        # moving it is a workaround. 
        shutil.move(data_directory + '/../' + archive_name + '.zip', 
                    data_directory + '/' + archive_name + '.zip')
        print("Pure archive of data is stored in  < {arc_dir} >"
              .format(arc_dir=(data_directory + '/' + archive_name + '.zip')))

    # For the files to be renamed.
    original_names = glob.glob(data_directory + '/*.fits')
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
        
        
    # Compile the renames, assume that the sets repeat themselves if there 
    # are more files than voltages . Then actually rename the file.
    voltage_string_list = []
    for fileindex,filenamedex,pathdex in zip(range(n_files),original_names,original_paths):
        volt_string = (str(voltage_strings[fileindex%n_voltages]) 
                       + ',' + str(fileindex + 1).zfill(3))
        voltage_string_list.append(volt_string)
        
        # Renaming if needed.
        if (rename):
            renamed_file = (common_prefix + '__' + volt_string + '__' + common_suffix)
            os.rename(filenamedex, os.path.join(pathdex, renamed_file))

    # Finished.
    return voltage_string_list
    