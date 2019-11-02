import copy
import os
import pickle

# This may be unneeded because the imports should already be read by the 
# Yankee module.
from IfA_Smeargle import yankee
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

    def __str__(self):
        """ The print visualization of the configuration classes.

        This is for a good amount of printing and visualization. This just 
        the default method, though it should work for most cases. Each other 
        configuration class may have their own method if need be.        

        This statement uses a fair bit of basic Unicode characters mostly 
        for ease of printing and to reduce confusion.
        """

        config_dictionary = self.__dict__
        config_keys = config_dictionary.keys()

        # The beginning newline is for multi configuration class printing.
        print_output = '\n< Configuration Class --- ' + str(type(self).__name__) + ' > \n'

        # chr(9555) = ╓ . It is a pretty header character. The class is 
        # repeated again to reduce confusion especially with multi-class 
        # printing.
        print_output += chr(9555) + ' ' + str(type(self).__name__) + ' Parameters:' + '\n'


        for keydex in config_keys:
            # A nice character encoding in the event that the new object is 
            # to be an embedded configuration class.
            if ('Configuration Class' in str(config_dictionary[keydex])):
                # char(8628) = ↴ . Entered because configuration classes go
                # to the next line.
                correspondence_symbol = chr(8628)
            else:
                # char(8640) = ⇀ . A right top harpoon is used for its visual
                # aspect, and to not have it confused with an equals. Also, 
                # it discourages copying the key and value.
               correspondence_symbol = chr(8640)

            # chr(9567) = ╟ . It is a pretty vertical bar that matches.
            line_string = (chr(9567) + '  ' 
                           + str(keydex) 
                           + ' ' + correspondence_symbol + ' ' 
                           + str(config_dictionary[keydex]) 
                           + '\n')
            print_output += line_string

        # End of the loop, char(9561) = ╙ . It is a pretty end character.
        print_output += chr(9561) + '------------------------------------------' + '\n'

        # Final end of print.
        print_output += '</ Configuration Class --- ' + str(type(self).__name__) + ' >'

        return print_output

    def print(self):
        """ This is a silly wrapper function around basic printing; do not ask
        why.

        P.S. It is fun.

        Parameters
        ----------
        nothing
        """
        print(self)

    def write_to_file(self, file_name, overwrite=False, protocol=pickle.HIGHEST_PROTOCOL):
        """ Wrapper function around configuration file writing. 
        
        Writes the configuration class to a pickle file. See 
        ``yankee_write_config_file`` for more information.

        Parameters
        ----------
        config_class : Configuration class
            The configuration class that is going to be saved as a file.
        file_name : string
            The name of the configuration class. The extension ``.ifaspkl``  
            is automatically applied. This denotes a Python pickle file from 
            IfA-Smeargle.
        overwrite : boolean
            If true, the writing of the configuration class will overwrite any
            existing file.
        protocol : int
            The pickling protocol value for the pickling function.

        Returns
        -------
        nothing

        """

        yankee.yankee_write_config_file(self, file_name, overwrite=overwrite, protocol=protocol)


    def read_from_file(self, file_name):
        """ Wrapper function around configuration file reading.

        Reads and assigns a file IfA Smeargle configuration class to this
        current class. See ``yankee_read_config_file`` for more information on
        file reading.
        
        Parameters
        ----------
        file_name : string
            The path and name of the file that contains the configuration  
            class. Must have the extension ``.ifaspkl``. If ``file_name`` 
            is None, then nothing happens. 

        Returns
        -------
        nothing
        """

        if (file_name is not None):
            if (not isinstance(file_name, str)):
                smeargle_warning(InputWarning, ("The configuration file name is not a string "
                                                "type. Nothing will be done."))
                pass

            elif (isinstance(file_name, str)):
                read_config_class = yankee.yankee_read_config_file(file_name)
            else:
                raise BrokenLogicError("Somehow config_file_name is both and a string and "
                                       "not a string.")

            # Ensure that the read configuration file is of the same class.
            # That is, for example, a BravoConfig class is not mixed with an 
            # EchoConfig class.
            if (not isinstance(read_config_class,type(self))):
                raise ImportingError("The read configuration file configuration class type " 
                                     "is not the same as the calling class type.  \n  "
                                     "File:  {file_type}  \n  Init:  {init_type} ".format(
                                         file_type=type(read_config_class),
                                         init_type=type(self)))
            else:
                try:
                    self.__dict__.update(read_config_class.__dict__)
                except Exception:
                    raise ImportingError("The configuration file cannot be read this way. "
                                         "consider using the factory function for the "
                                         "<yankee_read_config_file> function.")
        else:
            # File name is not strictly provided, give an empty class.
            smeargle_warning(InputWarning,("The file name string is None, nothing will be done."))
        
        # Finished
        return self


