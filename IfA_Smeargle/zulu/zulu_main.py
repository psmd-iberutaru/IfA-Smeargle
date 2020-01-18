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
        
        # The documentation should reflect the subfunctions.
        self.__doc__ = "\n".join([self.__doc__, 
                                 self._echo_functionality.__doc__,
                                 self._oscar_functionality.__doc__,
                                 self._yankee_functionality.__doc__])

        # Extract the data from the fits file, unless they wanted it blank.
        if (blank):
            self.filename = None
            self.fits_file = None
            self.fits_header = None
            self.fits_data = None
            self.fits_rawdata = None
            self.fits_datamask = None
            smeargle_warning(InputWarning,("The data array file is indicated to return a blank "
                                           "one. Doing so as requested."))
        else:
            # The file name, for completeness purposes.
            self.filename = filename
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
            self._raw_configuration_class = None
            smeargle_warning(InputWarning,("There is no configuration class provided for this "
                                           "array. The attribute will be None. The "
                                           "SmargleConfig class will be the default."))

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
        self._bravo_functionality()
        self._echo_functionality()
        self._oscar_functionality()
        self._yankee_functionality()


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
                bravo.bravo_filename_split_by_parameter(path_file_name=self.filename, 
                                                        ignore_mismatch=False))

        # End point median calculation creation.
        raise IncompleteError
        

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
        # Needed attributes for the ECHO class.
        self.echo_mask = None
        self.echo_mask_dictionary = {}

        # Allow for the usage of the general form of the ECHO line.
        def _execute_mask_function(self, **kwargs):
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
            def _temp_mask_function(filter_funct=filterdex, filter_key=keydex, 
                                    configuration=None, **kwargs):
                # This runs on the assumption that the configuration keys
                # have been properly named.
                config_key = ((filter_key[0:7] + '_config') 
                              if ('echo' in filter_key[0:7]) else None)
                
                config_params = self._zulu_determine_configuration_parameters(
                    configuration_flag_input=configuration, custom_inputs=kwargs,
                    subconfig_class=yankee.EchoConfig, subconfig_key=config_key)

                # Check for the run parameter, if it is false, this filter
                # should not be run.
                if (config_params.pop('run')):
                    # The masking dictionary is what shall be mutated, ensure 
                    # that there won't be a conflict with this.
                    filter_dict =  filter_funct(data_array=self.data,
                                                previous_mask=self.echo_mask_dictionary,
                                                return_mask=False,
                                                **config_params)
                else:
                    # No filter should be run, and therefore no output.
                    smeargle_warning(MaskingWarning,("The <run> parameter for the masking "
                                                     "function < {filter_name} > is False. The "
                                                     "mask shall not be applied nor added to "
                                                     "masking dictionary."
                                                     .format(filter_name=filter_key)))
                    filter_dict = {}
                # Add the filter to the masking dictionary.
                self.echo_mask_dictionary.update(filter_dict)
                # All done.
                return None

            # Attach the function.
            setattr(self, keydex, meta_prog.smeargle_deepcopy_function(_temp_mask_function))
            # Allow for the reusing of the temp function
            del _temp_mask_function

                
        # Allow for the synthesis of the masking dictionary, a wrapper 
        # function around the original function.
        def _synthesize_function():
            masked_array = echo.echo_synthesize_mask_dictionary(self.echo_mask_dictionary)
            self.echo_mask = masked_array
            return masked_array
        setattr(self, 'echo_synthesize_mask_dictionary', _synthesize_function)
        del _synthesize_function

        # Allow for the application of the data mask using the masking 
        # dictionary that is stored in this class.
        def _update_function():
            masked_array = echo.echo_numpy_masked_array(data_array=self.data,
                                                        synthesized_mask=self.echo_mask,
                                                        masking_dictionary=None)
            self.data = masked_array
            self.datamask = (np_ma.getmask(masked_array) 
                                  if np_ma.getmask(masked_array) is not np_ma.nomask else None)
            return masked_array
        setattr(self, 'echo_numpy_masked_array', _update_function)
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
            def plot_function(plot_funt=functdex, **kwargs):
                config_params = self._zulu_determine_configuration_parameters(
                    configuration_flag_input=configuration, custom_inputs=kwargs,
                    subconfig_class=yankee.OscaConfig, subconfig_key=config_key)

            setattr(self, keydex, meta_prog.smeargle_deepcopy_function(
                lambda plot_funct=functdex, **kwargs: plot_funct(data_array=self.data, 
                                                                 **kwargs)))

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
            setattr(self, "SmeargleConfig", 
                    yankee.yankee_configuration_factory_function(yankee.SmeargleConfig, None, True))
        else:
            # Fast forward just in case the provided configuration class is 
            # outdated.
            fast_forwarded_class = None
            try:
                fast_forwarded_class = yankee.yankee_fast_forward_configuration_class(
                    self._raw_configuration_class)
            except Exception:
                # The raw configuration class may not even be a configuration
                # class.
                if (isinstance(self._raw_configuration_class,(yankee.SmeargleConfig,
                                                              yankee.BaseConfig))):
                    # Hm... Sparrow is still at a loss for why it would enter 
                    # here.
                    raise BugError("The yankee_fast_forward_configuration_class function seemed to "
                                   "fail with a valid configuration class input.")
                elif (isinstance(self._raw_configuration_class, str)):
                    # It may be that the user provided a file name.
                    configuration_file_name = str(copy.deepcopy(self._raw_configuration_class))
                    fast_forwarded_class = yankee.yankee_configuration_factory_function(
                        yankee.SmeargleConfig, configuration_file_name, False)
                else:
                    # It is not a configuration class, it is best that a 
                    # default one is assigned.
                    smeargle_warning(ConfigurationWarning,("The initial configuration class "
                                                            "provided is not an actual "
                                                            "configuration class and is "
                                                            "unworkable. A default is being "
                                                            "provided."))
                    fast_forwarded_class = yankee.yankee_configuration_factory_function(
                        yankee.SmeargleConfig, None, True)
            finally:
                # For naming convention.
                configuration_class = fast_forwarded_class
                setattr(self, "SmeargleConfig", configuration_class)
                setattr(self, "config", configuration_class)

        # Also allow for the printing, reading, writing, and updating of 
        # the new configuration class. These are mostly aliases.
        def print_configuration(self):
            """ Prints the configuration class parameters. """
            self.SmeargleConfig.print()
        setattr(self, "print_configuration", print_configuration)
        def read_configuration(self, file_name):
            """ Reads the configuration class from a configuration file. """
            self.SmeargleConfig.read_from_file(file_name)
        setattr(self, "read_configuration", read_configuration)
        def write_configuration(self, file_name):
            """ Writes the configuration class to a configuration file. """
            self.SmeargleConfig.write_to_file(file_name)
        setattr(self, "write_configuration", write_configuration)
        def overwrite_configuration(self, overwriting_configuration):
            """ Overwrite the configuration class by the provided class. """
            self.SmeargleConfig = yankee.yankee_overwrite_configuration_class(self.SmeargleConfig,
                                                                       overwriting_configuration)
        setattr(self, "overwrite_configuration", overwrite_configuration)
        def fast_forward_configuration():
            """ Fast forward the configuration class. It is unlikely that 
                this will be needed, but, it is here. """
            self.SmeargleConfig = yankee.yankee_fast_forward_configuration_class(self.SmeargleConfig)
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
