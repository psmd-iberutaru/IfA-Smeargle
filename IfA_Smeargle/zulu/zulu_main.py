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
import importlib
import inspect
import numpy as np
import numpy.ma as np_ma
import os
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
    :doc:`ZULU pipelines <IfA_Smeargle.zulu.detector_pipelines>`)
    
    New pipelines, however, should always be developed using this object
    oriented approach. 
    """

    def __init__(self, pathname, configuration_class=None,
                 blank=False, silent=False):
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
        silent : boolean (optional)
            Executes the creation of this class without any warnings or 
            information.
        """

        # This separate function is so that the silencing functionality can
        # work properly. 
        def _initalization(pathname=None, configuration_class=None,
                           blank=None):
            # Extract the data from the fits file, unless they wanted it blank.
            if (blank):
                self.filename = None
                self.filedirectory = None
                self.fileextension = None
                self.filepathname = None
                self.fits_file = None
                self.fits_header = None
                self.fits_data = None
                self.fits_rawdata = None
                self.fits_datamask = None
                smeargle_warning(InputWarning,("The data array file is indicated to return a "
                                               "blank one. Doing so as requested."))
            else:
                # Clean up the file path nane such that there are no directory
                # slash problems.
                pathname = os.path.join(pathname)
                # The file name, for completeness purposes.
                self.filename = os.path.splitext(os.path.basename(pathname))[0]
                self.filedirectory = os.path.dirname(pathname)
                self.fileextension = os.path.splitext(os.path.basename(pathname))[-1]
                self.filepathname = pathname
                # Read the fits file data.
                hdul_file, hdu_header, hdu_data = meta_io.smeargle_open_fits_file(pathname)
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
                self._raw_configuration_class = None
                smeargle_warning(InputWarning,("There is no configuration class provided for "
                                               "this array. The raw attribute will be None; the "
                                               "mutable attribute will be a default "
                                               "configuration class."))

            # Though these may seem like copies, these are the intended mutable 
            # versions of the previous attributes.
            self._mutable_header = copy.deepcopy(self.fits_header)
            self._mutable_data = copy.deepcopy(self.fits_data)
            self._mutable_datamask = copy.deepcopy(self.fits_datamask)
            self._mutable_config = copy.deepcopy(self._raw_configuration_class)
            # Needed attributes for the ECHO class. The property class is defined
            # externally along with the others.
            self._mutable_echo_mask = None
            self._mutable_echo_mask_dictionary = {}

            # Meta data to test if this is a proper blank fits file.
            self._proper_blank = blank

            # This adds the functions that is responsible for a lot of the 
            # functionality to this class.
            self._bravo_functionality()
            self._echo_functionality()
            self._oscar_functionality()
            self._yankee_functionality()

            return None
        
        # If the user desired it to be silent.
        if (silent):
            with smeargle_absolute_silence():
                _initalization(pathname=pathname, configuration_class=configuration_class,
                               blank=blank)
        else:
            _initalization(pathname=pathname, configuration_class=configuration_class,
                               blank=blank)

        return None


    # Property variables and for the mutable attributes for the data and
    # the global data mask.
    def _get_header(self): return self._mutable_header
    def _set_header(self, h): self._mutable_header = h
    def _del_header(self): del self._mutable_header
    header = property(_get_header, _set_header, _del_header)
    def _get_data(self): return self._mutable_data
    def _set_data(self, d): self._mutable_data = d
    def _del_data(self): del self._mutable_data
    data = property(_get_data, _set_data, _del_data)
    def _get_datamask(self): return self._mutable_datamask
    def _set_datamask(self, m): self._mutable_datamask = m
    def _del_datamask(self): del self._mutable_datamask
    datamask = property(_get_datamask, _set_datamask, _del_datamask)
    def _get_config(self): return self._mutable_config
    def _set_config(self, c): self._mutable_config = c
    def _del_config(self): del self._mutable_config
    config = property(_get_config, _set_config, _del_config)
    # Property values for the ECHO based functionality.
    def _get_echo_mask(self): return self._mutable_echo_mask
    def _set_echo_mask(self, em): self._mutable_echo_mask = em
    def _del_echo_mask(self): del self._mutable_echo_mask
    echo_mask = property(_get_echo_mask, _set_echo_mask, _del_echo_mask)
    def _get_echo_mask_dictionary(self): return self._mutable_echo_mask_dictionary
    def _set_echo_mask_dictionary(self, ed): self._mutable_echo_mask_dictionary = ed
    def _del_echo_mask_dictionary(self): del self._mutable_echo_mask_dictionary
    echo_mask_dictionary = property(_get_echo_mask_dictionary, 
                                    _set_echo_mask_dictionary, 
                                    _del_echo_mask_dictionary)


    def _bravo_functionality(self):
        """ This allows for the usage of some BRAVO line functions within
        this class.

        BRAVO Attributes
        ----------------
        bravo_filename_split_by_parameter : dictionary
            Takes a standard file name made by the BRAVO class and splits 
            it into a more workable dictionary.
        median_endpoints : method
            Reads the fits file values and computes the new result using 
            end points calculations.
        median_endpoints_per_second : method
            Reads the fits file values and computes the new result using 
            end points calculations.
        median_endpoints_per_kilosecond : method
            Reads the fits file values and computes the new result using 
            end points calculations.
        """

        # File name parameter splitting.
        setattr(self, 'bravo_filename_split_by_parameter', 
                lambda: bravo.bravo_filename_split_by_parameter(path_file_name=self.filename,
                                                                ignore_mismatch=False))
        
        # The median functions, to act on this data file.
        def median_endpoints(start_chunk, end_chunk):
            resulting_data = bravo.avging.median_endpoints(data_array=self.data, 
                                                           start_chunk=start_chunk, 
                                                           end_chunk=end_chunk)
            self.data = resulting_data
            return resulting_data
        setattr(self, 'median_endpoints', median_endpoints)
        # The two other median endpoints functions.
        def median_endpoints_per_second(start_chunk, end_chunk, frame_exposure_time):
            resulting_data = bravo.avging.median_endpoints_per_second(
                data_array=self.data, start_chunk=start_chunk, 
                end_chunk=end_chunk, frame_exposure_time=frame_exposure_time)
            self.data = resulting_data
            return resulting_data
        setattr(self, 'median_endpoints_per_second', median_endpoints_per_second)
        def median_endpoints_per_kilosecond(start_chunk, end_chunk, frame_exposure_time):
            resulting_data = bravo.avging.median_endpoints_per_kilosecond(
                data_array=self.data, start_chunk=start_chunk, 
                end_chunk=end_chunk, frame_exposure_time=frame_exposure_time)
            self.data = resulting_data
            return resulting_data
        setattr(self, 'median_endpoints_per_kilosecond', median_endpoints_per_kilosecond)

        return None

    def _echo_functionality(self):
        """ This allows for the usage of the ECHO line with this class.

        ECHO Attributes
        ---------------
        echo###_filter_name : method
            These are methods attached to this class that allows for the 
            execution of a filter in an object orientated approach. See the
            :doc:`ECHO masks <python_docstrings/IfA_Smeargle.echo.masks>`) 
            documentation for more information.
        echo_mask : ndarray
            A boolean array that is the overall mask of this data array.
            Does not supersedes, but combines nicely with, the data array 
            masked array.
        echo_mask_dictionary : dictionary
            The ECHO masking dictionary that is relevant to this data array.
        echo_echo_synthesize_mask_dictionary : method
            This method takes the masking dictionary and collapses it down 
            into a single mask and saves it to the ``echo_mask`` attribute.
        echo_apply_mask : method
            This method takes the current mask stored in ``echo_mask`` and 
            applies to the data array, storing the resulting masked array in
            the ``data`` attribute and the mask itself in ``datamask``.

        """

        # Allow for the usage of the general form of the ECHO line.
        def _execute_mask_function(frame=None, **kwargs):
            # Allow for the configuration class to be used.
            if ('configuration_class' in kwargs):
                pass
            else:
                kwargs['configuration_class'] = copy.deepcopy(self.config)
            # Change the dictionary of the mask, but, leave the data array.
            # Return both normally however. Also, if the process is to only
            # be done on a specific frame.
            if ((_data_array.ndim >= 3) and (isinstance(frame, int))):
                temp_mask, temp_dict = echo_execution(data_array=self.data[frame], **kwargs)
            else:
                temp_mask, temp_dict = echo_execution(data_array=self.data, **kwargs)
            self.echo_mask_dictionary = {**self.echo_mask_dictionary, **temp_dict}
            return temp_mask, temp_dict
        setattr(self, 'echo_execution', _execute_mask_function)
        # Remove for its re-usage.
        del _execute_mask_function


        # Gathering all possible filters, given as a dictionary. For valid 
        # filters, add them as a possible function.
        echo_filters_dict = meta_prog.smeargle_avaliable_echo_filter_functions()

        # Attach the functions to the main data class, using the data from 
        # this class where appropriate. Keep in mind of the late
        # binding problem that causes all of the functions to just be copies
        # of the last function. See https://stackoverflow.com/q/3431676.
        for keydex, filterdex in echo_filters_dict.items():
            def _temp_mask_function(filter_funct=filterdex, filter_key=keydex, frame=None, 
                                    **kwargs):
                # The data may be desired to only be a subset.
                data_array = self.data[frame] if isinstance(frame, int) else self.data

                # Run the filter.
                filter_dict =  filter_funct(data_array=data_array,
                                            previous_mask=self.echo_mask_dictionary,
                                            return_mask=False,
                                            **kwargs)
                # Add the filter to the masking dictionary.
                self.echo_mask_dictionary.update(filter_dict)

                # Also, for the sake of extra data if needed.
                filter_array =  filter_funct(data_array=data_array,
                                            previous_mask={},
                                            return_mask=True,
                                            **kwargs)

                # All done.
                return filter_array

            # Attach the function.
            setattr(self, keydex, 
                    meta_prog.smeargle_deepcopy_function(original_funct=_temp_mask_function))
            # Allow for the reusing of the temp function
            del _temp_mask_function

                
        # Allow for the synthesis of the masking dictionary, a wrapper 
        # function around the original function.
        def _synthesize_function():
            masked_array = echo.echo_synthesize_mask_dictionary(
                masking_dictionary=self.echo_mask_dictionary)
            self.echo_mask = masked_array
            return masked_array
        setattr(self, 'echo_synthesize_mask_dictionary', _synthesize_function)
        del _synthesize_function

        # Allow for the application of the data mask using the masking 
        # dictionary that is stored in this class.
        def _update_function():
            masked_array = echo.echo_create_masked_array(data_array=self.data,
                                                         synthesized_mask=self.echo_mask,
                                                         masking_dictionary=None)
            self.data = masked_array
            self.datamask = (np_ma.getmask(masked_array) 
                                  if np_ma.getmask(masked_array) is not np_ma.nomask else None)
            return masked_array
        setattr(self, 'echo_create_masked_array', _update_function)
        del _update_function

        # All done.
        return None

    def _oscar_functionality(self):
        """ This allows for the usage of the OSCAR line with this class.

        OSCAR Attributes
        ----------------
        plot_ploting_function_name : method
            This is just a simple plotting function that is wrapped and 
            built in from the OSCAR line. 
        """
        
        # Obtain all of the available plotting functions that can be used.
        oscar_plot_dict = meta_prog.smeargle_avaliable_oscar_plotting_functions()

        # Attach the plotting functions to the class. Keep in mind of the late
        # binding problem that causes all of the functions to just be copies
        # of the last function. See https://stackoverflow.com/q/3431676.
        for keydex, functdex in copy.deepcopy(oscar_plot_dict).items():
            # Allow for runtime modification of parameters.
            def plotting_function(_function=functdex, **kwargs):
                return _function(data_array=self.data, **kwargs)
            setattr(self, keydex, plotting_function)
            del plotting_function

        # All done.
        return None

    def _yankee_functionality(self):
        """This allows for the usage of the YANKEE line with this class.

        YANKEE Attributes
        -----------------
        SmeargleConfig : Configuration Class
            This is the built in configuration class that goes along with 
            this data class. 
        print_configuration : method
            This allows for the print visualization of the SmeargleConfig
            configuration class.
        read_configuration : method
            Provided a configuration file name, this method reads it from 
            the provided file. 
        write_configuration : method
            Provided a configuration file name, this method writes the 
            current configuration file to the file name provided. 
        overwrite_configuration : method
            Provided a configuration class, all elements in the current
            configuration class, where similar, are overwritten using the 
            provided class. 
        fast_forward_configuration : method
            Fast forwards the current configuration class to the current 
            version. 
        """

        # First, test if the configuration class is an actual configuration
        # class.
        if (self._raw_configuration_class is None):
            # There is no need for error, a default one will be assigned.
            self.config = yankee.yankee_configuration_factory_function(
                desired_class=yankee.SmeargleConfig, file_name=None, silent=True)
            # But, warn...
            smeargle_warning(InputWarning,("There is no input configuration class. A blank one "
                                           "will be assigned."))
        else:
            # Fast forward just in case the provided configuration class is 
            # outdated.
            fast_forwarded_class = None
            try:
                fast_forwarded_class = yankee.yankee_fast_forward_configuration_class(
                    configuration_class=self._raw_configuration_class)
            except Exception:
                # The raw configuration class may not even be a configuration
                # class.
                if (isinstance(self._raw_configuration_class,(yankee.SmeargleConfig,
                                                              yankee.BaseConfig))):
                    # Hm... Sparrow is still at a loss for why it would enter 
                    # here.
                    raise AssumptionError("The yankee_fast_forward_configuration_class function "
                                          "seemed to fail with a valid configuration class "
                                          "input.")
                elif (isinstance(self._raw_configuration_class, str)):
                    # It may be that the user provided a file name.
                    configuration_file_name = str(copy.deepcopy(self._raw_configuration_class))
                    fast_forwarded_class = yankee.yankee_configuration_factory_function(
                        desired_class=yankee.SmeargleConfig, 
                        file_name=configuration_file_name, silent=False)
                else:
                    # It is not a configuration class, it is best that a 
                    # default one is assigned.
                    smeargle_warning(ConfigurationWarning,("The initial configuration class "
                                                            "provided is not an actual "
                                                            "configuration class and is "
                                                            "unworkable. A default is being "
                                                            "provided."))
                    fast_forwarded_class = yankee.yankee_configuration_factory_function(
                        desired_class=yankee.SmeargleConfig, file_name=None, silent=True)
            finally:
                # For naming convention.
                configuration_class = fast_forwarded_class
                self.config = configuration_class

        # Also allow for the printing, reading, writing, and updating of 
        # the new configuration class. These are mostly aliases.
        def print_configuration(self):
            """ Prints the configuration class parameters. """
            self.SmeargleConfig.print()
        setattr(self, "print_configuration", print_configuration)
        def read_configuration(self, file_name):
            """ Reads the configuration class from a configuration file. """
            self.SmeargleConfig.read_from_file(file_name=file_name)
        setattr(self, "read_configuration", read_configuration)
        def write_configuration(self, file_name):
            """ Writes the configuration class to a configuration file. """
            self.SmeargleConfig.write_to_file(file_name=file_name)
        setattr(self, "write_configuration", write_configuration)
        def overwrite_configuration(self, overwriting_configuration):
            """ Overwrite the configuration class by the provided class. """
            self.SmeargleConfig = yankee.yankee_overwrite_configuration_class(
                inferior_class=self.SmeargleConfig, superior_class=overwriting_configuration)
        setattr(self, "overwrite_configuration", overwrite_configuration)
        def fast_forward_configuration():
            """ Fast forward the configuration class. It is unlikely that 
                this will be needed, but, it is here. """
            self.SmeargleConfig = yankee.yankee_fast_forward_configuration_class(
                configuration_class=self.SmeargleConfig)
        setattr(self, "fast_forward_configuration", fast_forward_configuration)

        # All done.
        return None

    def _zulu_determine_configuration_parameters(self,
                                                 configuration_flag_input=None, 
                                                 custom_inputs=None,
                                                 subconfig_class=None, 
                                                 subconfig_key=None):
        """ This function basically determines and extracts the configuration
        option for all of the surrounding structures.

        The configuration class is built in to the class. It is generally the
        case that the user would want to use it. However, the user may also
        have their own entries that conflict (and should override) the 
        built in configuration class. 

        This function takes these issues into account and returns the proper
        configuration dictionary for the respective function.        

        Parameters
        ----------
        configuration_flag_input : Configuration Class, string, boolean
            This is what the user input for their configuration flag. Note
            that this flag can be one of many types (not just a string). The
            flags are adapted as follows:
                :Configuration Class: 
                    This becomes the configuration class that will be used 
                    for the function.
                :string:
                    It is assumed that the configuration class is in a file.
                    The string must be a path that will load the desired
                    configuration file.
                :boolean:
                    If the boolean is true, then the current configuration 
                    class defined in this structure will be used as the 
                    default one.
        custom_inputs : dictionary
            A dictionary of the user's custom inputs. Custom inputs always
            override the provided or default configuration file.
        subconfig_class : Configuration class type
            The sub-configuration class (e.g. BravoConfig, EchoConfig, etc.) 
            type that is desired.
        subconfig_key : string
            The key of the configuration class that corresponds to the correct
            parameters.

        Returns
        -------
        parameter_dictionary : dictionary
            The desired parameters after the standard processing.
        """

        # Type check to ensure that there are no bad inputs. This is done as
        # the issubclass command may raise an error which is uninformative.
        try:
            if (not issubclass(subconfig_class, yankee.BaseConfig)):
                raise InputError("The subconfig class must be a subset of the YANKEE "
                                 "configuration classes.")
        except Exception:
            raise InputError("The subconfig class must be a subset of the YANKEE class "
                             "family. Moreover, it should be the class itself, not an "
                             "instance thereof.")
        # Type checking the key.
        if (not isinstance(subconfig_key,str)):
            raise InputError("The sub-configuration class key must be a string as it is a "
                             "dictionary key.")
        # Then the user's inputs.
        try:
            if (custom_inputs is None):
                # Nothing is just no configurations.
                custom_inputs = {}
            else:
                custom_inputs = dict(custom_inputs)
        except Exception:
            raise InputError("The custom inputs provided by the user must be a dictionary of "
                             "key-value parameters that will be passed to the function. Or, it "
                             "must be a None type if there are no custom inputs.")


        # Determine which configuration class to use in the first place
        # based on what is provided.
        try:
            if (isinstance(configuration_flag_input, yankee.BaseConfig)):
                using_config = yankee.yankee_extract_proper_configuration_class(
                    configuration_flag_input, subconfig_class, deep_copy=True)
            elif (isinstance(configuration_flag_input, str)):
                # Unsurprisingly, the extraction can also work with the
                # file path. Marked as a separate check for visual purposes.
                using_config = yankee.yankee_extract_proper_configuration_class(
                    configuration_flag_input, subconfig_class, deep_copy=True)
            elif (isinstance(configuration_flag_input, bool)):
                if (configuration_flag_input):
                    # Assume the user wants to use the built in configuration.
                    using_config = yankee.yankee_extract_proper_configuration_class(
                        self.config, subconfig_class, deep_copy=True)
                else:
                    # The built in configuration class should not be used. 
                    # A blank configuration file is provided.
                    using_config = yankee.yankee_configuration_factory_function(subconfig_class, 
                                                                         silent=True)
            else:
                # They did not specify a valid configuration flag. Just 
                # returning a blank one.
                using_config = yankee.yankee_configuration_factory_function(subconfig_class,
                                                                            silent=True)
        except Exception:
            raise
        finally:
            default_configuration = yankee.yankee_configuration_factory_function(subconfig_class, 
                                                                               silent=True)
            configuration = yankee.yankee_overwrite_configuration_class(default_configuration,
                                                                        using_config)

        # Extract the configuration dictionary (the parameters) from the two 
        # configurations, include the user's defined configurations.
        default_params = getattr(default_configuration, subconfig_key, {})
        config_params = getattr(configuration, subconfig_key, {})
        custom_params = copy.deepcopy(dict(custom_inputs))

        # A blank configurations may mean that the subconfig_key is not a 
        # valid or expected key.
        if (not (default_params or config_params)):
            smeargle_warning(ConfigurationWarning,("Both the default package and the data class "
                                                   "configurations are blank. This may be "
                                                   "indicative of the configuration key being "
                                                   "incorrect. "))
        
        # Precedence is to the custom inputs, then the system configuration
        # then the defaults; mimicking the order of overriding.
        parameter_dictionary = {**default_params, **{**config_params, **custom_params}} 

        # There are no actual configurations, user might want to know about
        # this.
        if (not parameter_dictionary):
            smeargle_warning(ConfigurationWarning,("There are no parameters being returned "
                                                   "provided the key <{key}> and the user's "
                                                   "custom inputs."
                                                   .format(key=str(subconfig_key))))
        elif (parameter_dictionary):
            # All done.
            return parameter_dictionary
        else:
            raise BrokenLogicError("The code should not reach here; the parameter_dictionary "
                                   "check must have failed, likely due to a change on how "
                                   "dictionaries are handled.")
        return None

    def deepcopy(self):
        """ Create a separate deep copy of an IfasDataArray using the data 
            within this one.
            
            There are a few issues with binding and copying this class. 
            Because of the recursive and layered nature of this class, there
            are issues with a simple deep copy function from the copy module.

            Parameters
            ----------
            none

            Returns
            -------
            new_instance : IfasDataArray
                The new copied instance of this class.
        """

        # The best way to resolve unwanted references is just to make a new
        # class.
        new_instance = IfasDataArray(pathname=None, configuration_class=None,
                                     blank=True, silent=True)

        # Extract the needed data to copy over and do so.
        original_instance = copy.deepcopy(self)
        original_dictionary = copy.deepcopy(vars(original_instance))
        for keydex, valuedex in copy.deepcopy(original_dictionary).items():
            if (callable(valuedex)):
                # There is no need for functions to be copied over, it is 
                # already provided for separately by the new class.
                __ = original_dictionary.pop(keydex)
            else:
                transfer = copy.deepcopy(original_dictionary.pop(keydex))
                new_instance.__dict__.update({keydex:transfer})

        return new_instance


    def write_fits_file(self, overwrite=True, silent=False):
        """ This writes the fits file to, well, file.

        Parameters
        ----------
        pathname : string (optional)
            The path where the file will be stored.
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
        # Write the file.
        hdul_file = meta_io.smeargle_write_fits_file(file_name=self.filepathname,
                                                     hdu_header=self.header, hdu_data=self.data,
                                                     hdu_object=None, save_file=True,
                                                     overwrite=overwrite, silent=silent)
        # Return the hdul.
        return hdul_file

    def update_pathname(self, directory=None, filename=None, extension=None,
                        prepend_directory=None, prepend_filename=None,
                        append_directory=None, append_filename=None):
        """ This allows for the updating of the file directory and filename.
        
        Parameters
        ----------
        directory : string (optional)
            A replacement string that will replace the directory section
            of the pathname.
        filename : string (optional)
            A replacement string that will replace the filename section
            of the pathname.
        extension : string (optional)
            A replacement string that will replace the extension section
            of the pathname.
        prepend_directory : string (optional)
            A string that will be prepended onto the directory string.
        prepend_filename : string (optional)
            A string that will be prepended onto the filename string.
        append_directory : string (optional)
            A string that will be appended onto the directory string.
        append_filename : string (optional)
            A string that will be appended onto the filename string.

        Returns
        -------
        new_pathname : string
            The new pathname of this file.
        """
        
        # Apply a basic type checking and replace None with blank strings for
        # the main purpose of concatenation.
        directory = str(directory) if isinstance(directory, str) else ''
        filename = str(filename) if isinstance(filename, str) else ''
        extension = str(extension) if isinstance(extension, str) else ''
        prepend_directory = str(prepend_directory) if isinstance(prepend_directory, str) else ''
        prepend_filename = str(prepend_filename) if isinstance(prepend_filename, str) else ''
        append_directory = str(append_directory) if isinstance(append_directory, str) else ''
        append_filename = str(append_filename) if isinstance(append_filename, str) else ''

        # Create the new directory as per the user created.
        if (len(directory) != 0):
            new_directory = os.path.join(prepend_directory, directory, append_directory)
        else:
            new_directory = os.path.join(prepend_directory, 
                                         self.filedirectory, 
                                         append_directory)
        # Create the new filename as per the user created.
        if (len(filename) != 0):
            new_filename = ''.join([prepend_filename, filename, append_filename])
        else:
            new_filename = ''.join([prepend_filename, self.filename, append_filename])
        # Update the extension as per the user inputted.
        new_extension = extension if (len(extension) != 0) else self.fileextension
        # Update the pathname.
        new_pathname = os.path.join(new_directory, ''.join([new_filename, new_extension]))

        # Update all of the variables.
        self.filepathname = copy.deepcopy(new_pathname)
        self.filename = os.path.splitext(os.path.basename(self.filepathname))[0]
        self.filedirectory = os.path.dirname(self.filepathname)
        self.fileextension = os.path.splitext(os.path.basename(self.filepathname))[-1]

        return new_pathname