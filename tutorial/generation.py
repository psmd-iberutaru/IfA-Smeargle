
"""
These functions generates all of the required tutorial data,
configurations, and other needed objects to begin or run through
the tutorial.
"""

import copy
import shutil
import os
import numpy as np
import numpy.random as np_rand

import IfA_Smeargle.core as core

def tutorial_generate_fits_file(generation_mode, data_shape, 
                                fill_value=None, seed=None, range=None):
    """ This function generates a fits file that emulate 
    the real data in some regards. The different modes can create 
    different data representations.

    Parameters
    ----------
    generation_mode : string
        The generation mode that the data will adhere to. 
            
            * 'fill' : The fits data values are some constant number.
            * 'increment' : The files data values are created by 
            counting up individually. Order is based on C indexing.
            * 'pseudorandom' : The fits data values are generated 
            using a set seed and a pseudorandom number generator.
            * 'random' : The fits data values are generated randomly 
            as determined by undetermined-seed random number 
            generator.
    data_shape : tuple
        The shape of the data that will be created.
    fill_value : float (optional)
        The value that fills the data array. Only used if 
        the generation mode is `fill`.
    seed : int (optional)
        The seed value for the pseudorandom number generator. Only
        used if the generation mode is `pseudorandom`.
    range : array-like (optional)
        The range for the pseudorandom and the random number 
        generator. It takes only the highest and lowest numbers in 
        the tuple as the appropriate range. The range is [min, max).
        Defaults to [0.0, 1.0).

    Returns
    -------
    hdu_object : Astropy HDU object
        An object representation of the fits file. The header is 
        also generated.
    """
    # Simple type checking for the data generation mode.
    try:
        generation_mode = str(generation_mode)
    except Exception:
        raise core.error.InputError("The generation_mode cannot be turned "
                                    "into a string. The input must be a "
                                    "string.")
    # Simple type checking for the shape of the data array.
    data_shape = tuple(np.array(data_shape, dtype=int).tolist())
    
    # Decide on which method to generate a data array and run 
    # with it.
    if (generation_mode.lower() == 'fill'):
        # All of the data should be a constant value.
        if (fill_value is None):
            # But... they didn't give us the value...
            raise core.error.InputError("The `fill_value` for the data array "
                                        "creation is missing.")
        # Create the data array.
        data_array = np.full(data_shape, fill_value)
    elif (generation_mode.lower() == 'increment'):
        # All of the data is incremented values.

        # The total number of data values that need to be generated.
        n_total = np.sum(np.array(tuple(data_shape), dtype=int))
        # The data array through incremental generation. Creating
        # the data array.
        data_array = np.arange(n_total).reshape(tuple(data_shape))
    elif (generation_mode.lower() == 'pseudorandom'):
        # All of the data should be a random value based on the seed.
        
        # Checking if the seed exists.
        if (seed is None):
            # But... they didn't give us the seed...
            core.error.ifas_warning(core.error.InputWarning,
                                    "The `seed` for the random number "
                                    "generator is missing. The set seed "
                                    "of seed=42 will be used.")
            # Using a default seed.
            seed = 42
        # Also check for the range, if it was provided, evaluate the
        # minimum and maximum for number generation.
        if (range is None):
            # They didn't give us a range either.
            core.error.ifas_warning(core.error.InputWarning,
                                  ("The `range` for the random number "
                                  "generator is missing. Using the defaults "
                                  "0.0 and 1.0 instead as [0.0, 1.0)."))
            min_range = 0.0
            max_range = 1.0
        else:
            # Assigning the range based on their inputs.
            min_range = np.nanmin(np.array(range, dtype=float))
            max_range = np.nanmax(np.array(range, dtype=float))
            # Test if their inputs for the maximum and minimum are
            # the same, it would make little sense if they did. 
            # Handle float-based equality.
            float_tolerance = core.runtime.extract_runtime_configuration(
                config_key='FLOAT_EQUALITY_TOLERANCE')
            if (np.isclose(min_range, max_range, rtol=float_tolerance)):
                core.error.ifas_error(core.error.InputErrro,
                                      ("The minimum and maximum values "
                                       "allowed for pseudorandom number "
                                       "generation are very close. The "
                                       "array might be populated with the "
                                       "same value."))

        # Psuedorandom data as generated from the seed. The shape is
        # also factored in.
        random_data = np_rand.default_rng(seed).random(data_shape)

        # The numbers are currently [0,1). This scales them to be
        # [min, max) as specified by the range of random values.
        # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.random.html#numpy.random.Generator.random 
        # Creating the data array also.
        data_array = min_range + (max_range - min_range) * random_data

    elif (generation_mode.lower() == 'random'):
        # The numbers provided should be completely random.

        # Checking to see if the range was provided. If not, default
        # to the normal [0.0, 1.0).
        if (range is None):
            # They didn't give us a range either.
            core.error.ifas_warning(core.error.InputWarning,
                                  ("The `range` for the random number "
                                   "generator is missing. Using the defaults "
                                   "0.0 and 1.0 instead as [0.0, 1.0)."))
            min_range = 0.0
            max_range = 1.0
        else:
            # Assigning the range based on their inputs.
            min_range = np.nanmin(np.array(range, dtype=float))
            max_range = np.nanmax(np.array(range, dtype=float))
            # Test if their inputs for the maximum and minimum are
            # the same, it would make little sense if they did. 
            # Handle float-based equality.
            float_tolerance = core.runtime.extract_runtime_configuration(
                config_key='FLOAT_EQUALITY_TOLERANCE')
            if (np.isclose(min_range, max_range, rtol=float_tolerance)):
                core.error.ifas_error(core.error.InputError,
                                      ("The minimum and maximum values "
                                       "allowed for random number generation "
                                       "are very close. The array might be "
                                       "populated with the same value."))

        # Random data as generated from the seed. The shape is
        # also factored in. A None seed forces the usage of the 
        # machine's random number seed generator, or its clock. 
        # Both are good enough.
        random_data = np_rand.default_rng(None).random(data_shape)

        # The numbers are currently [0,1). This scales them to be
        # [min, max) as specified by the range of random values.
        # See https://cutt.ly/kyUUmgC .
        # Creating the data array also.
        data_array = min_range + (max_range - min_range) * random_data
    else:
        # The generation mode is not a valid input.
        raise core.error.InputError("The generation mode input is not a "
                                    "valid mode of data generation. "
                                    "Current input: {input}"
                                    .format(input=generation_mode))

    # The data array should only be integers, mirroring 
    # SAPHIRA arrays as they are integer only.
    data_array = np.array(data_array, dtype=int)

    # Creating the header for this file.
    data_header = {'TUTORIAL':True,
                   'data_generator':generation_mode.lower(),
                   'data_shape':str(data_shape),
                   'fill_value':fill_value, 
                   'seed':seed, 
                   'range':str(range)}

    # Creating the Astropy object. There is no need to write it to
    # file.
    hdu_object = core.io.write_fits_file(
        file_name=None, hdu_header=data_header, hdu_data=data_array, 
        hdu_object=None, save_file=False, overwrite=False, silent=True)

    # All done, return.
    return hdu_object

