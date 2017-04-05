""" Implement the entire mechanism to build λ-abstractions from a
few magic tricks provided here and a lot of operator overloading.
Be reassured: while you're not using the public stuff exposed here,
no operator is overloaded and everything is working as usual.
Importing this module has no side-effect.

All functions publicly exposed by the built-in module `operator`
are redefined here to be immediately usable in lambda expressions.
"""

import abc
import itertools
import operator as op
import sys

_operators = vars(op)


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
        return {
            method_name: _generate_magic_method(op)
            for method_name, op in (
                ('__%s__' % op_name.rstrip('_'), op)
                for op_name, op in _operators.items()
                if not op_name.startswith('_')
            ) if method_name in _operators
        }


class _LambdaAbstractionBase(metaclass=_AddDunderMethods):
    _β_reducing = None

    @abc.abstractmethod
    def _β(self, *input_data):
        """ β-reduction of the λ-abstraction """

    def __call__(self, *args, **kwargs):  # pylint: disable=method-hidden
        if not self._β_reducing:
            if (args and not kwargs and
                    not any(isinstance(v, _LambdaAbstractionBase)
                            for v in itertools.chain(args, kwargs.values()))):
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

    def __init__(self, idx):
        self._λ_index = idx

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


# Provide all usual operators (defined in built-in module `operator`)
# as functions usable in a lambda.

# comparison operations
eq = λ(op.eq)
ge = λ(op.ge)
gt = λ(op.gt)
lt = λ(op.lt)
le = λ(op.le)
ne = λ(op.ne)

# logical operations
is_ = λ(op.is_)
is_not = λ(op.is_not)
not_ = λ(op.not_)
truth = λ(op.truth)

# mathematical and bitwise operations
abs = λ(op.abs)  # pylint: disable=redefined-builtin
add = λ(op.add)
floordiv = λ(op.floordiv)
index = λ(op.index)
inv = λ(op.inv)
invert = λ(op.invert)
lshift = λ(op.lshift)
mod = λ(op.mod)
mul = λ(op.mul)
if sys.version_info >= (3, 5):
    matmul = λ(op.matmul)
neg = λ(op.neg)
pos = λ(op.pos)
pow = λ(op.pow)  # pylint: disable=redefined-builtin
rshift = λ(op.rshift)
sub = λ(op.sub)
truediv = λ(op.truediv)

# sequence operations
concat = λ(op.concat)
contains = λ(op.contains)
countOf = λ(op.countOf)
delitem = λ(op.delitem)
getitem = λ(op.getitem)
indexOf = λ(op.indexOf)
setitem = λ(op.setitem)
if sys.version_info >= (3, 4):
    length_hint = λ(op.length_hint)

# in-place operations
iadd = λ(op.iadd)
iand = λ(op.iand)
iconcat = λ(op.iconcat)
ifloordiv = λ(op.ifloordiv)
ilshift = λ(op.ilshift)
imod = λ(op.imod)
imul = λ(op.imul)
if sys.version_info >= (3, 5):
    imatmul = λ(op.imatmul)
ior = λ(op.ior)
ipow = λ(op.ipow)
irshift = λ(op.irshift)
isub = λ(op.isub)
itruediv = λ(op.itruediv)
ixor = λ(op.ixor)


# In the list above are missing (in comparison with the module `operator`)
# the bitwise functions `and`, `or_` and `xor`. To be consistent with the
# provided functions `not_`, `is_` and `is_not`, which are functions equivalent
# to the keyword operators `not`, `is` and `is not` (FYI, the keyword `in` is
# provided as function with `contains`), we implement the keyword operators
# `and` and `or` as functions below. To avoid confusion between logical and
# bitwise operations, we don't provide a function `xor` at all.
# For the bitwise operations, use the notation `a & b`, `a | b`, `a ^ b`.

def and_(a, b):
    """ Logical `and` (like the keyword) as a function. """
    return _LambdaAbstraction(a, lambda a_: a_ and b, (), {})


def or_(a, b):
    """ Logical `or` (like the keyword) as a function. """
    return _LambdaAbstraction(a, lambda a_: a_ or b, (), {})
