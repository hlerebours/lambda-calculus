""" For now, all tests related to `lambdax`. It'll be split later. """

from pytest import raises

from lambdax import X
from lambdax import in_, and_, or_, not_
from lambdax import len, bool, getattr  # pylint: disable=redefined-builtin
from lambdax.lambda_calculus import _LambdaAbstractionBase


def test_identity():
    my_lambda = X
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    identity = my_lambda.β
    assert identity(int) == int
    assert identity(42) == 42


def test_attribute():
    # delay the read of an attribute: here, get_my_attr ~= lambda x: x.my_attr
    class Foo(object):
        my_attr = 42

        def __init__(self):
            self.my_attr = 51

    my_lambda = X.my_attr
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    get_my_attr = my_lambda.β
    assert get_my_attr(Foo()) == 51
    assert get_my_attr(Foo) == 42


def test_property():
    # delay the read of an property: here, get_imaginary_part ~= lambda x: x.imag
    my_lambda = X.imag
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    get_imaginary_part = my_lambda.β
    assert get_imaginary_part(complex(42, 51)) == 51


def test_instantiation():
    # delay the instantiation of a class: here, instantiate ~= lambda x: x()
    my_lambda = X()
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    instantiate = my_lambda.β
    assert instantiate(int) == 0
    assert instantiate(str) == ""


def test_method_no_arg():
    # delay the call to the method __neg__ with no argument
    my_lambda = -X
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    neg = my_lambda.β
    assert list(map(neg, range(4))) == [0, -1, -2, -3]


def test_method():
    # delay the application of a method; here, join ~= lambda x: x.join(['O', 'o'])
    # note that list.join doesn't exist (see next example for an operator that also
    # means sth on the argument)
    my_lambda = X.join(['O', 'o'])
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    join = my_lambda.β
    assert join('_') == 'O_o'


def test_asymmetric_method():
    # delay the application of a method; here, half ~= lambda x: x // 2
    # note that 2.__floordiv__ exists; this test checks that we don't call it by mistake:
    # half(21) != 2.__floordiv__(21) (== 2 // 21 == 0)
    my_lambda = X // 2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    half = my_lambda.β
    assert half(21) == 10


def test_multiply():
    # delay the application of a usual infix operator
    my_lambda = X * 4
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(3) == 12


def test_power():
    # delay the application of another usual infix operator
    my_lambda = X ** 3
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(2) == 8


def test_getitem():
    my_lambda = X["abc"]
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β({"abc": "Foo"}) == "Foo"


def test_getslice():
    # it's just a particular case of `getitem`, really (with a "slice" as argument)
    my_lambda = X[1:3]
    assert my_lambda.β("abcdefg") == "bc"


def test_abs():
    my_lambda = abs(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(-12) == 12
    assert my_lambda.β(13) == 13


def test_bit_and():
    my_lambda = X & 2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) == 0
    assert my_lambda.β(1) == 0
    assert my_lambda.β(2) == 2
    assert my_lambda.β(3) == 2
    assert my_lambda.β(4) == 0
    assert my_lambda.β(6) == 2


def test_bit_shift():
    my_lambda = X << 2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) == 0
    assert my_lambda.β(1) == 4
    assert my_lambda.β(3) == 12


def test_bit_flip():
    my_lambda = ~X
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) == -1
    assert my_lambda.β(1) == -2
    assert my_lambda.β(3) == -4


def test_lt():
    my_lambda = X < 42
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(-10) is True
    assert my_lambda.β(42) is False
    assert my_lambda.β(51) is False


def test_ge():
    my_lambda = X >= 10
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(12) is True
    assert my_lambda.β(10) is True
    assert my_lambda.β(-50) is False


# Particular cases using built-in "operators"

def test_len():
    assert len([]) == 0
    assert len("abc") == 3

    my_lambda1 = X.__len__()  # either you directly call the operator
    my_lambda2 = len(X)  # or you call the function provided by `lambdax` for "convenience"
    assert isinstance(my_lambda1, _LambdaAbstractionBase)
    assert isinstance(my_lambda2, _LambdaAbstractionBase)
    assert my_lambda1.β("abc") == 3
    assert my_lambda2.β("24-character-long-string") == 24


def test_bool():
    assert bool(1) is True
    assert bool(0) is False

    my_lambda = bool(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)

    # actually calls `__bool__`
    assert my_lambda.β(0) is False
    assert my_lambda.β(4) is True

    # actually calls `__len__`
    assert my_lambda.β("") is False
    assert my_lambda.β("string") is True
    assert my_lambda.β([]) is False
    assert my_lambda.β([0]) is True


def test_getattr():
    assert getattr(42, '__str__')() == '42'
    assert getattr(43, '__str__', int)() == '43'
    assert getattr(44, 'foo', int)() == 0
    assert getattr(45, 'foo', 4.2) == 4.2
    with raises(AttributeError):
        getattr(14, 'foo')

    get_imag = getattr(X, 'imag')
    assert isinstance(get_imag, _LambdaAbstractionBase)
    assert get_imag.β(complex(14, 42)) == 42
    with raises(AttributeError):
        get_imag.β('foo')


def test_in():
    my_lambda1 = X.__contains__(1)  # either you directly call the operator
    my_lambda2 = in_(1, X)  # or you call the function provided by `lambdax` for "convenience"
    assert isinstance(my_lambda1, _LambdaAbstractionBase)
    assert isinstance(my_lambda2, _LambdaAbstractionBase)

    assert my_lambda1.β((0, 1, 2)) is True
    assert my_lambda1.β(range(3)) is True
    assert my_lambda1.β((5, 6)) is False
    assert my_lambda1.β(range(4, 7)) is False

    assert my_lambda2.β((1, 4)) is True
    assert my_lambda2.β(range(4, 7)) is False

    with raises(TypeError):
        my_lambda1.β("012")
    with raises(TypeError):
        my_lambda2.β("012")


def test_not_in():
    # poor example for the "not in" operator
    my_lambda = not_(in_(1, X))
    assert isinstance(my_lambda, _LambdaAbstractionBase)

    assert my_lambda.β((0, 4, 2)) is True
    assert my_lambda.β(range(3)) is False


def test_logic_and():
    my_lambda = and_(X, 4)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) == 0
    assert my_lambda.β(1) == 4
    assert my_lambda.β(-3) == 4
    assert my_lambda.β("") == ""
    assert my_lambda.β("abc") == 4
    assert my_lambda.β([]) == []
    assert my_lambda.β([0]) == 4


def test_logic_or():
    my_lambda = or_(X, 4)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) == 4
    assert my_lambda.β(1) == 1
    assert my_lambda.β(-3) == -3
    assert my_lambda.β("") == 4
    assert my_lambda.β("abc") == "abc"
    assert my_lambda.β([]) == 4
    assert my_lambda.β([0]) == [0]


def test_logic_not():
    my_lambda = not_(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β(0) is True
    assert my_lambda.β(1) is False
    assert my_lambda.β(-3) is False
    assert my_lambda.β("") is True
    assert my_lambda.β("abc") is False
    assert my_lambda.β([]) is True
    assert my_lambda.β([0]) is False

# /Particular cases


def test_hard_use_case():
    my_lambda = len(X["abc"][5:])
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda.β({"abc": "24-character-long-string"}) == 24 - 5


def test_setattr_forbidden():
    my_var = X
    with raises(AttributeError):
        my_var.my_attr = 42
