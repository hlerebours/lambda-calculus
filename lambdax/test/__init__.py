""" Package to hold all unit-tests related to `lambdax`.
This module only contains a helper for the tests.
"""

from lambdax.lambda_calculus import is_λ


def assert_value(value, expected):
    """ Check that a value is as expected, and also that it's an abstraction because
    otherwise calling == on it would return another abstraction (which would be considered True
    by the assert.
    """
    assert not is_λ(value)
    assert value == expected
