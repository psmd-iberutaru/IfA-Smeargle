
import argparse
import inspect
import os
import sys

try:
    from IfA_Smeargle.meta import *
    from IfA_Smeargle import yankee
    from IfA_Smeargle import zulu
except (ModuleNotFoundError, ValueError):
    # Path hack, mostly likely because this python file 
    # is in the same directory of the package as is default.
    sys.path.insert(0, os.path.abspath('.'))
    sys.path.insert(0, os.path.abspath('..'))
    # Try again...
    from IfA_Smeargle.meta import *
    from IfA_Smeargle import yankee
    from IfA_Smeargle import zulu


    



def execute_ifas_smeargle(pipeline_name, data_directory, config_class_path,
                          silent=False):
    """ This takes the input from an argparser and executes the proper 
    pipeline.

    This function takes string information and parses and executes the input
    to the best of the ability of this module. This function cannot be called
    unless it via the command-line execution route. 

    Parameters
    ----------
    pipeline_name : string
        The name of the data reduction pipeline that will be used.
    data_directory : string
        The path to the data, specifically where the data is all stored in.
    config_class_path : string
        The file path (including the file) that describes where the 
        configuration class lies.
    silent : boolean (optional)
        Turn off all warnings and information sent by this function and 
        functions below it.

    Returns
    -------
    pipeline_results : unknown
        Returns exactly what the pipeline function would have returned.
    """

    # Check if the user wanted this function to be silent. 
    if (silent):
        with smeargle_absolute_silence():
            return execute_ifas_smeargle(pipeline_name, data_directory, config_class_path)

    # This function should not be executed if this is not instigated from the 
    # command line.
    if (__name__ != '__main__'):
        raise IllogicalProsedureError("This function is not supposed to operate outside of the "
                                      "command-line execution method. Please use the ZULU "
                                      "line if running this program via imports.")
    else:
        smeargle_info("Executing the following pipeline:  " + pipeline_name)

    # Gather all of the possible available pipelines. 
    pipeline_dictionary = dict(inspect.getmembers(zulu.pipelines, inspect.isfunction))

    # Try and attempted to get the pipeline function itself.
    try:
        pipeline_function = pipeline_dictionary[pipeline_name]
    except KeyError:
        raise InputError("There does not exist a pipeline of name <{pipe_name}>. Double check "
                         "the inputted pipeline name."
                         .format(pipe_name=pipeline_name))

    # Try and get the configuration class itself.
    try:
        configuration_class = yankee.SmeargleConfig(config_class_path)
    except Exception:
        # It seemed that the standard method could not return a good 
        # configuration class. Attempt to read with the factory function.
        configuration_class = yankee.configuration_factory_function(yankee.SmeargleConfig, 
                                                                    file_name=config_class_path)
    
    # Check if the file directory provided is a valid data directory. Be
    # generous on the definition of a 'directory'.
    if (not os.path.exists(data_directory)):
        raise InputError("The data directory <{data_dir}> does not seem to exist. Double check "
                         "the inputted data directory and its contents."
                         .format(data_dir=data_directory))

    # The parameters given pass all of the elements provided. Execute the 
    # pipeline. Assume it is in the following format (as all other pipelines
    # coded by Sparrow are).
    pipeline_results = pipeline_function(data_directory, configuration_class)

    # And finally return
    return pipeline_results


if (__name__ == '__main__'):
    # Creating the argpaser
    parser = argparse.ArgumentParser(description=("Execute a IfA-Smeargle data reduction and "
                                                  "analysis pipeline via a command-line call."))

    # Adding the three required arguments for all pipelines. These are always
    # constant requirements and thus are positional.
    parser.add_argument("pipeline", help=("The name of the ZULU pipeline that is "
                                          "going to be executed in the command call."),
                        type=str)
    parser.add_argument("data_dir", help=("The path to the directory that holds the data "
                                          "that the pipeline will work on."),
                        type=str)
    parser.add_argument("config_file", help=("The path to the .ifaspkl SmeargleConfig "
                                             "configuration file which will be used."),
                        type=str)

    # Optional arguments.
    parser.add_argument("-s", "--silent", help=("Run the pipeline silenced; no info or "
                                                "warnings printed."),
                        action="store_true")

    # Parse the arguments.
    args = parser.parse_args()

    # Extract the arguments for visual purposes.
    pipeline = str(args.pipeline)
    data_dir = str(args.data_dir)
    config_file = str(args.config_file)
    silent = bool(args.silent)

    # Execute the file. The return is likely lost anyways.
    __ = execute_ifas_smeargle(pipeline_name=pipeline, data_directory=data_dir, 
                               config_class_path=config_file, silent=silent)
    