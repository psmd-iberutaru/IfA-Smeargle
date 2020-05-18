""" This module deals with the formatting and processing of strings
where either otherwise not provided or as a wrapper function
for convience.
"""

import copy
import os
import secrets
import shutil

import IfA_Smeargle.core as core

def purge_substrings(string, substrings):
    """ Deletes all occurences of any substring provided from the original
    string.

    Parameters
    ----------
    string : string
        The string to be purged of all substrings.
    substrings : string or list
        The substrings in a list, or a string by itself.

    Returns
    -------
    purged_string : string
        The string after it had all substring occurences taken out.    
    """
    # Just in case.
    original_string = copy.deepcopy(string)

    # Check if the substring is singular or is a list of substrings. 
    # It is better to handle a one long list.
    if (isinstance(substrings, str)):
        substrings = [substrings,]
    
    # Purge all substrings using the built-in replace method and going 
    # through.
    for substringdex in substrings:
        original_string = original_string.replace(substringdex, '')

    # Naming convention.
    purged_string = original_string
    return purged_string

def format_slice_appending_name(reference_frame, averaging_frame):
    """ The formatting for the string alignment for slices. """
    slice_string = ''.join(['_slice;', str(reference_frame[0]), ',', str(reference_frame[-1]), 
                            '-', str(averaging_frame[0]), ',', str(averaging_frame[-1])])
    return slice_string

def format_shutil_archive_extensions(archive_string):
    """ This function formats an extension and type string to 
    conform with shutil allowed extensions. This does not handle
    entire file names.

    Parameters
    ----------
    archive_string : string or boolean
        This is any version (either archive type or file extension)
        that is allowed under shutil archive maker.

    Returns
    -------
    archive_type : string
        The archive type that shutil allows for archive making.
    archive_extension : string
        The associated file extension that shutil allows.
    """
    # Do simple type checking and on if archiving is disabled.
    # Strict equality is needed as it may be a string or a boolean.
    if (archive_string == False):
        core.error.ifas_info("There was a call to format archive extensions "
                             "while the `archive_string` is False, implying "
                             "that archiving is disabled. Returning the "
                             "parameter without modification.")
        return archive_string
    elif (isinstance(archive_string, str)):
        # Really unneeded, but it is good to make sure.
        archive_string = str(archive_string)
    elif (archive_string == True):
        core.error.ifas_error("The `archive_string` is exactly True, the "
                              "allowance of the archiving functions tells "
                              "nothing about the format. Returning the "
                              "boolean.")
        return archive_string
    else:
        raise core.error.InputError("The `archive_string` must be a string "
                                    "loosely related to shutil archive "
                                    "formats, or a boolean.")

    # The list of all available archive types.
    all_arc_types = [typedex[0] for typedex in shutil.get_archive_formats()]
    all_arc_ext = [extdex[1][0] for extdex in shutil.get_unpack_formats()]

    # Loop through all of the types and extensions until one that
    # matches the input it given.
    for typedex, extdex in zip(all_arc_types, all_arc_ext):
        # A special exception for `tar` as there is overlap with 
        # other formats. So, strict checking is done before lazy
        # checking.
        if ((archive_string.strip().lstrip('.') == typedex) or
            (archive_string.strip().lstrip('.') == extdex)):
            # This is likely the match to the user's input. For 
            # naming convention.
            archive_type = typedex
            archive_extension = extdex
            return archive_type, archive_extension
    # Now doing lazy testing to see if it matches.
    for typedex, extdex in zip(all_arc_types, all_arc_ext):
        if ((archive_string in typedex) or (archive_string in extdex)):
            # This is likely the match to the user's input. For 
            # naming convention.
            archive_type = typedex
            archive_extension = extdex
            return archive_type, archive_extension

    # It should have found something, if not, then there is no match.
    raise core.error.InputError("The input string does not have any usual "
                                "association to any archive type or "
                                "extension from shutil:  {input_str}"
                                .format(input_str=archive_string))
    return None

def random_string(characters, length):
    """ This function returns a random string of characters of some length
    from a set of characters to use.

    Creit to: https://stackoverflow.com/a/23728630

    Parameters
    ----------
    characters : string
        The total avaliable characters to use. The order does not matter.
    length : int
        The length of the random string.

    Returns
    -------
    random_string : string
        The random string of proper length.    
    """

    # Basic type checking.
    length = int(length)
    characters = str(characters)
    # Implementing the random string generator found from the credited
    # link.
    random_string = ''.join(secrets.choice(characters) for __ in range(length))
    # All done
    return random_string


def split_pathname(pathname):
    """ This fuction splits a pathname into the directory, file, and extension
    names.
    
    Parameters
    ----------
    pathname : string
        The path that is to be split.

    Returns
    -------
    directory : string
        The directory component of the path.
    file_name : string
        The file name component of the path.
    extension : string
        The extension component of the path.
    """
    # Type checking.
    pathname = str(pathname)

    # Split the pathname into directory/filename.extension.
    directory = os.path.split(pathname)[0]
    file_name = os.path.splitext(os.path.split(pathname)[1])[0]
    extension = os.path.splitext(pathname)[1]

    return directory, file_name, extension

def combine_pathname(directory=None, file_name=None, extension=None):
    """ This is the opposite of splitting path names. 

    Parameters
    ----------
    directory : string or list (optional)
        This is the directory component that the path should be 
        attached to. If it is a list, the directory components are
        strung together in order.
    file_name : string or list (optional)
        This is the file name component that the path should be 
        attached to. If it is a list, the file name components are
        strung together in order.
    extension : string or list (optional)
        This is the extension component that the path should be 
        attached to. If it is a list, the extension components are
        strung together in order.
    
    Returns
    -------
    pathname : string
        The pathname that is created by combining the parts above.
    """
    # Combine the directories...
    directory = directory if directory is not None else ''
    directory = (directory if isinstance(directory, (list,tuple))
                 else [str(directory)])
    all_directory = os.path.join(*directory)
    # ...the file names...
    file_name = file_name if file_name is not None else ''
    file_name = (file_name if isinstance(file_name, (list,tuple))
                 else [file_name])
    all_filename = ''.join(file_name)
    # ...and the file extensions.
    extension = extension if extension is not None else ''
    extension = (extension if isinstance(extension, (list,tuple))
                 else [extension])
    all_extension = ''.join(extension)
    # Finally combine all of it into one part.
    pathname = os.path.join(all_directory, 
                            ''.join([all_filename, all_extension]))
    # All done.
    return pathname