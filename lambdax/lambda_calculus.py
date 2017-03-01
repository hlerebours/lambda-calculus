""" Express a few lambdas in a more handy and readable way, thanks to a magic variable X (or x).

Examples:
square = X ** 2
get_42nd = X[42]

To apply a λ-abstraction (i.e. do a β-reduction), you either call the special β method on it,
or use the λX (or λx) function to do it for you, just for style...
assert square.β(3) == 9
assert λx(square)(3) == 9
assert get_42nd.β({42: "the answer"}) == "the answer"

and... here's the fun! and a typical use case:
assert list(map(λx(-x * 3), range(4))) == [0, -3, -6, -9]
"""

import operator
from abc import abstractmethod

# "Redefinition" of built-in operators if needed

original_len = len
original_bool = bool
original_getattr = getattr
_sentinel = object()


def len(collection):  # pylint: disable=redefined-builtin
    """ Built-in function `len` checks that the value returned by the call to the method __len__
    is an `int` and it only keeps the actual integral value, not the whole instance of a possible
    sub-class of `int`.
    """
    return (
        collection.__len__()
        if isinstance(collection, _LambdaAbstractionBase) else
        original_len(collection)
    )


def bool(truth):  # pylint: disable=redefined-builtin
    """ Built-in `bool` class, used as a function, calls __bool__ if present or falls back
    on __len__ if present... so we don't know yet what method to call (before the β-reduction).
    """
    return (
        _LambdaAbstraction(truth, original_bool, (), {})
        if isinstance(truth, _LambdaAbstractionBase) else
        original_bool(truth)
    )


def getattr(instance, name, default=_sentinel):  # pylint: disable=redefined-builtin
    """ Built-in `getattr` function checks that `name` is a string. """
    args = (name,) if default is _sentinel else (name, default)
    return (
        _LambdaAbstraction(instance, original_getattr, args, {})
        if isinstance(instance, _LambdaAbstractionBase) else
        original_getattr(instance, *args)
    )


def in_(item, collection):
    """ Keyword `in` needs the method __contains__ to return a `bool`,
    which cannot be sub-classed.
    """
    return collection.__contains__(item)


def and_(a, b):
    """ Logical `and` (like the keyword) as a function. """
    return _LambdaAbstraction(a, lambda a_: a_ and b, (), {})


def or_(a, b):
    """ Logical `or` (like the keyword) as a function. """
    return _LambdaAbstraction(a, lambda a_: a_ or b, (), {})


def not_(truth):
    """ Logical `not` (like the keyword) as a function. """
    return _LambdaAbstraction(truth, lambda t: not t, (), {})

# / Redefinition


def _apply(fun, *args, **kwargs):
    return fun(*args, **kwargs)


def _generate_magic_method(operation):
    def magic(self, *args, **kwargs):
        """ Used to convert an operator function to a "dunder"-method bound
        to _LambdaAbstractionBase
        """
        return _LambdaAbstraction(self, operation, args, kwargs)

    return magic


class _AddDunderMethods(type):
    @classmethod
    def __prepare__(mcs, _name, _bases):
        # add operators declared in `operator` standard module (e.g. __add__, __mul__, ...)
        _operator_methods = vars(operator)
        return {
            method_name: _generate_magic_method(op)
            for method_name, op in (
                ('__%s__' % op_name.rstrip('_'), op)
                for op_name, op in _operator_methods.items()
                if not op_name.startswith('_')
            ) if method_name in _operator_methods
        }


class _LambdaAbstractionBase(metaclass=_AddDunderMethods):
    _β_reducing = None

    @abstractmethod
    def β(self, input_data):
        """ β-reduction of the λ-abstraction """

    __call__ = _generate_magic_method(_apply)
    __getattr__ = _generate_magic_method(getattr)
    __getitem__ = None  # this is just to silence pylint when we do X[42]

    def __setattr__(self, name, value):
        if name[:3] not in ('_λ_', '_β_'):
            raise AttributeError("You cannot set an attribute on a λ-abstraction,"
                                 " the expression is purely functional.")
        super().__setattr__(name, value)


class _LambdaAbstraction(_LambdaAbstractionBase):
    def __init__(self, origin, operation, args, kwargs):
        assert isinstance(origin, _LambdaAbstractionBase)
        self._λ_origin = origin
        self._λ_operation = operation
        self._λ_args = args
        self._λ_kwargs = kwargs

    def β(self, input_data):
        return self._λ_operation(self._λ_origin.β(input_data), *self._λ_args, **self._λ_kwargs)


class _IdentityAbstraction(_LambdaAbstractionBase):
    def β(self, input_data):
        return input_data


X = x = _IdentityAbstraction()


def λX(lambda_abstraction):
    """ Just to be pretty...
    :type lambda_abstraction: _LambdaAbstractionBase
    """
    return lambda_abstraction.β


λx = λX
