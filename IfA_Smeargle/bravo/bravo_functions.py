import copy
import glob
import numpy as np
import os 
import shutil
import time


from IfA_Smeargle import bravo
from IfA_Smeargle.meta import *


def bravo_archive_data_duplicates(data_directory, archive_name=None, 
                                  archive_extension='bztar'):
    """Creates a file archive of a copy of the data files contained within a
    directory.
    
    This function creates an archive of a data directory, preserving a copy
    of data. However, note that this function generally takes a bit of time
    if there are a lot of files or if the files are particularly large.

    Please note that this function archives recursively. Non-data files and 
    non-required files should not be in the a given Data directory.

    Parameters
    ----------
    data_directory : string
        The directory that the data is contained within.
    archive_name : string (optional)
        The name of the archive that is to be created. If not provided, a 
        default is provided that contains the time-stamp of its creation.
    archive_extension : string (optional)
        The extension of the archive. Note that only some archives are 
        supported. Default is ``bztar``. See 
        :py:func:`shutil.get_archive_formats` for more information on 
        available archive formats.

    Returns
    -------
    nothing
    """


    # Warn just in case.
    smeargle_warning(TimeWarning,("Archiving and copying particularly a lot of large fits "
                                  "files may take a very long time. It is still suggested, "
                                  "but archive outside of Python. Disable archiving procedures "
                                  "via < copy_data=False >."))

    # Preserve the files just in case, work on a copy data set. Date-time 
    # to distinguish, by format __YYYYMMDD_HHMMSS, from other BravoArchives 
    # if an original name has not been given.
    if (archive_name is not None):
        pass
    else:
        archive_name = 'IFAS_BravoArchive' + time.strftime("__%Y%m%d_%H%M%S", time.localtime())
    
    # For some reason, if the archive is made in the same directory, it 
    # recursively archives itself and intended files until its way too big. 
    # Making it outside then moving it is a workaround. 
    shutil.make_archive(os.path.join(data_directory, '..', archive_name), 
                        archive_extension, os.path.join(data_directory, ''))

    # Be adaptive for the tar based file extensions, the notation used for 
    # shutil is not exactly the same as the file extension. This is required
    # for the moving workaround.
    if (archive_extension == 'zip'):
        archive_extension = '.zip'
    elif (archive_extension == 'tar'):
        archive_extension = '.tar'
    elif (archive_extension == 'gztar'):
        archive_extension = '.tar.gz'
    elif (archive_extension == 'bztar'):
        archive_extension = '.tar.bz2'
    elif (archive_extension == 'xztar'):
        archive_extension = '.tar.xz'
    else:
        raise InputError("The archive extension type is not supported. Please change the "
                         "extension type to a supported archive format.")

    # Proceed with the move.
    shutil.move(os.path.join(data_directory, '..', ''.join([archive_name, archive_extension])),
                os.path.join(data_directory, ''.join([archive_name, archive_extension])))

    # Inform the user where the archive is (just in case).
    smeargle_info("Raw archive of data is stored in  < {arc_dir} >"
                  .format(arc_dir=os.path.join(data_directory, 
                                               ''.join([archive_name, archive_extension]))))

    return None


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
    if (path_file_name is None):
        raise InputError("The path does not exist, it doesn't make sense to call this function "
                         "on an non-existent path file name.")
    elif (not isinstance(path_file_name,str)):
        raise TypeError("The path must be a string detailing the path to the file name to "
                        "read and split into its parts.")

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
            file_dictionary['ref_slice'] = (int(slice_range[0].split(',')[0]),
                                            int(slice_range[0].split(',')[-1]))
            file_dictionary['slice'] = (int(slice_range[-1].split(',')[0]), 
                                        int(slice_range[-1].split(',')[-1]))
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
        # For the files to be renamed. os.path.join(data_directory, ''.join(['*', '.fits']))
        original_names = glob.glob(os.path.join(data_directory, ''.join(['*', '.fits'])))
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
                os.rename(filenamedex, os.path.join(pathdex, ''.join([filerenamedex, 
                                                                      file_extensions])))
            else:
                os.rename(filenamedex, os.path.join(pathdex, filerenamedex))
    else: 
        for filenamedex,filerenamedex in zip(file_names,file_renames):
           # Check for automatic file name extension.
            if (filerenamedex[-len(file_extensions):] != file_extensions):
                os.rename(filenamedex, ''.join([filerenamedex, file_extensions]))
            else:
                os.rename(filenamedex, filerenamedex)

    return None

