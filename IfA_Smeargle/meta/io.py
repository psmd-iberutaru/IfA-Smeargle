"""

This module just adds some shortcut calling functions to functionality of plotting functions
and related methods. 

Although the implementation of the entire functionality module is supposed to be untouched,
it is still suggested that these functions be used over custom approaches when applicable. 

"""

import astropy as ap
import astropy.modeling as ap_mod
import numpy as np
import numpy.ma as np_ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sp_sig
import scipy.stats as sp_stat
import sys

from IfA_Smeargle.meta import *


def smeargle_open_fits_file(file_name, extension=0, 
                            null_min=-1e6, null_max=1e6,
                            silent=False):
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
    null_min : float (optional)
        The minimum value an element (pixel) in the file that will be 
        considered to be valid. Else, the containing frame may be flagged for 
        nullification. Defaults to -1e6.
    null_max : float (optional)
        The maximum value an element (pixel) in the file that will be 
        considered to be valid. Else, the containing frame may be flagged for 
        nullification. Defaults to +1e6.
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
        with smeargle_absolute_silence():
            return smeargle_open_fits_file(file_name, extension=extension)

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
            smeargle_warning(DataWarning,("This a 2D data frame with nan/null values. They "
                                          "will be kept; but, functions down the line may "
                                          "break."
                                          "\nFile name: {f_name} | 'Null' frames: {fr_list}."
                                          .format(f_name=file_name, fr_list=nan_frames)))
        elif (nan_index_data.shape[1] == 3):
            smeargle_warning(DataWarning,("This a 3D data frame with nan/null values. Frames "
                                          "with nan/null values have been completely nulled. "
                                          "\nFile name: {f_name}    Null frames: {fr_list}."
                                          .format(f_name=file_name, fr_list=nan_frames)))
            # Null all of the frames with null values.
            for framedex in nan_frames:
                hdu_data[framedex] = np.full_like(hdu_data[framedex], np.nan)
        else:
            raise DataError("The fits file exists, but is 1D or 4D+, this module cannot handle "
                            "such data.")

    # Check for unnaturally large or small values which are a glitch more 
    # than actual data. The values are provided by `null_min` and `null_max`.
    with np.errstate(invalid='ignore'):
        if (np.any(np.where(np.logical_or(null_min > hdu_data, 
                                          hdu_data > null_max)))):
            # For the values that are greater than the max, or less than the
            # min. There is also no need to have repeat index frame data.
            illegal_value_data = np.argwhere(np.logical_or(null_min > hdu_data, 
                                                           hdu_data > null_max))
            illegal_value_frames = np.unique(illegal_value_data.T[0])
            if (illegal_value_data.shape[1] == 2):
                smeargle_warning(DataWarning,("This a 2D data frame with +/- large values. They "
                                              "will be kept; but, functions down the line may "
                                              "easily break."
                                              "\nFile name: {f_name} | Nulled frames: {fr_list}."
                                              .format(f_name=file_name, 
                                                      fr_list=illegal_value_frames)))
            elif (illegal_value_data.shape[1] == 3):
                smeargle_warning(DataWarning,("This a 3D data frame with +/- large values. "
                                              "Frames with +/- large values have been "
                                              "completely nulled."
                                              "\nFile name: {f_name} | Nulled frames: {fr_list}."
                                              .format(f_name=file_name, 
                                                      fr_list=illegal_value_frames)))
                # Null all of the frames that have really big +/- values.
                for framedex in illegal_value_frames:
                    hdu_data[framedex] = np.full_like(hdu_data[framedex], np.nan)
            else:
                raise DataError("The fits file exists, but is 1D or 4D+, this module cannot "
                                "handle such data.")

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
            smeargle_warning(InputWarning,("The fits file contains an <IFASMASK> extension, "
                                           "a pixel mask created by this program. It will be "
                                           "applied to the data. The output data will be a "
                                           "Numpy Masked Array."))
            # Apply the mask.
            hdu_data = np_ma.array(hdu_data, mask=data_mask)
        else:
            hdu_data = np.array(hdu_data)

    # Finally return
    return hdul_file, hdu_header, hdu_data

def smeargle_write_fits_file(file_name, hdu_header, hdu_data,
                             hdu_object=None, save_file=True, overwrite=True,
                             silent=False):
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
        with smeargle_absolute_silence():
            return smeargle_write_fits_file(file_name, hdu_header, hdu_data,
                             hdu_object=hdu_object, save_file=save_file, overwrite=overwrite)


    # Check if the file name has a fits extension.
    if (file_name[-5:] != '.fits'):
        file_name += '.fits'
        smeargle_warning(InputWarning, ("The fits file name does not have a .fits extension; "
                                        "it has been automatically added."))

    # Create the main HDUL object to write the fits file.
    # Check for the hdu_object.
    if (isinstance(hdu_object,(ap_fits.PrimaryHDU,ap_fits.HDUList))):
        # Astropy can handle PrimaryHDU -> .fits conversion.
        hdul_file = hdu_object
    else:
        # Else, deal with the data.
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
        smeargle_warning(OutputWarning,("The data array provided has been detected to be a "
                                        "masked array. The mask is saved in the fits extension "
                                        "<IFASMASK>. The primary data is not affected."))


    # Check to see if the file exists, if so, then overwrite if provided for.
    if (os.path.isfile(file_name)):
        if (overwrite):
            # It should be overwritten, warn to be nice. 
            smeargle_warning(OverwriteWarning,("There exists a file with the provided name. "
                                               "Overwrite is true; the previous file will "
                                               "be replaced as provided."))
        else:
            # It should not overwritten at this point.
            raise ExportingError("There exists a file with the same name as the previous one. "
                                 "Overwrite is set to False, the new fits file cannot "
                                 "be written.")

    # Write, follow overwrite instructions, assume the user knows what they 
    # are doing. Return object.
    if (save_file):
        hdul_file.writeto(file_name, overwrite=overwrite)

    return hdul_file



def smeargle_save_figure_file(figure, file_name,
                              title=None, close_figure=True):
    """ This function just saves a figure to a file to a name provided.

    Because of some oddities with Matplotlib, saving a file within a function 
    and exiting said function (or overwriting in a loop its variable) with a 
    new figure causes two figures to be saved in parallel. This is very 
    memory intensive, so closing a saved figure is ideal.
    
    This function does it so the user or Smeargle lines do not need to care 
    about it.

    Parameters
    ----------
    figure : Matplotlib Figure
        This is the figure to be saved to a file.
    file_name : string
        This is the file string name for the figure to be saved. It should 
        already have the appropriate extension. If not, it defaults to pdf. 
    title : string (optional)
        This is the title for the figure plot. Although it can be added from 
        here, it is not advised.
    close_figure : boolean (optional)
        This specifies if the figure should be closed. Given that this 
        function is built for that, this should not be changed.

    Returns
    -------
    return_none : None
        Nothing

    Note
    ----
    The file type checking logic is not the smartest implementation.
    
    """

    # Warn about the build up of memory if the figure is not closed.
    if (not close_figure):
        smeargle_warning(MemoryWarning, ("The figure will not be released from RAM. An "
                                         "excessive amount of figures will be very memory "
                                         "intensive. Why this function is being used without "
                                         "its closing functionality is beyond Sparrow."))

    # Checking or applying file ending configuration.
    supported_file_types = figure.canvas.get_supported_filetypes()
    supported_file_types = list(supported_file_types.keys())
    if any(('.' + typedex) in file_name[-7:] for typedex in supported_file_types):
        # The there seems to be a supported file type already in here.
        pass
    else:
        # There does not seem to be an appropriate file extension. 
        # Add one (pdf).
        file_name += '.pdf'

    # Apply the title if provided, if the format isn't applicable, trash.
    if (title is not None):
        if (isinstance(title, str)):
            figure.suptitle(title)
        else:
            # Doesn't seem to be a string...
            smeargle_warning(InputWarning, ("The title parameter has been provided, but as it "
                                            "is not a string, it cannot be applied to the "
                                            "figure. The title will not be applied."))

    # Save to file then remove figure from RAM if specified.
    figure.savefig(file_name)
    if (close_figure):
        plt.close(figure)
        del figure

    return None

