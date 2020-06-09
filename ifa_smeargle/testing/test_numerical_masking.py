
"""
This tests the masking functions to ensure that they are 
appropriately calculating the masks as expected.

These mask tests operate on the principle that the product of single 
power prime integers is always unique, and by extension, so are 
their logarithms. Prime number arrays are masked, multiplied 
together, and compared against an expected hard-coded result.
"""

import numpy as np
import numpy.ma as np_ma
import pytest
import sympy as sy
import math

import ifa_smeargle.core as core
import ifa_smeargle.masking as mask


def test_mask_single_pixels():
    """ This tests the masking of single pixels."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    # Every other column.
    column_indexes = [1,2,3,4,8,7,6,5,1,1,8,8]
    row_indexes = [1,2,3,4,5,6,7,8,8,6,1,3]
    # Create the mask.
    test_mask = mask.mask_single_pixels(data_array=test_array, 
                                        column_indexes=column_indexes, 
                                        row_indexes=row_indexes)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '192.684278256839293972761174821265114117452620'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_rectangle():
    """ This tests the masking of a rectangle, checking for 
    inclusive bounds as documented."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    # Every other column.
    column_range = [1,3]
    row_range = [5,9]
    # Create the mask.
    test_mask = mask.mask_rectangle(data_array=test_array, 
                                   column_range=column_range, 
                                   row_range=row_range)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '181.420681280111414609737593564884506705539966'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_subarray():
    """ This tests the masking of the sub-arrays, checking for 
    inclusive bounds as documented."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    # Every other column.
    column_range = [2,7]
    row_range = [3,6]
    # Create the mask.
    test_mask = mask.mask_subarray(data_array=test_array, 
                                   column_range=column_range, 
                                   row_range=row_range)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '56.3707446027708450564362652684182233131700807'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_columns():
    """ This tests the masking of every other column to ensure none  
    are masked."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    # Every other column.
    column_list = [1,3,5,7,9]

    # Create the mask.
    test_mask = mask.mask_columns(data_array=test_array, 
                                  column_list=column_list)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '109.272771336794561690334546364566516721293116'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_rows():
    """ This tests the masking of every other row to ensure none 
    are masked."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    # Every other row.
    row_list = [1,3,5,7,9]

    # Create the mask.
    test_mask = mask.mask_rows(data_array=test_array, row_list=row_list)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '104.096554239102333101253207803525242280036787'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_nothing():
    """ This tests the masking of all pixels to ensure none are 
    masked."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    pass

    # Create the mask.
    test_mask = mask.mask_nothing(data_array=test_array)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_STRING = '219.673198903714619732225307280947191575466862'
    CHECK_LOGARITHM = sy.Float(CHECK_STRING)
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None

def test_mask_everything():
    """ This tests the masking of all pixels to ensure none are 
    missed."""

    # Creating the testing array.
    test_array = _create_test_array(shape=(10,10))

    # Prescribed masking parameters
    pass

    # Create the mask.
    test_mask = mask.mask_everything(data_array=test_array)
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask, dtype=int)

    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_LOGARITHM = -np.inf
    __, __, product_log10 = core.math.ifas_large_integer_array_product(
        integer_array=test_masked_array.compressed())

    # Finally, check. As we are dealing with large single power
    # prime composite numbers and long decimals, and the smallest 
    # factor change of removing the 2 product still changes the
    # logarithm enough, checking if the logs are close is good 
    # enough.
    assert_message = ("The check logarithm is: {check}  "
                      "The product logarithm is: {log} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_LOGARITHM, log=product_log10,
                              array=test_masked_array))
    assert math.isclose(product_log10, CHECK_LOGARITHM), assert_message
    # All done.
    return None


def _create_test_array(shape):
    """ This creates a test array for the purposes of creating 
    masks and to apply them and test them. This ensures a 
    uniform test array for all mask tests."""

    # And the numbers that create the array.
    test_array_values = core.math.generate_prime_numbers(
        index=0, count=np.prod(shape))

    # And reshape into the correct array shape.
    test_array = np.reshape(test_array_values, shape)
    # All done.
    return test_array