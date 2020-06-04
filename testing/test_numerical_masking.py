
"""
This tests the masking functions to ensure that they are 
appropriately calculating the masks as expected.
"""

import numpy as np
import numpy.ma as np_ma

import IfA_Smeargle.core as core
import IfA_Smeargle.masking as mask


def test_mask_nothing():
    """ This tests the masking of no pixels to ensure none are 
    missed."""

    # Creating the testing array.
    test_array = _create_test_array()

    # Prescribed masking parameters
    pass

    # Create the mask.
    test_mask = mask.mask_everything()
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask)


    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_NUMBER = 24133
    array_product = test_masked_array.product()

    # Finally, check.
    assert_message = ("The check number is: {check}  The product is {prod} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_NUMBER, prod=array_product,
                              array=test_masked_array))
    assert array_product == CHECK_NUMBER, assert_message
    # All done.
    return None

def test_mask_everything():
    """ This tests the masking of all pixels to ensure none are 
    missed."""

    # Creating the testing array.
    test_array = _create_test_array()

    # Prescribed masking parameters
    pass

    # Create the mask.
    test_mask = mask.mask_everything()
    # Create a masked array for both convince and testing.
    test_masked_array = np_ma.array(test_array, mask=test_mask)


    # A properly completed mask should have the same product value 
    # as this number. This is how the mask is checked.
    CHECK_NUMBER = 0
    array_product = test_masked_array.product()

    # Finally, check.
    assert_message = ("The check number is: {check}  The product is {prod} "
                      "The masked array is: \n {array}"
                      .format(check=CHECK_NUMBER, prod=array_product,
                              array=test_masked_array))
    assert array_product == CHECK_NUMBER, assert_message
    # All done.
    return None


def _create_test_array():
    """ This creates a test array for the purposes of creating 
    masks and to apply them and test them. This ensures a 
    uniform test array for all mask tests."""

    # The shape of the test array.
    test_array_shape = 10,10

    # And the numbers that create the array.
    test_array_values = core.math.generate_prime_numbers(
        index=0, count=np.sum(test_array_shape))

    # And reshape into the correct array shape.
    test_array = np.reshape(test_array_values, test_array_shape)
    # All done.
    return test_array