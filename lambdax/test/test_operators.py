from pytest import raises

from lambdax import X, is_λ, contains, not_, is_, len_λ
from lambdax.test import assert_value


def test_contains():
    contains_1 = X.__contains__(1)  # either you directly call the operator
    contains_2 = contains(X, 2)  # or you call the function provided by `lambdax` for "convenience"
    is_in_1_2_3 = contains([1, 2, 3], X)
    assert is_λ(contains_1)
    assert is_λ(contains_2)

    assert contains_1((0, 1, 2)) is True
    assert contains_1(range(3)) is True
    assert contains_1((5, 6)) is False
    assert contains_1(range(4, 7)) is False

    assert contains_2((2, 4)) is True
    assert contains_2(range(4, 7)) is False

    with raises(TypeError):
        contains_1("012")
    with raises(TypeError):
        contains_2("012")

    assert is_in_1_2_3(2) is True
    assert is_in_1_2_3(5) is False


def test_is():
    is_false = is_(X, False)
    assert is_λ(is_false)
    assert is_false(False) is True
    assert is_false(True) is False
    assert is_false(0) is False
    assert is_false(1) is False
    assert not_(X)(0) is True


def test_logic_not():
    my_lambda = not_(X)
    assert is_λ(my_lambda)
    assert my_lambda(0) is True
    assert my_lambda(1) is False
    assert my_lambda(-3) is False
    assert my_lambda("") is True
    assert my_lambda("abc") is False
    assert my_lambda([]) is True
    assert my_lambda([0]) is False


def test_len():
    my_lambda1 = X.__len__()  # either you directly call the operator
    my_lambda2 = len_λ(X)  # or you wrap the built-in function to make it an abstraction
    assert is_λ(my_lambda1)
    assert is_λ(my_lambda2)
    assert_value(my_lambda1("abc"), 3)
    assert_value(my_lambda2("24-character-long-string"), 24)
