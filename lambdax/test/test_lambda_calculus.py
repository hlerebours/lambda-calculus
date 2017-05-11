""" For now, all tests related to `lambdax`. It'll be split later. """

from collections import OrderedDict
from functools import partial

from pytest import raises

import lambdax
from lambdax import λ, X, x1, x2, x3, x4, x5, comp, chaining
from lambdax import contains, and_, or_, not_, is_
from lambdax.lambda_calculus import _LambdaAbstractionBase
from lambdax.test import assert_value


def test_provided_magic_variables():
    magic_variables = [(name, value)
                       for name, value in vars(lambdax).items()
                       if name[0].lower() == 'x' and (len(name) == 1 or name[-1].isdigit())]
    assert len(magic_variables) == 20
    assert all(value._λ_index + 1 == int(name[1:] or 1)  # pylint: disable=protected-access
               for name, value in magic_variables)


def test_identity():
    identity = X
    assert isinstance(identity, _LambdaAbstractionBase)
    assert_value(identity(int), int)
    assert_value(identity(42), 42)


def test_attribute():
    # delay the read of an attribute: here, get_my_attr ~= lambda x: x.my_attr
    class Foo(object):
        test = 42

        def __init__(self):
            self.test = 51

    get_my_attr = X.test
    assert isinstance(get_my_attr, _LambdaAbstractionBase)
    assert_value(get_my_attr(Foo()), 51)
    assert_value(get_my_attr(Foo), 42)


def test_property():
    # delay the read of an property: here, get_imaginary_part ~= lambda x: x.imag
    get_imaginary_part = X.imag
    assert isinstance(get_imaginary_part, _LambdaAbstractionBase)
    assert_value(get_imaginary_part(complex(42, 51)), 51)


def test_instantiation():
    # delay the instantiation of a class: here, instantiate ~= lambda x: x()
    instantiate = X()
    assert isinstance(instantiate, _LambdaAbstractionBase)
    assert_value(instantiate(int), 0)
    assert_value(instantiate(str), "")


def test_method_no_arg():
    # delay the call to the method __neg__ with no argument
    neg = -X
    assert isinstance(neg, _LambdaAbstractionBase)
    assert_value(list(map(neg, range(4))), [0, -1, -2, -3])


def test_method_with_constant():
    # delay the application of a method taking a constant;
    # here, join ~= lambda x: x.join(['O', 'o'])
    join = X.join(λ(['O', 'o']))  # λ(..) prevents from β-reducing too soon
    assert isinstance(join, _LambdaAbstractionBase)
    assert_value(join('_'), 'O_o')


def test_method_with_variable():
    # delay the application of a method taking a variable;
    # here, join ~= lambda x, y: x.join(y)
    join = x1.join(x2)
    assert isinstance(join, _LambdaAbstractionBase)
    assert_value(join('_', ['O', 'o']), 'O_o')


def test_method_with_variable2():
    # the same as before but with variables taken in another order;
    # here, join ~= lambda x, y: y.join(x)
    join = x2.join(x1)
    assert isinstance(join, _LambdaAbstractionBase)
    assert_value(join(['O', 'o'], '_'), 'O_o')


def test_asymmetric_method():
    # delay the application of a method; here, half ~= lambda x: x // 2
    # note that 2.__floordiv__ exists; this test checks that we don't call it by mistake:
    # half(21) != 2.__floordiv__(21) (== 2 // 21 == 0)
    half = X // 2
    assert isinstance(half, _LambdaAbstractionBase)
    assert_value(half(21), 10)


def test_multiply():
    # delay the application of a usual infix operator
    my_lambda = X * 4
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(3), 12)


def test_power():
    # delay the application of another usual infix operator
    my_lambda = X ** 3
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(2), 8)


def test_getitem():
    my_lambda = X["abc"]
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda({"abc": "Foo"}), "Foo")


def test_getslice():
    # it's just a particular case of `getitem`, really (with a "slice" as argument)
    my_lambda = X[1:3]
    assert_value(my_lambda("abcdefg"), "bc")


def test_abs():
    my_lambda = abs(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(-12), 12)
    assert_value(my_lambda(13), 13)


def test_bit_and():
    my_lambda = X & 2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(0), 0)
    assert_value(my_lambda(1), 0)
    assert_value(my_lambda(2), 2)
    assert_value(my_lambda(3), 2)
    assert_value(my_lambda(4), 0)
    assert_value(my_lambda(6), 2)


def test_bit_shift():
    my_lambda = X << 2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(0), 0)
    assert_value(my_lambda(1), 4)
    assert_value(my_lambda(3), 12)


def test_bit_flip():
    my_lambda = ~X
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(0), -1)
    assert_value(my_lambda(1), -2)
    assert_value(my_lambda(3), -4)


def test_eq():
    my_lambda = X + 3 == 7
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda(4) is True
    assert my_lambda(-4) is False
    assert my_lambda(True) is False


def test_lt():
    my_lambda = X < 42
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda(-10) is True
    assert my_lambda(42) is False
    assert my_lambda(51) is False


def test_ge():
    my_lambda = X >= 10
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda(12) is True
    assert my_lambda(10) is True
    assert my_lambda(-50) is False


def test_len():
    my_lambda1 = X.__len__()  # either you directly call the operator
    my_lambda2 = λ(len)(X)  # or you wrap the built-in function to make it an abstraction
    assert isinstance(my_lambda1, _LambdaAbstractionBase)
    assert isinstance(my_lambda2, _LambdaAbstractionBase)
    assert_value(my_lambda1("abc"), 3)
    assert_value(my_lambda2("24-character-long-string"), 24)


def test_bool():
    my_lambda = λ(bool)(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)

    # actually calls `__bool__`
    assert my_lambda(0) is False
    assert my_lambda(4) is True

    # actually calls `__len__`
    assert my_lambda("") is False
    assert my_lambda("string") is True
    assert my_lambda([]) is False
    assert my_lambda([0]) is True


def test_getattr():
    get_imag = λ(getattr)(X, 'imag')
    assert isinstance(get_imag, _LambdaAbstractionBase)
    assert_value(get_imag(complex(14, 42)), 42)
    with raises(AttributeError):
        get_imag('foo')

    get_attr = λ(getattr)(42, X)
    assert isinstance(get_attr, _LambdaAbstractionBase)
    assert_value(get_attr('__str__')(), '42')
    with raises(AttributeError):
        get_attr('foo')

    my_getattr = λ(getattr)(x1, x2)
    assert isinstance(my_getattr, _LambdaAbstractionBase)
    assert_value(my_getattr(14, '__str__')(), '14')
    with raises(AttributeError):
        my_getattr(14, 'foo')

    my_getattr_with_default = λ(getattr)(x1, x2, x3)
    assert isinstance(my_getattr_with_default, _LambdaAbstractionBase)
    assert_value(my_getattr_with_default(15, '__str__', int)(), '15')
    assert_value(my_getattr_with_default(16, 'foo', int)(), 0)
    assert_value(my_getattr_with_default(17, 'foo', 1.4), 1.4)


def test_contains():
    contains_1 = X.__contains__(1)  # either you directly call the operator
    contains_2 = contains(X, 2)  # or you call the function provided by `lambdax` for "convenience"
    is_in_1_2_3 = contains([1, 2, 3], X)
    assert isinstance(contains_1, _LambdaAbstractionBase)
    assert isinstance(contains_2, _LambdaAbstractionBase)

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
    assert isinstance(is_false, _LambdaAbstractionBase)
    assert is_false(False) is True
    assert is_false(True) is False
    assert is_false(0) is False
    assert is_false(1) is False
    assert not_(X)(0) is True


def test_logic_and():
    my_lambda = and_(X, 4)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(0), 0)
    assert_value(my_lambda(1), 4)
    assert_value(my_lambda(-3), 4)
    assert_value(my_lambda(""), "")
    assert_value(my_lambda("abc"), 4)
    assert_value(my_lambda([]), [])
    assert_value(my_lambda([0]), 4)


def test_logic_or():
    my_lambda = or_(X, 4)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(0), 4)
    assert_value(my_lambda(1), 1)
    assert_value(my_lambda(-3), -3)
    assert_value(my_lambda(""), 4)
    assert_value(my_lambda("abc"), "abc")
    assert_value(my_lambda([]), 4)
    assert_value(my_lambda([0]), [0])


def test_logic_not():
    my_lambda = not_(X)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert my_lambda(0) is True
    assert my_lambda(1) is False
    assert my_lambda(-3) is False
    assert my_lambda("") is True
    assert my_lambda("abc") is False
    assert my_lambda([]) is True
    assert my_lambda([0]) is False


def test_hard_use_case():
    my_lambda = λ(len)(X["abc"][5:])
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda({"abc": "24-character-long-string"}), 24 - 5)


def test_setattr_forbidden():
    my_var = X
    with raises(AttributeError):
        my_var.my_attr = 42

    my_const = λ(3)
    with raises(AttributeError):
        my_const.toto = 42

    my_expr = my_var * my_const
    with raises(AttributeError):
        my_expr.toto = 42
    assert_value(my_expr(4), 12)  # it still works :)


def test_two_variables():
    my_lambda = x1 + x2
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(1, 5), 6)


def test_two_variables_harder():
    my_lambda = (x1 + 4) * x2 + 7
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(3, 5), 42)


def test_with_named_param():
    class Class:
        @staticmethod
        def meth(arg, named=42):
            return arg, named

    my_lambda = x1.meth(x2)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(Class(), 1), (1, 42))

    my_lambda = x1.meth(arg=x2)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(Class(), 2), (2, 42))

    my_lambda = x1.meth(3, x2)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(Class(), 51), (3, 51))

    my_lambda = x1.meth(4, named=x2)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(Class(), 52), (4, 52))


def test_many_variables():
    my_lambda = x1 ** 5 + x2 ** 4 + x3 ** 3 + x4 ** 2 + x5
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(1, 2, 3, 4, 5), 1 + 2 ** 4 + 3 ** 3 + 4 ** 2 + 5)


def test_multiple_var_usage():
    my_lambda = x1 ** 2 + x2 + x1 * 4
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(3, 7), 28)
    my_lambda += x2 ** 3  # it really is the same `x2` than before
    assert_value(my_lambda(-2, 3), 26)


def test_wrong_var_choices():
    def test_expr(expr_2args, missing_x):
        try:
            expr_2args(1, 2)
            assert False
        except TypeError as exc:
            assert "Missing x%d" % missing_x in str(exc)

    test_expr(x2 ** 2 + x3, missing_x=1)
    test_expr(x3 ** 2 + x1, missing_x=2)


def test_distributivity():
    add6 = X + 3 * 2
    mul2_add3 = X * 2 + 3
    assert isinstance(add6, _LambdaAbstractionBase)
    assert isinstance(mul2_add3, _LambdaAbstractionBase)
    assert_value(add6(7), 13)
    assert_value(mul2_add3(7), 17)


def test_associativity():
    by_syntax = (X + 3) * 2
    by_definition = X + 3
    by_definition *= 2
    assert isinstance(by_syntax, _LambdaAbstractionBase)
    assert isinstance(by_definition, _LambdaAbstractionBase)
    assert_value(by_syntax(7), 20)
    assert_value(by_definition(7), 20)


def test_augment_abstraction():
    add3 = X + 3
    add7 = add3 + 4
    assert isinstance(add3, _LambdaAbstractionBase)
    assert isinstance(add7, _LambdaAbstractionBase)
    assert_value(add3(10), 13)
    assert_value(add7(10), 17)
    assert_value(add3(20), 23)
    assert_value(add7(20), 27)
    add3 *= 2
    assert_value(add3(30), 66)  # damn!
    assert_value(add7(30), 37)  # that one remains unchanged


def test_composition():
    mul3 = X * 3
    add7 = X + 7
    mul3_add7 = comp(add7, mul3)
    assert isinstance(mul3_add7, _LambdaAbstractionBase)
    assert_value(mul3_add7(2), 13)
    add7_mul3 = chaining(add7, mul3)
    assert isinstance(add7_mul3, _LambdaAbstractionBase)
    assert_value(add7_mul3(2), 27)


def test_compose_with_non_abstraction():
    # this makes sense
    suffixed_length = comp(len, X + "def")
    assert isinstance(suffixed_length, _LambdaAbstractionBase)
    assert_value(suffixed_length("abc"), 6)

    # that doesn't make sense
    with raises(ValueError):
        comp(X + "def", "abc")


def test_compose_different_card():
    two_var = x1 * 3 + x2 * 7
    one_var = X * 2
    composed = comp(one_var, two_var)
    assert isinstance(composed, _LambdaAbstractionBase)
    assert_value(composed(2, 4), (2 * 3 + 4 * 7) * 2)

    composed = comp(two_var, one_var)
    assert isinstance(composed, _LambdaAbstractionBase)

    # it makes no sense to have "g ∘ f" where `g` doesn't take exactly one
    # parameter (the return value of `f`)
    with raises(TypeError):
        composed(2, 4)
    with raises(TypeError):
        composed(3)

    # ... except if the return of `f` has the same arity as `g`
    assert_value(composed((1,)), two_var(1, 1))


def test_tricky_compose():
    times1 = X
    times2 = X * 2
    times3 = X * 3
    multiply_all = λ(map)(X, range(5))
    res = list(map(partial(comp, multiply_all), (times1, times2, times3)))
    assert_value(res, [
        [1, 2, 3, 4, 5],
        [2, 4, 6, 8, 10],
        [3, 6, 9, 12, 15]
    ])


def test_mixing_is_not_composing():
    # /!\ please don't mix expressions... particularly when it looks like a composition
    lambda_a = X
    lambda_b = X.__add__
    my_lambda = lambda_b(lambda_a)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert_value(my_lambda(3), 6)

    # this is possible, but dangerous because of the shared X
    lambda_a = X ** 2
    lambda_b = X + 1
    lambda_c = lambda_a - lambda_b
    assert isinstance(lambda_c, _LambdaAbstractionBase)
    assert_value(lambda_c(1), -1)
    assert_value(lambda_c(-1), 1)
    assert_value(lambda_c(0), -1)


def test_reduction_too_many_args():
    my_lambda = x1 + x2
    with raises(TypeError):
        my_lambda(1, 2, 3)
    with raises(TypeError):
        # the optimization at first reduction doesn't impact that, we still get the error
        my_lambda(1, 2, 3)
    assert_value(my_lambda(1, 2), 3)
    add3 = my_lambda + 3
    assert isinstance(add3, _LambdaAbstractionBase)
    assert_value(add3(1, 8), 12)
    with raises(TypeError):
        my_lambda(1, 2, 3)
    with raises(TypeError):
        add3(1, 2, 3)

    part = partial(my_lambda, 3)
    assert_value(part(10), 13)
    assert_value(my_lambda(3, 4), 7)
    with raises(TypeError):
        # we also get the error on a partially applied abstraction
        part(1, 2)
    assert_value(part(5), 8)

    # these however are explicitly not reductions:
    other = x1 + x2
    assert isinstance(other(1, foo=42), _LambdaAbstractionBase)
    assert isinstance(other(1, 2, foo=42), _LambdaAbstractionBase)
    assert isinstance(other(1, 2, 3, foo=42), _LambdaAbstractionBase)


def test_reduction_fast_path():
    # assert that two calls to reduce an abstraction don't do twice the same checks
    my_lambda = x1 + x2
    other_lambda = my_lambda + 42
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert isinstance(other_lambda, _LambdaAbstractionBase)

    my_lambda(1, b=2)
    my_lambda(c=4)
    my_lambda(1, 2)  # this is a reduction, following calls will not call the same prototype
    with raises(TypeError):
        my_lambda(1, b=2)
    with raises(TypeError):
        my_lambda(c=4)

    part = partial(my_lambda, 42)
    assert_value(part(3), 45)
    with raises(TypeError):
        part(4, a=1)
    with raises(TypeError):
        part(a=1)

    assert_value(my_lambda(40, 10), 50)
    assert_value(part(5), 47)


def test_identity_not_optimized():
    my_var = X
    assert isinstance(my_var, _LambdaAbstractionBase)
    assert_value(my_var(3), 3)
    # we can still define the abstraction after having reduced it
    # in this particular case of an only magic variable as expression,
    # because those variables must be reusable!
    assert isinstance(my_var(4, a=3), _LambdaAbstractionBase)
    assert_value(my_var(2), 2)


def test_partial():
    my_lambda = x1 ** 5 + x2 ** 4 + x3 ** 3 + x4 ** 2 + x5
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    after3 = partial(my_lambda, 3)
    assert isinstance(my_lambda, _LambdaAbstractionBase)
    assert not isinstance(after3, _LambdaAbstractionBase)
    assert_value(my_lambda(-3, 4, -5, -6, -7), (-3) ** 5 + 4 ** 4 + (-5) ** 3 + 6 ** 2 + -7)
    assert_value(after3(4, 5, 6, 7), 3 ** 5 + 4 ** 4 + 5 ** 3 + 6 ** 2 + 7)
    assert_value(after3(-4, 5, -6, 7), 3 ** 5 + (-4) ** 4 + 5 ** 3 + (-6) ** 2 + 7)


def test_particular_abstractions():
    my_id = X
    assert isinstance(my_id, _LambdaAbstractionBase)
    assert_value(my_id(3), 3)
    with raises(TypeError):
        my_id(1, 2)
    my_apply_no_arg = my_id()
    assert isinstance(my_apply_no_arg, _LambdaAbstractionBase)
    assert_value(my_apply_no_arg(int), 0)

    # combine a variable abstraction with a constant one:
    my_expr = my_id * λ(3)
    assert isinstance(my_expr, _LambdaAbstractionBase)
    assert_value(my_expr(4), 12)


def test_expand():
    # test that we can also take an iteration of arguments to reduce the abstraction
    my_join = x1 + x2
    assert isinstance(my_join, _LambdaAbstractionBase)
    assert_value(my_join(OrderedDict([("abc", 1), ("def", 2)])), "abcdef")
    assert_value(my_join([2, 3]), 5)

    def assert_list(it, ref_list):
        chal_list = list(it)
        assert len(chal_list) == len(ref_list), "%s != %s" % (chal_list, ref_list)
        for a, b in zip(chal_list, ref_list):
            assert_value(a, b)

    # really useful to map a lambda to an iteration of arg tuples:
    assert_list(map(x1 << x2, ((i, 2) for i in range(5))), [0, 4, 8, 12, 16])
    assert_list(map(x1 * 2 + x2, ((i, 3) for i in range(5))), [3, 5, 7, 9, 11])


def test_degenerate_expand():
    # test that we cannot take an iteration of arguments to reduce a non-multivariate abstraction
    plus3 = X + 3
    assert isinstance(plus3, _LambdaAbstractionBase)
    assert_value(plus3(2), 5)
    with raises(TypeError):
        plus3([3])

    assert isinstance(λ(42)([]), _LambdaAbstractionBase)
