import copy
import pickle

# This may be unneeded because the imports should already be read by the 
# Yankee module.
try:
    from IfA_Smeargle.yankee.configuration_classes.__init__ import *
    from IfA_Smeargle.yankee.__init__ import *
except ImportError:
    # It likely has been imported fine.
    pass

from IfA_Smeargle.meta import *



class BaseConfig(object):
    """ The base configuration class for the Smeargle Yankee configuration 
    line.

    This is the parent class of the configuration classes. This is mostly for 
    attributes or functions which all classes should have. 
    
    """

    def __init__(self, config_file_name=None):
        """ Generate or read from file a configuration class.

        This allows for the ease of creating configuration classes from 
        configuration files. 

        Parameters
        ----------
        config_file_name : string or None
            The path to the file name that is desired to be read. If it is
            None, then the default, blank, configuration class is returned
            instead.

        Returns
        -------
        self : Configuration Class
            The configuration class.
        """

        # Test if the config file name has been provided.
        if (config_file_name is not None):
            # Assume it is a string and attempt to parse it.
            self = self.read_from_file(config_file_name)
        else:
            # Assume defaults.
            pass


    def write_to_file(self, file_name, protocol=pickle.HIGHEST_PROTOCOL):
        """ Wrapper function around configuration file writing. 
        
        Writes the configuration class to a pickle file. See 
        ``write_config_file`` for more information.

        Parameters
        ----------
        config_class : Configuration class
            The configuration class that is going to be saved as a file.
        file_name : string
            The name of the configuration class. The extension ``.ifaspkl``  
            is automatically applied. This denotes a Python pickle file from 
            IfA-Smeargle.
        protocol : int
            The pickling protocol value for the pickling function.

        Returns
        -------
        nothing

        """

        write_config_file(self, file_name, protocol=protocol)


    def read_from_file(self, file_name):
        """ Wrapper function around configuration file reading.

        Reads and assigns a file IfA Smeargle configuration class to this
        current class. See ``read_config_file`` for more information on
        file reading.
        
        Parameters
        ----------
        file_name : string
            The path and name of the file that contains the configuration  
            class. Must have the extension ``.ifaspkl``. If ``file_name`` 
            is None, then a default configuration class is returned. 

        Returns
        -------
        nothing
        """

        if (file_name is not None):
            if (not isinstance(file_name, str)):
                smeargle_warning(file_name,("The configuration file name is not a string "
                                               "type. A default and blank configuration class "
                                               "will be provided instead."))
                self = self.__init__()

            elif (isinstance(file_name, str)):
                read_config_class = read_config_file(file_name)
            else:
                raise BrokenLogicError("Somehow config_file_name is both a neither a string or "
                                       "not a string.")

            # Ensure that the read configuration file is of the same class.
            # That is, for example, a BravoConfig class is not mixed with an 
            # EchoConfig class.
            if (not isinstance(read_config_class,type(self))):
                raise ImportingError("The read configuration file configuration class type " 
                                     "is not the same as the calling class type. See:   "
                                     "File:  {file_type}    Init:  {init_type} ".format(
                                         file_type=type(read_config_class),
                                         init_type=type(self)))
            else:
                # Seems to be all good.
                try:
                    self = copy.deepcopy(read_config_class)
                except Exception:
                    self = read_config_class
        else:
            # File name is not strictly provided, give an empty class.
            smeargle_warning(InputWarning,("The file name string is None, returning a blank "
                                           "class instead."))
            self = self.__init__()
        
        # Finished
        return self



# Loading/unloading functions.
def write_config_file(config_class, file_name, 
                      protocol=pickle.HIGHEST_PROTOCOL):
    """ Function to write a specific configuration class to a normal file.

    As the entire module more or less depends on configuration classes. It 
    is important to be able to save, copy, and reuse configuration classes. 
    Therefore, this allows configuration files to be written to file. 

    Parameters
    ----------
    config_class : Configuration class
        The configuration class that is going to be saved as a file.
    file_name : string
        The name of the configuration class. The extension ``.ifaspkl``  
        is automatically applied. This denotes a Python pickle file from 
        IfA-Smeargle.
    protocol : int
        The pickling protocol value for the pickling function.

    Returns
    -------
    nothing

    """

    # Make sure the proper class is being sent through.
    if (not isinstance(config_class, BaseConfig)):
        raise InputError("Provided class is not a Smeargle BaseConfig configuration class. It "
                         "would be improper to write it as one.")

    # Automatically apply extension for good file hygiene.
    if (file_name[-8:] == '.ifaspkl'):
        pass
    else:
        # It is missing the extension, add, but warn.
        smeargle_warning(InputWarning,("The provided file name is missing the .ifaspkl file "
                                       "extension. It has been automatically appended."))
        file_name += '.ifaspkl'

    # ...and write.
    with open(file_name, 'wb') as config_file:
        pickle.dump(config_class, config_file, protocol)


def read_config_file(file_name):
    """ Function to read a specific configuration class from a normal file.

    As the entire module more or less depends on configuration classes. It is 
    important to be able to save, copy, and reuse configuration classes.  
    Therefore, this allows pre-made/saved configuration files to be read from 
    a file.

    Parameters
    ----------
    file_name : string
        The path and name of the file that contains the configuration class. 
        Must have the extension ``.ifaspkl``

    Returns
    -------
    config_class : SmeargleConfig
        The configuration class stored in the file.

    """
    
    # Amateur checking to see the file is associated with IfA-Smeargle.
    if (file_name[-8:] != '.ifaspkl'):
        raise InputError("Provided file name does not have the .ifaspkl extension. This may be "
                         "the wrong file.")

    # And load...
    with open(file_name,'rb') as config_file:
        
        # Test if the class is defined.
        try:
            config_class = pickle.load(config_file)
        except AttributeError:
            raise ImportError("The configuration class objects have not been imported properly. "
                              "The depickleing has no template to use. Consider importing the "
                              "configuration classes to __main__.")

        config_class = copy.deepcopy(config_class)

    return config_class