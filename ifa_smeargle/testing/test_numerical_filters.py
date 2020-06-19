"""
This tests the filter functions to ensure that they are 
appropriately calculating the filters as expected.

These filter tests operate on the principle that the product of 
single power prime integers is always unique, and by extension, 
so are their logarithms. Prime number arrays are filtered, 
multiplied together, and compared against an expected hard-coded 
result.
"""

import numpy as np
import numpy.ma as np_ma
import pytest
import sympy as sy
import math

import ifa_smeargle.core as core
import ifa_smeargle.masking as mask
import ifa_smeargle.testing as test


def test_filter_sigma_value():
    """ This tests the filtering of sigma boundaries."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(10,10), index=50)

    # Prescribed filtering parameters
    # 1 Sigma
    sigma_multiple = 1
    sigma_iterations = 2
    # Create the filter.
    test_filter = mask.filter_sigma_value(data_array=test_array, 
                                          sigma_multiple=sigma_multiple,
                                          iterations=sigma_iterations)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '92.7429789714003440708375243748487223136051046'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_percent_truncation():
    """ This tests the filtering of percent truncations."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # Prescribed filtering parameters
    # The top 35% and bottom 10%.
    top_percent = 0.35
    bottom_percent = 0.10
    # Create the filter.
    test_filter = mask.filter_percent_truncation(
        data_array=test_array, top_percent=top_percent, 
        bottom_percent=bottom_percent)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '48.3986809684295405908025212823332315778806862'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_pixel_truncation():
    """ This tests the filtering of pixel boundaries."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # Prescribed filtering parameters
    # Top 13 pixels and bottom 9.
    top_count = 13
    bottom_count = 9
    # Create the filter.
    test_filter = mask.filter_pixel_truncation(data_array=test_array,
                                               top_count=top_count,
                                               bottom_count=bottom_count)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '51.0043131557317283360473320982116998982267737'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_maximum_value():
    """ This tests the filtering of values above a maximum."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # Prescribed filtering parameters
    # The value 113 should not be masked.
    maximum_value = 113
    # Create the filter.
    test_filter = mask.filter_maximum_value(data_array=test_array,
                                            maximum_value=maximum_value)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '46.4998252465517387337527237516559582272076600'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_minimum_value():
    """ This tests the filtering of values below a minimum."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # Prescribed filtering parameters.
    # The value 101 itself should not be masked.
    minimum_value = 101
    # Create the filter.
    test_filter = mask.filter_minimum_value(data_array=test_array,
                                            minimum_value=minimum_value)
    # Create a filter array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '52.5579255086291590806495158287835916351211866'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_exact_value():
    """ This tests the filtering of exact values."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # Prescribed filtering parameters
    exact_value = 101
    # Create the filter.
    test_filter = mask.filter_exact_value(data_array=test_array,
                                          exact_value=exact_value)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter, dtype=int)

    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '86.9163820638011874618505104537286754939523446'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_filter_invalid_value():
    """ This tests the filtering of invalid values."""

    # Creating the testing array.
    test_array = test.base.create_prime_test_array(shape=(7,7))

    # We need to force invalid values as the prime test creation
    # does not have them.
    test_array = np.array(test_array,dtype=float)
    test_array[1:3,2] = np.inf
    test_array[2,4:6] = -np.inf
    test_array[5,1:6] = np.nan

    # Prescribed filtering parameters
    pass
    # Create the filter.
    test_filter = mask.filter_invalid_value(data_array=test_array)
    # Create a filtered array for both convince and testing.
    test_filtered_array = np_ma.array(test_array, mask=test_filter)
    print(test_filtered_array)
    # A properly completed filter should have the same product value 
    # as this number. This is how the filter is checked.
    CHECK_STRING = '70.8884174145533646297736729939104459590381610'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_filtered_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The filtered array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_filtered_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None
