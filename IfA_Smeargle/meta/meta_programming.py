"""
This is a list of functions that as rather useful in meta-programming.

"""

import copy
import functools
import importlib
import inspect
import types

from IfA_Smeargle.meta import *
from IfA_Smeargle import echo
from IfA_Smeargle import oscar

def smeargle_deepcopy_function(original_funct):
    """ A function to deep copy another function.

    The built in Python deep copy function utility does not really deep copy
    a function as one would expect, instead just returning the function as is.
    This function returns a proper deep copy of the function.

    Parameters
    ----------
    original_funct : function
        The original function.

    Returns
    -------
    deepcopy_funct : function
        The function deep copied.

    .. note::

        Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
    deepcopy_funct = types.FunctionType(original_funct.__code__, original_funct.__globals__,
                                        name=original_funct.__name__,
                                        argdefs=original_funct.__defaults__,
                                        closure=original_funct.__closure__)
    deepcopy_funct = functools.update_wrapper(deepcopy_funct, original_funct)
    deepcopy_funct.__kwdefaults__ = deepcopy_funct.__kwdefaults__

    # Just to test if it worked.
    if (original_funct is not deepcopy_funct):
        raise BugError("There should be no reason for the original and the "
                       "deep copy function to be the same.")

    # All done.
    return deepcopy_funct


def smeargle_avaliable_echo_filter_functions():
    """ This returns a dictionary of the available filtering functions found 
    in ECHO which can be used.

    Parameters
    ----------
    nothing

    Returns
    -------
    echo_filter_dict : dictionary
        This is a collection of all of the available filtering functions that 
        are usable.
    """

    # Gathering all possible filters, given as a dictionary. For valid 
    # filters, add them as a possible function.
    filter_list = dict(inspect.getmembers(echo.masks, inspect.isfunction))

    # Sort these filters, although it is not needed, it is helpful.
    sorted_filter_list = echo.echo_funct.echo_sort_masking_dictionary(filter_list)

    # Filters are generally required to have the 'echo' prefix.
    for keydex, filterdex in copy.deepcopy(sorted_filter_list).items():
        # Remove those that are not filters.
        if (not 'echo' in keydex):
            __ = sorted_filter_list.pop(keydex, None)
        else:
           continue

    # Return the filters, rename for documentation purposes. 
    echo_filter_dict = copy.deepcopy(sorted_filter_list)
    return echo_filter_dict

def smeargle_avaliable_oscar_plotting_functions():
    """ This returns a dictionary of the available plotting functions found 
    in OSCAR which can be used.

    Parameters
    ----------
    nothing

    Returns
    -------
    oscar_plotting_dict : dictionary
        This is a collection of all of the available plotting functions that 
        are usable.
    """

    # Obtain the dictionary of the OSCAR line to process into the 
    # individual functions and to ignore the other unneeded methods. 
    complete_oscar_dict = dict(inspect.getmembers(oscar, inspect.ismodule))

    # Filter only those functions belonging to IfA-Smeargle, then OSCAR. 
    # This is done using the source file location names and the file
    # naming conventions of IfA-Smeargle. 
    source_file_list = [inspect.getsourcefile(complete_oscar_dict[keydex]) 
                        for keydex in complete_oscar_dict.keys()]
    ifa_smeargle_file_list = [filedex for filedex in source_file_list 
                              if 'IfA_Smeargle' in filedex]
    oscar_file_list = [filedex for filedex in ifa_smeargle_file_list 
                       if 'oscar' in filedex]

    # The module names as a normal name, rather than the file path to the
    # python file. 
    oscar_mod_name_list = [inspect.getmodulename(oscardex) 
                           for oscardex in ifa_smeargle_file_list if 'oscar' in oscardex]

    # Module specifications and the frozen versions of the modules 
    # themselves. 
    oscar_modspec = [importlib.util.spec_from_file_location(namedex, filedex) 
                     for namedex, filedex in zip(oscar_mod_name_list, oscar_file_list)]
    oscar_modules = [importlib.util.module_from_spec(specdex) 
                     for specdex in oscar_modspec]

    # Un-freezing and loading the OSCAR modules to be used and reloaded
    # for its plotting functions. 
    for specdex, moduledex in zip(oscar_modspec, oscar_modules):
        specdex.loader.exec_module(moduledex)

    # All filtered functions belonging to the OSCAR module that only
    # contains the functions from IfA-Smeargle.
    function_dictionaries = [dict(inspect.getmembers(moduledex, inspect.isfunction)) 
                             for moduledex in oscar_modules]

    # The  function dictionary has some functions from IfA.meta and 
    # from the OSCAR functions module, that is, it does not contain any 
    # real significance for the plotting functionality to add a wrapper 
    # for. 
    oscar_plotting_functions = {}
    for dictionarydex in function_dictionaries: 
        oscar_plotting_functions = {**oscar_plotting_functions, **dictionarydex}
    for keydex, valuedex in copy.deepcopy(oscar_plotting_functions).items():
        # Removing the IfA.meta additives.
        if ('smeargle' in keydex):
            oscar_plotting_functions.pop(keydex, None)
        # Plots such as these require the entire directory of data and 
        # are not applicible for this class. 
        if ('plotdir' in keydex):
            oscar_plotting_functions.pop(keydex, None)
        # Removing everything else that is not considered a plotting
        # function. 
        if ('plot' not in keydex):
            oscar_plotting_functions.pop(keydex, None)

    # For documentation purposes.
    oscar_plotting_dict = copy.deepcopy(oscar_plotting_functions) 
    return oscar_plotting_dict