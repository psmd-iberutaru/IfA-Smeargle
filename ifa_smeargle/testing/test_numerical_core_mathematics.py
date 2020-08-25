
"""
This module is made to test the mathematical functions of the 
core.mathematics section.
"""

import numpy as np
import numpy.ma as np_ma
import pytest
import sympy as sy
import math

import ifa_smeargle.core as core
import ifa_smeargle.masking as mask
import ifa_smeargle.testing as test

def test_ifas_large_integer_array_product():
    """ This tests the multiplication of large integers."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5),index=13)

    # The products of the multiplication.
    _pd, _pdln, _pdl10 = core.math.ifas_large_integer_array_product(
        integer_array=test_array)
    product, product_nat_log, product_log10 = (_pd, _pdln, _pdl10)
    
    # Checking the values against results from Wolfram|Alpha. 
    # Sparrow thinks Wolfram|Alpha is a "correct" enough source.
    # See https://cutt.ly/ZuccSbe for Wolfram|Alpha computation.
    CHECK_PROD_STRING = '18952004028289913475831259188568511277704891202961'
    CHECK_NUMBER = sy.Integer(CHECK_PROD_STRING)
    # See https://cutt.ly/quccGdx for Wolfram|Alpha computation.
    CHECK_NLOG_STRING = '113.4659941431228872468758215004232622784893568421'
    CHECK_NLOG = sy.Float(CHECK_NLOG_STRING)
    # See https://cutt.ly/fuccHAI for Wolfram|Alpha computation.
    CHECK_B10_STRING = '49.277655140024960622131491261439997397213580891331'
    CHECK_B10LOG = sy.Float(CHECK_B10_STRING)

    # Checking the product itself.
    prod_assert_message = ("The check number is: {check}  "
                           "The product is: {prod} "
                           .format(check=CHECK_NUMBER, prod=product))
    assert math.isclose(product, CHECK_NUMBER), prod_assert_message

    # Checking the natural log of the product.
    nlog_assert_message = ("The check logarithm is: {check}  "
                           "The product natural logarithm is: {log} "
                           .format(check=CHECK_NLOG, log=product_nat_log))
    assert math.isclose(product_nat_log, CHECK_NLOG), nlog_assert_message

    # Checking the base 10 log itself.
    b10log_assert_message = ("The check logarithm is: {check}  "
                             "The product base 10 logarithm is: {log} "
                             .format(check=CHECK_B10LOG, log=product_log10))
    assert math.isclose(product_log10, CHECK_B10LOG), b10log_assert_message
    # All done.
    return None


def test_ifas_masked_mean():
    """ This tests the mean computation with masked arrays."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5))

    # Creating the mask for this array.
    column_indexes = [0,1,3,4]
    row_indexes = [1,4,2,3]
    mask_array = mask.mask_single_pixels(data_array=test_array,
                                         column_indexes=column_indexes,
                                         row_indexes=row_indexes)

    # Creating a masked array.
    masked_array = np_ma.array(test_array, mask=mask_array)

    # The mean.
    mean = core.math.ifas_masked_mean(array=masked_array)

    # Test the mean against the expected value.
    CHECK_STRING = '40.666666666666664'
    CHECK_NUMBER = sy.Float(CHECK_STRING)

    # Checking the mean itself.
    assert_message = ("The check mean value is: {check}  "
                      "The mean value is: {mean} "
                      "The array is: \n {array}"
                      .format(check=CHECK_NUMBER, mean=mean,
                              array=masked_array))
    assert math.isclose(mean, CHECK_NUMBER), assert_message
    # All done.
    return None

def test_ifas_masked_median():
    """ This tests the median computation with masked arrays."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5))

    # Creating the mask for this array.
    column_indexes = [0,1,3,4]
    row_indexes = [1,4,2,3]
    mask_array = mask.mask_single_pixels(data_array=test_array,
                                         column_indexes=column_indexes,
                                         row_indexes=row_indexes)

    # Creating a masked array.
    masked_array = np_ma.array(test_array, mask=mask_array)

    # The median.
    median = core.math.ifas_masked_median(array=masked_array)

    # Test the median against the expected value.
    CHECK_STRING = '37'
    CHECK_NUMBER = sy.Integer(CHECK_STRING)

    # Checking the mean itself.
    assert_message = ("The check median value is: {check}  "
                      "The median value is: {median} "
                      "The array is: \n {array}"
                      .format(check=CHECK_NUMBER, median=median,
                              array=masked_array))
    assert median == CHECK_NUMBER, assert_message
    # All done.
    return None

def test_ifas_masked_std():
    """ This tests the standard deviation computation with masked 
    arrays."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5))

    # Creating the mask for this array.
    column_indexes = [0,1,3,4]
    row_indexes = [1,4,2,3]
    mask_array = mask.mask_single_pixels(data_array=test_array,
                                         column_indexes=column_indexes,
                                         row_indexes=row_indexes)

    # Creating a masked array.
    masked_array = np_ma.array(test_array, mask=mask_array)

    # The std.
    std = core.math.ifas_masked_std(array=masked_array)

    # Test the population std against the expected value.
    CHECK_STRING = '29.08662486490562'
    CHECK_NUMBER = sy.Float(CHECK_STRING)

    # Checking the mean itself.
    assert_message = ("The check std value is: {check}  "
                      "The std value is: {std} "
                      "The array is: \n {array}"
                      .format(check=CHECK_NUMBER, std=std,
                              array=masked_array))
    assert math.isclose(std, CHECK_NUMBER), assert_message
    # All done.
    return None

def test_ifas_robust_mean():
    """ This tests the computation of means using a more robust 
    approach."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5))

    robust_mean = core.math.ifas_robust_mean(array=test_array)

    # Test the mean against the expected value.
    CHECK_STRING = '42.4'
    CHECK_NUMBER = sy.Float(CHECK_STRING)

    # Checking the mean itself.
    assert_message = ("The check mean value is: {check}  "
                      "The mean value is: {mean} "
                      "The array is: \n {array}"
                      .format(check=CHECK_NUMBER, mean=robust_mean,
                              array=test_array))
    assert math.isclose(robust_mean, CHECK_NUMBER), assert_message
    # All done.
    return None

def test_ifas_robust_std():
    """ This tests the computation of means using a more robust 
    approach."""

    # Creating the testing array of integers.
    test_array = test.base.create_prime_test_array(shape=(5,5))

    robust_std = core.math.ifas_robust_std(array=test_array)

    # Test the mean against the expected value.
    CHECK_STRING = '28.880443209895517'
    CHECK_NUMBER = sy.Float(CHECK_STRING)

    # Checking the mean itself.
    assert_message = ("The check mean value is: {check}  "
                      "The std value is: {std} "
                      "The array is: \n {array}"
                      .format(check=CHECK_NUMBER, std=robust_std,
                              array=test_array))
    assert math.isclose(robust_std, CHECK_NUMBER), assert_message
    # All done
    return None