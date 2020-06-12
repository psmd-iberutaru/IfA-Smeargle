
"""
This file contains methods used to determine proper naming 
conventions and to reformat the fits file names from raw output 
(often just timestamps) to something more useful and accurate to the 
data.
"""


import glob
import os 
import string


import ifa_smeargle.core as core

def _get_renaming_delimiter_string():
    """ This function gets the delimiter string along with setting
    """
    # This is the delimiter string; it should be common for all 
    # renaming functions.
    delimiter = str(core.runtime.extract_runtime_configuration(
        config_key='RENAMING_DELIMITER'))
    # It also cannot be a number.
    try:
        if (not isinstance(delimiter, str)):
            raise core.error.ConfigurationError("The renaming delimiter "
                                                "must be a string. It is "
                                                "type: {type}"
                                                .format(type=type(delimiter)))
        # This should raise a ValueError, it is caught and dealt 
        # with.
        __ = float(delimiter)

        # It did not... the delimiter may be wrong.
        raise RuntimeError
    except ValueError:
        # This is normal behavior, it should be a string that cannot be
        # a number.
        return delimiter
    except RuntimeError:
        raise core.error.ConfigurationError("The renaming delimiter should "
                                            "not be able to be turned into "
                                            "a number. A numerical splitter "
                                            "will lead to confusion. The "
                                            "current delimiter: {delim} "
                                            .format(delim=delimiter))
    # The code should not reach here. It should have either 
    # returned or failed the float conversion.
    raise core.error.BrokenLogicError
    return None
# The delimiter.
RENAMING_DELIMITER = _get_renaming_delimiter_string()


def rename_detector(data_directory, detector_name):
    """ Creates file tags according to the detector qualifier name.
    
    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to 
        be renamed.
    detector_name : string
        The detector name that should be applied.

    Returns
    -------
    detector_string_list : list
        This is the list of the state on if the object is garbage or 
        not.
    detector_raw_list : list 
        This is the raw, unformatted values that was formatted into 
        the string version.
    """
    # The total number of fits files.
    n_files = len(core.io.get_fits_filenames(data_directory=data_directory))
    
    # Apply the detector name to all files.
    detector_raw_list = [str(detector_name) for filedex in range(n_files)]
    detector_string_list = [''.join(['detector', RENAMING_DELIMITER,
                                     detectordex]) 
                            for detectordex in detector_raw_list]

    return detector_string_list, detector_raw_list

def rename_garbage(data_directory, begin_garbage=0):
    """ Creates file tags according to their status as garbage. If 
    a file is garbage, it should generally not be used.

    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to 
        be renamed.
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count 
        as data, (i.e. the number of garbage files).

    Returns
    -------
    garbage_string_list : list
        This is the list of the state on if the object is garbage 
        or not.
    garbage_raw_list : list 
        This is the raw, unformatted values that was formatted 
        into the string version.
    """
    # The total number of fits files.
    n_files = len(core.io.get_fits_filenames(data_directory=data_directory))

    # The status on if the object is garbage or not.
    garbage_raw_list = [True if index < begin_garbage else False 
                        for index in range(n_files)]
    # And their formatted string value.
    yes_garbage = ''.join(['garb', RENAMING_DELIMITER, 'Y'])
    no_garbage = ''.join(['garb', RENAMING_DELIMITER, 'N'])
    garbage_string_list = [yes_garbage if garbdex else no_garbage
                           for garbdex in garbage_raw_list]

    # Finished.
    return garbage_string_list, garbage_raw_list

def rename_number(data_directory, begin_garbage=0):
    """ Creates file tags according to their number in order.

    Some data filename outputs only give timestamps. This function 
    renames said filenames for better processing.  
    
    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files to 
        be renamed.
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count 
        as data.

    Returns
    -------
    number_string_list : list
        This is the list of the numbered strings applied, given in 
        a parallel ordered form. Does not include prefixes/suffixes.
    number_raw_list : list
        This is the raw, unformatted values that was formatted 
        into the string version.
    """
    
    # The files that are before the garbage denotation should be 
    # labeled as such.
    garbage_names = core.io.get_fits_filenames(
        data_directory=data_directory)[:begin_garbage]
    garbage_paths = [os.path.split(garbagepathdex)[0] 
                     for garbagepathdex in garbage_names]
    n_garbage_files = len(garbage_names)


    # For the files to be renamed.
    original_names = core.io.get_fits_filenames(
        data_directory=data_directory)[begin_garbage:]
    original_paths = [os.path.split(pathdex)[0] 
                      for pathdex in original_names]
    n_files = len(original_names)

    # Each file number, separating the garbage and the non-garbage 
    # numbers. There is no reason to lump the two together without 
    # denotation.
    garbage_numbers = [(index + 1) for index in range(n_garbage_files)]
    file_numbers = [(index + 1) for index in range(n_files)]

    # Converting the numbers to their new names. The `garbage` \
    # prefix to the number is a standard. Any file with garbage in 
    # the name is not processed.
    garbage_string_list = [''.join(['num', RENAMING_DELIMITER, 'garbage', 
                                    str(numdex)])
                           for numdex in garbage_numbers]
    file_string_list = [''.join(['num', RENAMING_DELIMITER, str(numdex)])
                        for numdex in file_numbers]

    # The completed lists.
    number_file_list = garbage_string_list + file_string_list
    number_raw_list = garbage_numbers + file_numbers

    return number_file_list, number_raw_list

def rename_set(data_directory, set_length, begin_garbage=0):
    """ Creates file tags according to their set number, as 
    determined by the number of files in a set. Sets are assumed 
    to be consecutive.

    Some data filename outputs only give timestamps. This function 
    renames said filenames for better processing.  
    
    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files 
        to be renamed.
    set_length : int 
        This is the length of a set. 
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not 
        count as data.

    Returns
    -------
    set_string_list : list
        This is the list of the numbered strings applied, given in 
        a parallel ordered form. Does not include prefixes/suffixes.
    set_raw_list : list
        This is the raw, unformatted values that was formatted 
        into the string version.
    """

    # The files that are before the garbage denotation should be 
    # labeled as such.
    garbage_names = core.io.get_fits_filenames(
        data_directory=data_directory)[:begin_garbage]
    garbage_paths = [os.path.split(garbagepathdex)[0] 
                     for garbagepathdex in garbage_names]
    n_garbage_files = len(garbage_names)


    # For the files to be renamed.
    original_names = core.io.get_fits_filenames(
        data_directory=data_directory)[begin_garbage:]
    original_paths = [os.path.split(pathdex)[0] 
                      for pathdex in original_names]
    n_files = len(original_names)

    # Each file number, separating the garbage and the non-garbage 
    # numbers. There is no reason to lump the two together without 
    # denotation.
    garbage_numbers = [(index + 1) for index in range(n_garbage_files)]
    file_numbers = [(index + 1) for index in range(n_files)]

    # Converting the numbers to their new names. The `garbage` 
    # prefix to the number is a standard. Any file with garbage in 
    # the name is not processed.
    garbage_string_list = [''.join(['set', RENAMING_DELIMITER, 'garbage', 
                                    str((numdex-1)//set_length + 1)]) 
                           for numdex in garbage_numbers]
    file_string_list = [''.join(['set', RENAMING_DELIMITER, 
                                 str((numdex-1)//set_length + 1)])
                        for numdex in file_numbers]

    # The completed list.
    set_file_list = garbage_string_list + file_string_list
    set_raw_list = garbage_numbers + [(numdex-1)//set_length + 1 
                                      for numdex in file_numbers]

    return set_file_list, set_raw_list

def rename_voltage_pattern(data_directory, voltage_pattern, 
                           begin_garbage=0):
    """ Creates file tags according to their voltage pattern 
    specified.

    Some data filename outputs only give timestamps. This function 
    renames said filenames for better processing.

    The output files created are according to the voltage pattern 
    that the user specified. This function assumes that the pattern 
    provided is one 'set', where a set contains some amount of fits 
    files. Moreover, this function weakly determines which are 
    up-mid-down ramps. 

    Parameters
    ----------
    data_directory : string
        This is the directory that contain all of the data files 
        to be renamed.
    voltage_pattern : array_like
        These are voltage values, assuming that the first element 
        is the first voltage element to be used, proceeding from 
        there in order.
    begin_garbage : int (optional)
        The number of files, in the beginning, that should not count 
        as data.

    Returns
    -------
    voltage_string_list : list
        This is the list of the voltage strings applied, given in 
        a parallel ordered form. Does not include prefixes/suffixes.
    voltage_raw_list : dictionary
        This is the raw, unformatted values that was formatted 
        into the string version. The voltage values and trends are 
        separated (as `value` and `trend`).

    """

    # The files that are before the garbage denotation should be 
    # labeled as such.
    garbage_names = core.io.get_fits_filenames(
        data_directory=data_directory)[:begin_garbage]
    garbage_paths = [os.path.split(garbagepathdex)[0] 
                     for garbagepathdex in garbage_names]
    n_garbage_files = len(garbage_names)


    # For the files to be renamed.
    original_names = core.io.get_fits_filenames(
        data_directory=data_directory)[begin_garbage:]
    original_paths = [os.path.split(pathdex)[0] 
                      for pathdex in original_names]
    n_files = len(original_names)

    
    # Formatting the voltage trends by the increase or decrease 
    # of the voltages.
    n_voltages = len(voltage_pattern)
    voltage_strings = []
    # This is just for renaming and smaller lines.
    vlt_patt = voltage_pattern
    for voltindex in range(n_voltages):
        temp_voltage_string = ''
    
        # Record the voltage number.
        temp_voltage_string += str(vlt_patt[voltindex]) + 'V'
    
        # Detecting if the voltage is overall increasing, 
        # decreasing, or peaking. The odd modular division is to 
        # handle the last voltage effectively. 
        if (vlt_patt[voltindex - 1] == vlt_patt[voltindex] and 
            vlt_patt[voltindex] == vlt_patt[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are equal, this is a flat slope.
            temp_voltage_string += 'mid'
        elif (vlt_patt[voltindex - 1] <= vlt_patt[voltindex] and 
              vlt_patt[voltindex] <= vlt_patt[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are sloped upwards.
            temp_voltage_string += 'up'
        elif (vlt_patt[voltindex - 1] >= vlt_patt[voltindex] and 
              vlt_patt[voltindex] >= vlt_patt[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are sloped downwards.
            temp_voltage_string += 'down'
        elif (vlt_patt[voltindex - 1] <= vlt_patt[voltindex] and 
              vlt_patt[voltindex] >= vlt_patt[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are lower than this voltage.
            temp_voltage_string += 'top'
        elif (vlt_patt[voltindex - 1] >= vlt_patt[voltindex] and 
              vlt_patt[voltindex] <= vlt_patt[(voltindex + 1)%n_voltages]):
            # Surrounding voltages are higher than this voltage.
            temp_voltage_string += 'bot'
        else:
            # For some reason, it does not fit into the pattern.
            temp_voltage_string += 'null'

        # Label, Windows does not like the colon or pipe, so, we 
        # use the next best thing. Allow the setting of the 
        # uniform delimiter.
        temp_voltage_string = ''.join(['detBias', RENAMING_DELIMITER,
                                      temp_voltage_string])


        # Save and record.
        voltage_strings.append(temp_voltage_string)

    # Compile the garbage files. The garbage 'prefix' to the 
    # number is a standard. Any file with garbage in the name is not 
    # processed.
    garbage_string_list = []
    for fileindex in range(n_garbage_files):
        garbage_string = 'garbage' + str(fileindex + 1).zfill(3)
        garbage_string_list.append(garbage_string)

    # Compile the renames, assume that the sets repeat themselves 
    # if there are more files than voltages . Then actually rename 
    # the file.
    voltage_string_list = []
    for fileindex in range(n_files):
        volt_string = str(voltage_strings[fileindex%n_voltages])
        voltage_string_list.append(volt_string)

    # Extracting the raw values from the formatted values and 
    # converting.
    _purge_volt_substrings = (list(string.ascii_uppercase) 
                        + list(string.ascii_lowercase) 
                        + [':',';', RENAMING_DELIMITER])
    raw_voltages = [float(core.strformat.purge_substrings(
        string=voltdex, substrings=_purge_volt_substrings))
                    for voltdex in (garbage_string_list 
                                    + voltage_string_list)]
    _purge_trend_substrings = (list(string.digits) + ['.',RENAMING_DELIMITER,
                                                      'detBias','V'])
    raw_trends = [str(core.strformat.purge_substrings(
        string=voltdex, substrings=_purge_trend_substrings))
                    for voltdex in (garbage_string_list 
                                    + voltage_string_list)]


    # Finished, it is also helpful to return the garbage file names.
    voltage_string_list = garbage_string_list + voltage_string_list
    voltage_raw_list = {'value':raw_voltages, 'trend':raw_trends}

    return voltage_string_list, voltage_raw_list    





def script_rename_detector(config):
    """ The scripting version of `rename_detector`. This function 
    applies the rename to the entire directory. It also adds the 
    tags to the header file of each fits.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for 
        this function.

    Returns
    -------
    None
    """

    # Extract the configuration parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    detector_name = core.config.extract_configuration(
        config_object=config, keys=['renaming','detector_name'])

    # Obtain the labels.
    labels, raw = rename_detector(data_directory=data_directory, 
                                  detector_name=detector_name)
    
    # Add to all file headers. Assume that the order has not changed 
    # between renaming steps.
    core.error.ifas_info("Adding the detector name `{detect_name}` "
                         "under the `DETECTOR` card in the headers of the "
                         "fits files in {data_dir}."
                         .format(detect_name=detector_name, 
                                 data_dir=data_directory))
    fits_files = core.io.get_fits_filenames(data_directory=data_directory)
    for (filedex, headerdex) in zip(fits_files, raw):
        __ = core.io.append_astropy_header_card(
            file_name=filedex, header_cards={'DETECTOR':headerdex})

    # Finally rename the files based on parallel appending. Glob 
    # provides the directory.
    core.error.ifas_info("Appending the detector name to the end of the "
                         "files in {data_dir}."
                         .format(data_dir=data_directory))
    core.io.rename_by_parallel_append(file_names=fits_files, 
                                      appending_names=labels, 
                                      directory=None)

    return None

def script_rename_garbage(config):
    """ The scripting version of `rename_garbage`. This function 
    applies the rename to the entire directory. It also adds the 
    tags to the header file of each fits.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the configuration parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    begin_garbage = core.config.extract_configuration(
        config_object=config, keys=['renaming','begin_garbage'])

    # Obtain the labels.
    labels, raw = rename_garbage(data_directory=data_directory,
                                 begin_garbage=begin_garbage)
    
    # Add to all file headers. Assume that the order has not changed 
    # between renaming steps.
    core.error.ifas_info("Adding the garbage status under the `GARBAGE` "
                         "card in the headers of the fits files in "
                         "{data_dir}."
                         .format(data_dir=data_directory))
    fits_files = core.io.get_fits_filenames(data_directory=data_directory)
    for (filedex, headerdex) in zip(fits_files, raw):
        __ = core.io.append_astropy_header_card(
            file_name=filedex, header_cards={'GARBAGE':headerdex})

    # Finally rename the files based on parallel appending. Glob 
    # provides the directory.
    core.error.ifas_info("Appending the garbage status to the end of "
                         "the files in {data_dir}."
                         .format(data_dir=data_directory))
    core.io.rename_by_parallel_append(file_names=fits_files, 
                                      appending_names=labels, 
                                      directory=None)

    return None

def script_rename_number(config):
    """ The scripting version of `rename_number`. This function 
    applies the rename to the entire directory. It also adds the 
    tags to the header file of each fits.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """

    # Extract the configuration parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    begin_garbage = core.config.extract_configuration(
        config_object=config, keys=['renaming','begin_garbage'])

    # Obtain the labels.
    labels, raw = rename_number(data_directory=data_directory, 
                                begin_garbage=begin_garbage)
    
    # Add to all file headers. Assume that the order has not 
    # changed between renaming steps.
    core.error.ifas_info("Adding the file number under the `NUMBER` card "
                         "in the headers of the fits files in {data_dir} "
                         "based on the file order."
                         .format(data_dir=data_directory))
    fits_files = core.io.get_fits_filenames(data_directory=data_directory)
    for (filedex, headerdex) in zip(fits_files, raw):
        __ = core.io.append_astropy_header_card(
            file_name=filedex, header_cards={'NUMBER':headerdex})

    # Finally rename the files based on parallel appending. Glob 
    # provides the directory.
    core.error.ifas_info("Appending the file number to the end of "
                         "the files in {data_dir}."
                         .format(data_dir=data_directory))
    core.io.rename_by_parallel_append(file_names=fits_files, 
                                      appending_names=labels, 
                                      directory=None)

    return None

def script_rename_set(config):
    """ The scripting version of `rename_set`. This function 
    applies the rename to the entire directory. It also adds the 
    tags to the header file of each fits.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """

    # Extract the configuration parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    set_length = core.config.extract_configuration(
        config_object=config, keys=['renaming','set_length'])
    begin_garbage = core.config.extract_configuration(
        config_object=config, keys=['renaming','begin_garbage'])

    # Obtain the labels.
    labels, raw = rename_set(data_directory=data_directory, 
                               set_length=set_length, 
                               begin_garbage=begin_garbage)
    
    # Add to all file headers. Assume that the order has not 
    # changed between renaming steps.
    core.error.ifas_info("Adding the set number under the `SET_NUM` card "
                         "in the headers of the fits files in {data_dir} "
                         "based on the file order."
                         .format(data_dir=data_directory))
    fits_files = core.io.get_fits_filenames(data_directory=data_directory)
    for (filedex, headerdex) in zip(fits_files, raw):
        __ = core.io.append_astropy_header_card(
            file_name=filedex, header_cards={'SET_NUM':headerdex})

    # Finally rename the files based on parallel appending. Glob 
    # provides the directory.
    core.error.ifas_info("Appending the set number to the end of the "
                         "files in {data_dir}."
                         .format(data_dir=data_directory))
    core.io.rename_by_parallel_append(file_names=fits_files, 
                                      appending_names=labels, 
                                      directory=None)

    return None

def script_rename_voltage_pattern(config):
    """ The scripting version of `rename_voltage_pattern`. This 
    function applies the rename to the entire directory. It also 
    adds the tags to the header file of each fits.
    
    Parameters
    ----------
    config : ConfigObj
        The configuration object that is to be used for this 
        function.

    Returns
    -------
    None
    """
    # Extract the configuration parameters.
    data_directory = core.config.extract_configuration(
        config_object=config, keys=['data_directory'])
    voltage_pattern = core.config.extract_configuration(
        config_object=config, keys=['renaming','voltage_pattern'])
    begin_garbage = core.config.extract_configuration(
        config_object=config, keys=['renaming','begin_garbage'])

    # Obtain the labels. This one is a little special with its 
    # output; the raw contains two sections.
    labels, raw = rename_voltage_pattern(data_directory=data_directory, 
                                           voltage_pattern=voltage_pattern,
                                           begin_garbage=begin_garbage)
    # Split the sections.
    raw_volt_value = raw['value']
    raw_volt_trend = raw['trend']

    # Add to all file headers. Assume that the order has not 
    # changed between renaming steps.
    core.error.ifas_info("Adding the bias voltage under the `VOLTAGE` "
                         "card and the ramp slope under the `RAMPSLPE` card "
                         "in the headers of the fits files in "
                         "{data_dir} based on the file order."
                         .format(data_dir=data_directory))
    fits_files = core.io.get_fits_filenames(data_directory=data_directory)
    for (filedex, voltdex, trenddex) in zip(fits_files, 
                                            raw_volt_value, raw_volt_trend):
        __ = core.io.append_astropy_header_card(
            file_name=filedex, header_cards={'VOLTAGE':voltdex, 
                                             'RAMPSLPE':trenddex})

    # Finally rename the files based on parallel appending. Glob 
    # provides the directory.
    core.error.ifas_info("Appending the bias voltage number and slope to "
                         "the end of the files in {data_dir}."
                         .format(data_dir=data_directory))
    core.io.rename_by_parallel_append(file_names=fits_files, 
                                      appending_names=labels, 
                                      directory=None)

    return None
