
"""
This contains a lot of functions that are common across all of the
testing functions and modules.
"""

import numpy as np

import ifa_smeargle.core as core

def create_prime_test_array(shape, index=0):
    """ This creates a test array for the purposes of creating 
    masks and to apply them and test them. This ensures a 
    uniform test array for all mask tests.
    
    Parameters
    ----------
    shape : tuple
        The shape of the data array.
    index : integer
        The index that the prime numbers should start from.

    Returns
    -------
    prime_test_array : ndarray
        The array filled with prime numbers.
    """

    # And the numbers that create the array.
    test_array_values = core.math.generate_prime_numbers(
        index=index, count=np.prod(shape))

    # And reshape into the correct array shape.
    prime_test_array = np.reshape(test_array_values, shape)
    # All done.
    return prime_test_array