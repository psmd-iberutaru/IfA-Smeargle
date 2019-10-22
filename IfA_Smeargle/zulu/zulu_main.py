"""
The ZULU line is the final cumulation of all other lines, in a way, it is
the script that dictates how the data should be manipulated. Each array
type has its own functional line, while each subset of these arrays should
contain their own configuration file (from Yankee). 

Each functional line is contained within their own file.

The reduction of the arrays should not generally call the upper lines. 
Each line should be called within a Zulu function, allowing for the 
consistency and ease of usage of the IfA Smeargle module. Changes should
only be applied to the configuration classes.
"""

import copy
import inspect
import numpy as np
import numpy.ma as np_ma
import types

from IfA_Smeargle import bravo
from IfA_Smeargle import echo
from IfA_Smeargle import oscar
from IfA_Smeargle import yankee

from IfA_Smeargle.meta import *

class IfasDataArray():
    """ This data frame class is a wrapper object around a data array image.
    For the directory version of this class, see 
    :class:`IfasDirectoryDataArray`.

    The purpose of this class is to make easier the development of pipelines 
    and the general flow of the manipulations of data arrays. However, because
    this is a wrapper function, not all functionality is guaranteed. For 
    more basic and known reductions, pipelines are still preferred (see 
    :doc:`ZULU pipelines <python_docstrings/IfA_Smeargle.zulu.detector_pipelines>`)
    
    New pipelines, however, should always be developed using this object
    oriented approach. 

    Arguments
    ---------
    A shit ton

    """

    def __init__(self, filename, configuration_class=None,
                blank=False):
        """ This initializes a data array by reading a fits file from storage.
        
        A fits file is required, it is expected to conform to the IFAS naming
        conventions imposed upon by the 
        :doc:`BRAVO module <python_docstrings/IfA_Smeargle.bravo>`)
        system. 

        Parameters
        ----------
        filename : string
            The name of the fits file that is to be read.
        configruation_class : SmeargleConfig class (optional)
            The appropriate configuration class that is tied to this data 
            array.
        blank : boolean (optional)
            If a completely blank class is instead desired. Please note no 
            function (except for i/o functions) will likely work.
        """

        # Extract the data from the fits file, unless they wanted it blank.
        if (blank):
            self.fits_file = None
            self.fits_header = None
            self.fits_data = None
            self.fits_rawdata = None
            self.fits_datamask = None
            smeargle_warning(InputWarning,("The data array file is indicated to return a blank "
                                           "one. Doing so as requested."))
        else:
            # Read the fits file data.
            hdul_file, hdu_header, hdu_data = meta_faa.smeargle_open_fits_file(filename)
            self.fits_file = hdul_file
            self.fits_header = hdu_header
            self.fits_data = hdu_data

            # Extract the mask and separate it from the data to hold the 
            # raw data values. Ternary operator for the change in 
            # representation of a mask.
            self.fits_rawdata = np_ma.getdata(hdu_data)
            self.fits_datamask = (np_ma.getmask(hdu_data) 
                                  if np_ma.getmask(hdu_data) is not np_ma.nomask else None)

        # Hold the configuration class also.
        if (configuration_class is not None):
            self._raw_configuration_class = configuration_class
        else:
            smeargle_warning(InputWarning,("There is no configuration class provided for this "
                                           "array. The attribute will be None."))

        # Though these may seem like copies, these are the intended mutable 
        # versions of the previous attributes.
        self.data = copy.deepcopy(self.fits_data)
        self.rawdata = copy.deepcopy(self.fits_rawdata)
        self.datamask = copy.deepcopy(self.fits_datamask)
        self.config = copy.deepcopy(self._raw_configuration_class)

        # Meta data to test if this is a proper blank fits file.
        self._proper_blank = blank

        # This adds the functions that is responsible for a lot of the 
        # functionality to this class.
        self._echo_functionality()
        self._oscar_functionality()
        self._yankee_functionality()
        

    def _echo_functionality(self):
        """
        ECHO Attributes
        ---------------
        echo_mask : ndarray
            A boolean array that is the overall mask of this data array.
            Supercedes, but combines nicely with, the data array masked array.
        echo_mask_dictionary : dictionary
            The ECHO masking dictionary that is relevant to this data array.
        echo_synthesize_mask_dictionary : method
            This method takes the masking dictionary and collapses it down 
            into a single mask and saves it to the ``echo_mask`` attribute.
        echo_apply_mask : method
            This method takes the current mask stored in ``echo_mask`` and 
            applies to the data array, storing the resulting masked array in
            ``
            
        """
        # Needed attributes for the ECHO class.
        self.echo_mask = None
        self.echo_mask_dictionary = {}

        # Allow for the usage of the general form of the ECHO line.
        def _mask_function(**kwargs):
            # Allow for the configuration class to be used.
            if 'configuration_class' in kwargs:
                pass
            else:
                kwargs['configuration_class'] = copy.deepcopy(self.config)
            # Change the dictionary of the mask, but, leave the data array.
            # Return both normally however.
            temp_mask, temp_dict = echo_execution(data_array=self.data, **kwargs)
            self.echo_mask_dictionary = {**self.echo_mask_dictionary, **temp_dict}
            return temp_mask, temp_dict
        setattr(self, 'echo_execution', _mask_function)
        # Remove for its re-usage.
        del _mask_function

        # Gathering all possible filters, given as a dictionary. For valid 
        # filters, add them as a possible function.
        filter_list = dict(inspect.getmembers(echo.masks, inspect.isfunction))

        echo_filters = echo.echo_funct.sort_masking_dictionary(copy.deepcopy(filter_list))
        for keydex, functiondex in filter_list.items():
            if (not 'echo' in keydex):
                echo_filters.pop(keydex, None)
            else:
                # Making the filter function rely on the data and previous 
                # dictionary of this class.
                def _mask_function(**kwargs):
                    return functiondex(data_array=self.data, 
                                       previous_mask=self.echo_mask_dictionary,
                                       return_mask_only=False
                                       **kwargs)
                # Attach the masking function to the class.
                setattr(self, keydex, _mask_function)
                # Remove for its re-usage in the next iteration of the loop.
                del _mask_function
                
        # Allow for the synthesis of the masking dictionary, a wrapper 
        # function around the original function.
        def _update_function():
            masked_dict = echo.synthesize_mask_dictionary(self.echo_mask_dictionary)
            self.echo_mask = masked_dict
            return masked_dict
        setattr(self, 'echo_synthesize_mask_dictionary', _update_function)
        del _update_function

        # Allow for the application of the data mask using the masking 
        # dictionary that is stored in this class.
        def _update_function():
            masked_array = echo.numpy_masked_array(data_array=self.data,
                                                   synthesized_mask=self.echo_mask)
            self.data = masked_array
            self.datamask = (np_ma.getmask(masked_array) 
                                  if np_ma.getmask(masked_array) is not np_ma.nomask else None)
            return masked_array
        setattr(self, 'echo_apply_mask', _update_function)
        del _update_function



    def _oscar_functionality(self):
        pass

    def _yankee_functionality(self):
        """This allows for the usage of the YANKEE line with this class.
        """