
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