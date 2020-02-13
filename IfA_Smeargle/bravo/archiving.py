
"""
The purpose of this file is to contain all of the data conservation methods 
that are used to ensure that modifications to data do not harm the original 
data. Of course, the usage of these methods usually involve creating a 
copy of data. The usage of these functions are optional.
"""

import shutil
import os
import time

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

    raise DeprecationError("Use BRAVO's version")


    # Warn just in case.
    smeargle_warning(TimeWarning,("Archiving and copying particularly a lot of large fits "
                                  "files may take a very long time. It is still suggested, "
                                  "but archive outside of Python. Disable archiving prosedures"
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
    if (archive_extension == 'gztar'):
        archive_extension = '.tar.gz'
    elif (archive_extension == 'bztar'):
        archive_extension = '.tar.bz2'
    elif (archive_extension == 'xztar'):
        archive_extension = '.tar.xz'

    # Proceed with the move.
    shutil.move(data_directory + '/../' + archive_name + '.' + archive_extension, 
                data_directory + '/' + archive_name + '.' + archive_extension)

    shutil.move(os.path.join(data_directory, '..', ''.join([archive_name, archive_extension]),
                os.path.join(data_directory, ''.join([archive_name, archive_extension]))))

    # Inform the user where the archive is (just in case).
    smeargle_info("Raw archive of data is stored in  < {arc_dir} >"
                  .format(arc_dir=os.path.join(data_directory, 
                                               ''.join([archive_name, archive_extension]))))

    return None
