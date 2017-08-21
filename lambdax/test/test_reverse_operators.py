from lambdax.lambda_calculus import X, is_λ
from lambdax.test import assert_value


def test_radd():
    my_lambda = 3 + X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 5)


def test_rsub():
    my_lambda = 3 - X
    assert is_λ(my_lambda)
    assert_value(my_lambda(5), -2)


def test_rmul():
    my_lambda = 3 * X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 6)


def test_rtruediv():
    my_lambda = 3 / X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 1.5)


def test_rfloordiv():
    my_lambda = 8 // X
    assert is_λ(my_lambda)
    assert_value(my_lambda(3), 2)


def test_rmod():
    my_lambda = 11 % X
    assert is_λ(my_lambda)
    assert_value(my_lambda(3), 2)


def test_rpow():
    my_lambda = 3 ** X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 9)


def test_rlshift():
    my_lambda = 3 << X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 12)


def test_rrshift():
    my_lambda = 12 >> X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 3)


def test_rand():
    my_lambda = 3 & X
    assert is_λ(my_lambda)
    assert_value(my_lambda(2), 2)


def test_ror():
    my_lambda = 3 | X
    assert is_λ(my_lambda)
    assert_value(my_lambda(6), 7)


def test_rxor():
    my_lambda = 3 ^ X
    assert is_λ(my_lambda)
    assert_value(my_lambda(6), 5)


def test_harder_with_reverse_op():
    my_lambda1 = 3 ** X + 1
    my_lambda2 = 1 + X ** 2
    my_lambda3 = 1 + 3 ** X
    assert_value(my_lambda1(2), 10)
    assert_value(my_lambda2(3), 10)
    assert_value(my_lambda3(2), 10)
