
import glob
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as np_ma
import pandas as pd

from IfA_Smeargle import bravo
from IfA_Smeargle import yankee

from IfA_Smeargle.meta import *

def plotdir_dark_current_over_voltage(data_directory, figure_axes=None, configuration_class=None,
                                      **kwargs):
    """ This function plots the dark current as a function of voltage over
    all frames within a file directory.

    The plots provided serve to show the dark current as voltage increases. 
    This function attempts to execute and plot without the usage of a 
    configuration file; but, if it fails, specifying it will help.
    
    Parameters
    ----------
    data_directory : string
        The directory where all of the data files are stored.
    figure_axes : Matplotlib Axes (optional)
        This is a predefined axes variable that the user may desire to have 
        the trend plot to. This defaults to either making new ones, or 
        using the currently defined axes. This is not deep-copied!
    configuration_class : SmeargleConfig or OscarConfig class (optional)
        The configuration class that would assist in better plotting
        accuracy.
    Returns
    -------
    final_figure : Matplotlib Figure
        This is the final figure depicting the dark current change over time.
    data_arrays : dictionary
        This is a dictionary of the voltages, values, and error values as 
        processed.
    data_frame : Pandas dataframe
        This is a formal representation of all data of the entire data array 
        with regards to the plot.
    """

    # First, figure out what type of Matplotlib axes to use.
    if (figure_axes is not None):
        ax = figure_axes
    else:
        ax = plt.gca()

    # Load all of the fits files specified. Ensure that it is known that only
    # data directories are accepted.
    if (not isinstance(data_directory, str)):
        raise InputError("This plotting function requires the usage of a data directory path. "
                         "What has been provided is not a string path. ")
    else:
        file_names = glob.glob(data_directory + '/*' + '.fits')

    # Convert to the dictionary descriptions
    file_dictionaries = []
    for filenamedex in file_names:
        temp_dict = bravo.bravo_filename_split_by_parameter(filenamedex)
        if (temp_dict is None):
            # This generally means that the file is considered garbage and
            # should not be included.
            continue
        else:
            file_dictionaries.append(temp_dict)

    # Transform the dataframe so it contains mostly data specific to this
    # plot, along with the actual computed values.
    file_data = []
    for filedictdex in file_dictionaries:
        try:
            # The standard metadata
            file_metadict = {'num':filedictdex['num'], 'detector':filedictdex['detName'],
                             'volt':filedictdex['detBias'][0],'voltslope':filedictdex['detBias'][-1],
                             'topslice':filedictdex['slice'][0], 
                             'botslice':filedictdex['slice'][-1],
                             'filename':filedictdex['filename']}
            # The actual computed data for each of the data frames.
            __, __, data_array = meta_faa.smeargle_open_fits_file(filedictdex['filename'])
            __, gaussian_data = meta_model.smeargle_fit_histogram_gaussian_function(data_array,
                                                                                   bin_width=10)
            file_datadict = {'mean':np_ma.mean(data_array), 
                             'median':np_ma.median(data_array),
                             'stddev':np_ma.std(data_array), 
                             'g_mean':gaussian_data['mean'], 'g_stddev':gaussian_data['stddev'],
                             'g_amp':gaussian_data['amplitude'], 'g_max':gaussian_data['max']}
            file_data.append({**file_metadict, **file_datadict})
        except KeyError:
            continue
    file_data = pd.DataFrame(file_data)

    # Obtain the total voltages.
    try:
        voltage_list = copy.deepcopy(np.sort(np.unique(file_data.loc[:,'volt'].to_numpy())))
    except Exception:
        # Try instead with the configuration class.
        if (configuration_class is not None):
            try:
                configuration_class = yankee.yankee_extract_proper_configuration_class(
                    configuration_class, yankee.BravoConfig)
                voltage_pattern = configuration_class.voltpat_rename_config[voltage_pattern]
                voltage_list = np.sort(np.unique(voltage_pattern, axis=None))
            except Exception:
                raise ConfigurationError("The voltage list cannot be extracted from the "
                                         "filenames nor the configuration class. This plot "
                                         "cannot be done without a voltage list.")
        else:
            raise DataError("The voltage list cannot be extracted from filenames. There is no "
                            "configuration file input to rely on. Ensure that the filenames are "
                            "formatted by the BRAVO module and that the data is appropriate to "
                            "this plotting function.")

    # Derive all of the metadata needed to determine which set each numbered 
    # data file belongs to, and how it corresponds with their voltage 
    # and voltage ramp values.
    set_metadata = []
    for voltdex in voltage_list:
        slope_list = list(set(file_data.query('volt == @voltdex')['voltslope']))
        
        for slopedex in slope_list:
            query = file_data.query('volt == @voltdex and voltslope == @slopedex')['num']
            filenum = np.sort(np.unique(query))
            
            # It is assumed that the first voltslope up/down pair is the first
            # set, the second pair the second set, and so on. 
            for numdex, setdex in zip(filenum,np.arange(len(filenum))+1):
                temp_dict = {'metavolt':voltdex,'metaslope':slopedex,
                             'metanum':numdex,'metaset':setdex}
                set_metadata.append(temp_dict)
    # Store all of the information into a data frame.
    set_metadata = pd.DataFrame(set_metadata)

    # Find the total number of complete sets that are contained. Any 
    # incomplete set is not included for plotting.
    set_count = np.flip(np.unique(set_metadata['metaset']))\
        [np.flip(np.unique(set_metadata['metaset'],return_counts=True)[1]).argmax()]

    # For storing the information in 'data_arrays'.
    data_arrays = {}

    # Create different plots per set (over-plotting on the same figure).
    # All data is within the 'file_data' object, and the metadata
    # that helps extract said data is within the 'set_metadata' object.
    for setdex in (np.arange(set_count) + 1):
        # Extract only the current set.
        dataset_list = set_metadata.query('metaset == @setdex')
        
        # Temporary instantiations. 
        x_axis_voltage = []
        y_axis_data = []
        y_axis_error = []
        
        # Extract the data and store into list/array for plotting.
        for voltdex in voltage_list:
            fits_file_numbers = list(dataset_list.query('metavolt == @voltdex')['metanum'].to_numpy())
            voltset_data = file_data.query('num == @fits_file_numbers')
            
            x_axis_voltage.append(voltdex)
            y_axis_data.append(np.nanmedian(voltset_data['g_mean']))
            y_axis_error.append(np.nanmedian(voltset_data['g_stddev']))
            
        # Plot the data from this set as needed. Reuse the previous set's 
        # canvas for the overplotting. 
        x_axis_voltage = np.array(x_axis_voltage)
        y_axis_data = np.array(y_axis_data)
        y_axis_error = np.array(y_axis_error)
        ax.errorbar(x_axis_voltage, y_axis_data, yerr=y_axis_error,
                    fmt='.-', elinewidth=0.25, capsize=3, capthick=0.25,
                    label=('Set ' + str(setdex)))
        
        # Legend and other labels things. The title is always the detector 
        # name.
        ax.set_title(file_data['detector'][0])
        ax.legend(loc='upper left')
        ax.set_xticks(x_axis_voltage)
        ax.set_xlabel('Detector Bias Voltage (V)')
        ax.set_ylabel('Average Dark Current (ADU)')

        # Store the information.
        data_arrays.update({'voltage_set' + str(setdex):x_axis_voltage, 
                            'value_set' + str(setdex): y_axis_data, 
                            'error_set' + str(setdex):y_axis_error})
        
    # For naming conventions per documentation.
    final_figure = ax
    data_arrays = data_arrays
    data_frame = file_data

    return ax, data_arrays, data_frame