""" These are functions related to the reading, writing, and manipulation
of files (data, configuration, or otherwise).
"""

import astropy as ap
import astropy.io.fits as ap_fits
import numpy as np
import numpy.ma as np_ma
import copy
import time
import glob
import shutil
import os

import IfA_Smeargle.core as core

def get_subdirectories(directory):
    """ This returns a list of the immediate subdirectories of the
    provided directory.
    
    Credit: https://stackoverflow.com/a/59938961

    Parameters
    ----------
    directory : string
        The directory that subdirectories will be found from.

    Returns
    -------
    subdirectories : list
        The list of subdirectories.
    """
    # Finding all of the subdirectories.
    subdirectories = [filedex.path for filedex in os.scandir(directory) 
                      if filedex.is_dir()]
    return subdirectories


def archive_data_directory(data_directory, archive_name=None, 
                           archive_type='bztar', silent=False):
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
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.
        
    Returns
    -------
    archive_path : string
        The path of the archive file.
    """
    # The user doesn't want any warnings.
    if (silent):
        with core.error.ifas_absolute_silence():
            return archive_data_directory(data_directory=data_directory, 
                                          archive_name=archive_name,
                                          archive_type=archive_type, 
                                          silent=False)
    # Ensure that archiving is not disabled. Strict equality is 
    # because the archive type would normally be a string.
    if (archive_type == False):
        # There should be no archiving.
        core.error.ifas_info("A call has been made to the archiving "
                             "utility. However, archiving is disabled for "
                             "this particular call, exiting.")
        return data_directory

    # Warn just in case.
    core.error.ifas_warning(core.error.TimeWarning,
                            ("Archiving and copying particularly a lot of "
                             "large fits files may take a very long time. "
                             "It is still suggested, but archive outside "
                             "of Python."))

    # Preserve the files just in case, work on a copy data set. Date-time 
    # to distinguish, by format __YYYYMMDD_HHMMSS, from other BravoArchives 
    # if an original name has not been given.
    if (archive_name is not None):
        pass
    else:
        archive_name = 'IFAS_DataArchive' + time.strftime("__%Y%m%d_%H%M%S", time.localtime())
    
    # Extract the archive type and extension from the user input.
    arc_type, arc_ext = core.strformat.format_shutil_archive_extensions(
        archive_string=archive_type)

    # For some reason, if the archive is made in the same directory, it 
    # recursively archives itself and intended files until its way too big. 
    # Making it outside then moving it is a workaround.
    temp_dir = core.strformat.combine_pathname(
        directory=[data_directory, '..'], 
        file_name=archive_name)
    archive_path = core.strformat.combine_pathname(
        directory=[data_directory, ''], 
        file_name=archive_name, extension=arc_ext)
    # Create the archive of the data within the data directory.
    temp_archive_path = shutil.make_archive(temp_dir, arc_type,
                        core.strformat.combine_pathname(
                            directory=[data_directory, '']))
    # Proceed with the move.
    shutil.move(temp_archive_path, archive_path)

    # Inform the user where the archive is (just in case).
    core.error.ifas_info("Archive is stored in  < {arc_dir} >"
                         .format(arc_dir=archive_path))

    return archive_path

def dearchive_data_directory(archive_name, alternate_directory=None,
                             silent=False):
    """Unpacks a file archive of a copy of the data files contained 
    within an archive.
    
    This function unpacks an archive of a data directory. However, 
    note that this function generally takes a bit of time if there 
    are a lot of files or if the files are particularly large.

    Parameters
    ----------
    archive_name : string
        The name of the archive that is to be unpacked.
    alternate_directory : string
        The path that an alternate directory that the archive should 
        be unpacked it.
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.

    Returns
    -------
    unarchive_path : string
        The path of the archive file.
    """
    if (silent):
        with core.error.ifas_absolute_silence():
            return dearchive_data_directory(
                archive_name=archive_name, 
                alternate_directory=alternate_directory,
                silent=False)

    # Unpack the archive. Check if the user supplied an alternative
    # directory.
    if (alternate_directory is not None):
        shutil.unpack_archive(archive_name, alternate_directory)
    else:
        shutil.unpack_archive(archive_name)

    return None


def rename_by_parallel_replace(file_names, file_renames, directory=None):
    """ Renames files provided parallel name arrays. This only works for
    fits files.

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
    directory : string (optional)
        A directory that contains all of the files that are going to be 
        renamed. Does not handle directories recursively.

    Returns
    -------
    None
    """
    # Adapt for an added directory. The path join function cannot handle 
    # a NoneType, but it can deal with an empty string.
    directory = '' if (directory is None) else str(directory)
    file_names = [os.path.join(directory, filedex) for filedex in file_names]
    file_renames = [os.path.join(directory, filedex) for filedex in file_renames]

    # Check for length issues.
    if (len(file_names) != len(file_renames)):
        raise core.error.RuntimeError("The number of file names and the number of file "
                                      "renames are not the same; therefore, these are not "
                                      "parallel arrays.")

    # Loop through all file names, renaming each of them.
    for (filedex, refiledex) in zip(file_names, file_renames):
        # Check if the file exists.
        if (not os.path.isfile(filedex)):
            core.error.ifas_warning(core.error.RuntimeWarning,
                                    ("The file {file_name} does not exist and thus cannot be "
                                     "renamed. Moving on to the next file."
                                     .format(file_name=filedex)))
            continue
        else:
            # The file exists, rename.
            os.rename(filedex, refiledex)

    return None

def rename_by_parallel_append(file_names, appending_names, directory=None):
    """ This function renames all files by appending a string to their name.
    The file name extension is not modified.

    Parameters
    ----------
    file_names : array_like
        The list of the file names that is to be renamed.
    appending_names : array_like
        The list of the appending strings that are going to be used for 
        the renaming process.
    directory : string (optional)
        A directory that contains all of the files that are going to be 
        renamed. Does not handle directories recursively.

    Returns
    -------
    None
    """
    # Obtain the path names, combining the two inputs.
    directory = '' if directory is None else str(directory)
    path_names = [os.path.join(directory, filedex) for filedex in file_names]
    n_files = len(path_names)

    # Append the extry between the end of the file name and the extension
    # for all files.
    new_path_names = []
    for pathdex, appenddex in zip(path_names, appending_names):
        # Extract the new path parameters.
        dir, file, ext = core.strformat.split_pathname(pathname=pathdex)
        # The new file and path name.
        new_file = ''.join([file, '_',appenddex, ext])
        new_path = os.path.join(dir, new_file)
        # Add it to the rest.
        new_path_names.append(copy.deepcopy(new_path))
        # For reuseabiltity.
        del new_path

    # Rename, given the new file names by append. The directory has already 
    # been accounted for.
    rename_by_parallel_replace(file_names=file_names, file_renames=new_path_names, 
                               directory=None)
    # Done.
    return None

def get_fits_filenames(data_directory, sub_extension=None, recursive=False):
    """ This function is a wrapper function around the glob command to get
    all fits files.

    Parameters
    ----------
    data_directory : string
        The data directory that the fits files will be search for from.
    sub_extension : string (optional)
        This allows for the focus of obtaining fits files that 
        is only like a .subextension.fits file, depending on what
        the string `sub-extension` is.
    recursive : boolean (optional)
        If True, also search subdirectories for fits files.

    Returns
    -------
    fits_filenames : list
        The list of the fits file names.

    .. note::

        If `data_directory` is instead a valid fit file, then only that
        fit file is returned in a list. This allows scripts to only be run
        on single files. (Recursive must be False.)
    """
    # This is the entire extension that should be used, including 
    # the sub-extension. A basic test first.
    if (sub_extension is not None):
        if (str(sub_extension)[0] != '.'):
            core.error.ifas_warning(core.error.InputWarning,
                                    ("The sub-extension does not begin like "
                                     "an extension (with a `.`)."))
        extension = core.strformat.combine_pathname(
            extension=[str(sub_extension), '.fits'])
        #''.join([str(sub_extension), '.fits'])
    else:
        # Just stick to the default extension.
        extension = '.fits'

    # Allow a single fits file if the file is a valid fits file. 
    # This is to allow single file scripts rather than whole 
    # directory scripts.
    if ((not os.path.isdir(data_directory)) and (not recursive)):
        # It is not a directory, check if it is a fits file and then on.
        # Testing for existence and extension.
        if ((os.path.isfile(data_directory)) and 
             (core.strformat.split_pathname(pathname)[-1] == extension)):
            # If Astropy can deal with it, it should be good enough.
            try:
                ap_fits.info(data_directory, output=None)
                # It should be all well and good then.
                core.error.ifas_info("The data directory inputted is really just a single fits "
                                     "file: {file}. It will be handled and returned."
                                     .format(file=str(data_directory)))
                return [data_directory]
            except Exception:
                core.error.ifas_warning(core.error.InputWarning,
                                        ("The file input {file} is detected to be a .fits file. "
                                         "However, the Astropy module has issues with it. "
                                         .format(file=data_directory)))
    else:
        # Process the directory like normal and obtain the fits files.
        # os.path.join(data_directory, ''.join(['*', extension])), 
        dir_list = [data_directory, '**'] if recursive else [data_directory]
        fits_filenames = glob.glob(core.strformat.combine_pathname(
            directory=dir_list, file_name=['*'], extension=[extension]),
                                   recursive=recursive)

        # Check and warn for no files found.
        if (len(fits_filenames) == 0):
            core.error.ifas_warning(core.error.ImportingWarning,
                                   ("No fits files were obtained within the data directory:  "
                                    "{data_dir}."
                                    .format(data_dir=str(data_directory))))
        return fits_filenames

    # The code should not reach here.
    raise core.error.BrokenLogicError
    return None

def read_fits_file(file_name, extension=0, silent=False):
    """ A function to ensure proper loading/reading of fits files.

    This function, as its name, opens a fits file. It returns the Astropy HDU 
    file. This function is mostly done to ensure that files are properly 
    closed. It also extracts the needed data and header information from the 
    file.

    Parameters
    ---------- 
    file_name : string
        This is the path of the file to be read, either relative or absolute.
    extension : int or string (optional)
        The desired extension of the fits file. Defaults to primary structure. 
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.

    Returns
    -------
    hdu_file : HDULists
        The Astropy object representing the fits file.
    hdu_header : Header
        The Astropy header object representing the headers of the given file.
    hdu_data : ndarray
        The Numpy representation of a fits file data.
    """

    # The user doesn't want any warnings.
    if (silent):
        with core.error.ifas_absolute_silence():
            return read_fits_file(file_name, extension=extension)

    with ap_fits.open(file_name) as hdul:
        hdul_file = copy.deepcopy(hdul)
        
        # Just because just in case.
        hdul.close()
        del hdul

    # Read from the extension
    hdu_header = hdul_file[extension].header
    hdu_data = hdul_file[extension].data

    # For some reason, there are null problems and value problems with the 
    # data. Any and all frames that match the criteria are nulled out. Send
    # a warning.
    # Check first for nans.
    if (np.any(np.isnan(hdu_data))):
        # Test for bad or nan/null values. Of course, there is not need for repeat frames.
        nan_index_data = np.argwhere(np.isnan(hdu_data))
        nan_frames = np.unique(nan_index_data.T[0])
        # Check for 3D or 2D file.
        if (nan_index_data.shape[1] == 2):
            core.error.ifas_log_warning(core.error.DataWarning,
                                        ("This a 2D data frame with nan/null values. "
                                         "They will be kept; but, functions down the "
                                         "line may break."
                                         "\n    File name: {f_name} | 'Null' frames: {fr_list}."
                                         .format(f_name=file_name, fr_list=nan_frames)))
        elif (nan_index_data.shape[1] == 3):
            core.error.ifas_warning(core.error.DataWarning,
                                    ("This a 3D data frame with nan/null values. Frames with "
                                     "nan/null values have been completely nulled. "
                                     "\n    File name: {f_name} | Null frames: {fr_list}."
                                     .format(f_name=file_name, fr_list=nan_frames)))
            # Null all of the frames with null values.
            for framedex in nan_frames:
                hdu_data[framedex] = np.full_like(hdu_data[framedex], np.nan)
        else:
            raise core.error.DataError("The fits file exists, but is 1D or 4D+, this module "
                                       "cannot handle cleaning such data.")

    # Check if there is an IfA-Smeargle mask, if so, mutate data to a masked
    # array.
    try:
        data_mask = hdul_file['IFASMASK'].data
        # Because fits files do not handle boolean arrays, convert from the 
        # int 1/0 array in the file.
        data_mask = np.array(np.where(data_mask >= 1, True, False), dtype=bool)

    except KeyError:
        data_mask = None
    finally:
        if (data_mask is not None):
            # Inform that a mask has been found and is going to be used.
            core.error.ifas_info("The fits file contains an <IFASMASK> extension, "
                                 "a pixel mask created by this program. It will be "
                                 "applied to the data. The output data will be a "
                                 "Numpy Masked Array.")
            # Apply the mask.
            hdu_data = np_ma.array(hdu_data, mask=data_mask)
        else:
            hdu_data = np.array(hdu_data)

    # Finally return. Inform the sucessful reading.
    core.error.ifas_info("Successfully read {read_fits} into memory."
                   .format(read_fits=file_name))
    return hdul_file, hdu_header, hdu_data

def write_fits_file(file_name, hdu_header, hdu_data, hdu_object=None, 
                    save_file=True, overwrite=False, silent=False):
    """ A function to ensure proper writing of fits files.

    This function writes fits files given the data and header file. The 
    file name should be a complete path and must also include the file name.



    Parameters
    ----------
    file_name : string
        This is the path of the file to be written, either relative or 
        absolute.
    hdu_header : Header
        The Astropy header object representing the headers of the given file.
    hdu_data : ndarray
        The Numpy representation of a fits file data.
    hdu_object : Astropy HDUList (optional)
        An astropy HDUList object, if provided, this object takes priority 
        to be written, the rest are ignored.
    save_file : boolean (optional)
        If ``True``, then the fits file will be written to file, else, just
        the instance will be returned.
    overwrite : boolean (optional)
        If ``True``, if there exists a file of the same name, overwrite.
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.

    Returns
    -------
    hdul_file : Astropy HDUList
        The file object that was written to disk. If ``hdu_object`` was 
        provided, it is returned untouched.
    """

    # The user does not want any warnings.
    if (silent):
        with core.error.ifas_absolute_silence():
            return write_fits_file(file_name, hdu_header, hdu_data,
                                   hdu_object=hdu_object, save_file=save_file, 
                                   overwrite=overwrite)


    # Check if the file name has a fits extension.
    core.strformat.split_pathname(pathname=file_name)[2]
    if (core.strformat.split_pathname(pathname=file_name)[2] != '.fits'):
        file_name =  core.strformat.combine_pathname(file_name=file_name, 
                                                     extension='.fits')
        core.error.ifas_log_warning(core.error.InputWarning, 
                                    ("The fits file name does not have a .fits extension; "
                                     "it has been automatically added."))

    # Create the main HDUL object to write the fits file.
    # Check for the hdu_object.
    if (isinstance(hdu_object,(ap_fits.PrimaryHDU,ap_fits.HDUList))):
        # Astropy can handle PrimaryHDU -> .fits conversion.
        hdul_file = hdu_object
    else:
        # Else, deal with the data.
        # If the data is a boolean, then as FITS cannot handle 
        # booleans, convert to int.
        if (isinstance(np.ravel(hdu_data)[0], (bool, np.bool_))):
            hdu_data = np.where(hdu_data, 1, 0)
        # Writing to a fits HDU.
        hdu = ap_fits.PrimaryHDU(data=np.array(hdu_data), header=hdu_header)
        hdul_file = ap_fits.HDUList([hdu])

    # Check if the data is a masked array, if it is, extract the mask and save
    # it to write in an extension.
    if (isinstance(hdu_data,np_ma.MaskedArray)):
        # Get data mask and convert to int array; apparently fits files do not
        # work well with booleans.
        data_mask = np_ma.getmaskarray(hdu_data)
        data_mask = np.array(np.where(data_mask, int(1), int(0)), dtype=int)
        # Create the HDU object mask.
        data_mask_hdu = ap_fits.ImageHDU(data_mask, name='IFASMASK')
        hdul_file.append(data_mask_hdu)

        # Warn that the mask has been added.
        core.error.ifas_warning(core.error.DeprecatedWarning,
                                ("The usage of the <IFASMASK> extension to "
                                 "store masks is discouraged to storing it "
                                 "as a separate fits file."))
        core.error.ifas_info("The data array provided has been detected "
                             "to be a masked array. The mask is saved in "
                             "the fits extension <IFASMASK>. The primary "
                             "data is not affected.")


    # Check to see if the file exists, if so, then overwrite if provided for.
    if (os.path.isfile(file_name)):
        if (overwrite):
            # It should be overwritten, warn to be nice. 
            core.error.ifas_warning(core.error.OverwriteWarning,
                                    ("There exists a file with the provided name. "
                                     "Overwrite is true; the previous file will "
                                     "be replaced as provided."))
        else:
            # It should not overwritten at this point.
            raise core.error.ExportingError("There exists a file with the same name as the "
                                            "previous one. Overwrite is set to False, the new "
                                            "fits file cannot be written. File name: {f_name}"
                                            .format(f_name=file_name))

    # Write, follow overwrite instructions, assume the user knows what they 
    # are doing. Return object.
    if (save_file):
        core.error.ifas_info("Successfully wrote {read_fits} onto disk."
                       .format(read_fits=file_name))
        hdul_file.writeto(file_name, overwrite=overwrite)

    return hdul_file

def append_astropy_header_card(file_name, header_cards, comment_cards=None):
    """ This is a function to add header card entries into the header of a 
    fits file. This uses dictionaries to achieve said result.

    Parameters
    ----------
    file_name : string
        This is the path of the file to be written, either relative or 
        absolute.
    header_cards : dictionary
        The header entries to be added to the header file. Please note that
        the keys of the dictionary must be no more than 8 characters.
    comment_cards : dictionary (optional)
        The comment entries to be added to the header file. The keys of the 
        comment dictionary and the `header_cards` must line up.

    Returns
    -------
    hdul_file : Astropy PrimaryHDU
        The file object that was written to disk. If ``hdu_object`` was 
        provided, it is returned with its header changed..
    """
    # Sort the comment cards to the needed dictionary. If it is nothing, 
    # then blank is fine.
    comment_cards = comment_cards if isinstance(comment_cards, dict) else dict()

    # Add the entries.
    for keydex, valuedex in copy.deepcopy(header_cards).items():
        # Check that the entries are valid type based on the FITS 
        # specification. Astropy does this, but it is not as clear.
        if (isinstance(valuedex, (int, float, str))):
            # This is a valid and accepted type, write to the Header.
            ap_fits.setval(file_name, keydex, value=valuedex, 
                           comment=comment_cards.get(keydex,None))
        elif (isinstance(valuedex, bool)):
            core.error.ifas_log_warning(core.error.ExportingWarning,
                                        ("FITS Headers cannot store a boolean directly but "
                                         "can use T/F letters. The boolean has been "
                                         "converted."))
            # Convert to a fits proper type.
            converted_value = 'T' if valuedex else 'F'
            ap_fits.setval(file_name, keydex, value=converted_value, 
                           comment=comment_cards.get(keydex,None))
        else:
            core.error.ifas_warning(core.error.ExportingWarning,
                                    ("The header card key-value pair "
                                     "({key} = {value}) uses a value type "
                                     "of {value_type}. FITS Headers can "
                                     "only use numbers and ascii-strings. "
                                     "Converting it to a string."
                                      .format(key=keydex, value=str(valuedex), 
                                              value_type=type(valuedex))))
            # Convert to a fits proper type.
            converted_value = str(valuedex)

            # If the key, value and comment card entry is too big, 
            # (>=80) it is better to open and write the entire file 
            # for the CONTINUE card.
            card_length = (len(keydex) 
                           + len(str(converted_value)) 
                           + len(str(comment_cards.get(keydex,''))))
            if (card_length >= 80):
                __, hdu_header, hdu_data = read_fits_file(
                    file_name=file_name, extension=0, silent=True)
                # Change the header.
                hdu_header.set(keydex, converted_value, 
                               comment_cards.get(keydex,None))
                # Finally, over/re-write the file to save the change.
                write_fits_file(file_name=file_name, 
                                hdu_header=hdu_header, hdu_data=hdu_data, 
                                hdu_object=None,
                                save_file=True, overwrite=True, silent=True)
            else:
                ap_fits.setval(file_name, keydex, value=converted_value, 
                               comment=comment_cards.get(keydex,None))
    return None
        




