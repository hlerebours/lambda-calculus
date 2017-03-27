""" Implement the entire mechanism to build λ-abstractions from a
few magic tricks provided here and a lot of operator overloading.
Be reassured: while you're not using the public stuff exposed here,
no operator is overloaded and everything is working as usual.
Importing this module has no side-effect.
"""

import operator
from abc import abstractmethod
from itertools import chain

# "Redefinition" of built-in operators if needed

_original_len = len
_original_bool = bool
_original_getattr = getattr
_sentinel = object()


def len(collection):  # pylint: disable=redefined-builtin
    """ Built-in function `len` checks that the value returned by the call to the method __len__
    is an `int` and it only keeps the actual integral value, not the whole instance of a possible
    sub-class of `int`.
    """
    return (
        collection.__len__()
        if isinstance(collection, _LambdaAbstractionBase) else
        _original_len(collection)
    )


def bool(truth):  # pylint: disable=redefined-builtin
    """ Built-in `bool` class, used as a function, calls __bool__ if present or falls back
    on __len__ if present... so we don't know yet what method to call (before the β-reduction).
    """
    return (
        _LambdaAbstraction(truth, _original_bool, (), {})
        if isinstance(truth, _LambdaAbstractionBase) else
        _original_bool(truth)
    )


def getattr(instance, name, default=_sentinel):  # pylint: disable=redefined-builtin
    """ Built-in `getattr` function checks that `name` is a string. """
    args = (name,) if default is _sentinel else (name, default)
    return (
        _LambdaAbstraction(instance, _original_getattr, args, {})
        if any(isinstance(o, _LambdaAbstractionBase) for o in (instance,) + args) else
        _original_getattr(instance, *args)
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
    def _β(self, *input_data):
        """ β-reduction of the λ-abstraction """

    def __call__(self, *args, **kwargs):  # pylint: disable=method-hidden
        if not self._β_reducing:
            if (
                    args and not kwargs and
                    not any(isinstance(v, _LambdaAbstractionBase)
                            for v in chain(args, kwargs.values()))
            ):
                # For now, the only thing we now about β-reduction is that it's done by providing
                # at least one argument, no named argument and no abstraction, so here we assume
                # we are reducing.

                # Also, make all following calls be β-reductions too. The incentive is to speed up
                # vectorized operations or anytime a lambda is applied on many elements:
                # it's defined once and applied many times, so let's cache the reduction.
                if self._β_reducing is None:
                    self._β_reducing = True
            else:
                # Hence here we assume we're still defining the λ-abstraction
                return _LambdaAbstraction(self, _apply, args, kwargs)

        return self._β(*args, **kwargs)

    __getattr__ = _generate_magic_method(getattr)
    __getitem__ = None  # this is just to silence pylint when we do X[42]

    def __setattr__(self, name, value):
        if name[:3] not in ('_λ_', '_β_'):
            raise AttributeError("You cannot set an attribute on a λ-abstraction,"
                                 " the expression is purely functional.")
        super().__setattr__(name, value)


class _LambdaAbstraction(_LambdaAbstractionBase):
    def __init__(self, origin, operation, args, kwargs):
        self._λ_origin = λ(origin)
        self._λ_operation = operation
        self._λ_abstract_args = [λ(a) for a in args]
        self._λ_abstract_kwargs = {k: λ(v) for k, v in kwargs.items()}

    def _β(self, *input_data):
        return self._λ_operation(
            # pylint: disable=protected-access
            self._λ_origin._β(*input_data),
            *(a._β(*input_data) for a in self._λ_abstract_args),
            **{k: v._β(*input_data) for k, v in self._λ_abstract_kwargs.items()}
        )


class _IdentityAbstraction(_LambdaAbstractionBase):
    # this class cannot be optimized on β-reduction, because it would mutate
    # instances (x, x1, x2, etc.) shared by all expressions
    _β_reducing = False

    def __init__(self, index):
        self._λ_index = index

    def _β(self, *input_data):
        return input_data[self._λ_index]


class _ConstantAbstraction(_LambdaAbstractionBase):
    def __init__(self, constant):
        self._λ_constant = constant

    def _β(self, *input_data):
        return self._λ_constant


X1 = x1 = X = x = _IdentityAbstraction(0)
_other_vars = [_IdentityAbstraction(num - 1) for num in range(2, 10)]
x2, x3, x4, x5, x6, x7, x8, x9 = _other_vars
X2, X3, X4, X5, X6, X7, X8, X9 = _other_vars


def λ(lambda_abstraction):
    """ Force the expression to be an abstraction
    :rtype: _LambdaAbstractionBase
    """
    return (
        lambda_abstraction if isinstance(lambda_abstraction, _LambdaAbstractionBase) else
        _ConstantAbstraction(lambda_abstraction)
    )
