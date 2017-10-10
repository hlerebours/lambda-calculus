""" Most of the functions publicly exposed by the module `operator`
are redefined here to be immediately usable in lambda expressions.

Compared to the built-in module, the operators that are not redefined here are:
- `abs` and `pow`, which are built-in functions, redefined
  in `lambdax.builtins_as_lambdas` and `lambdax.builtins_overridden`,
- `and_` and `or_` redefined in `lambdax.lambda_calculus` as logical operators
  and not bitwise ones (so they don't behave like the homonyms from `operator`,
- `xor` which is not provided anywhere as a function to avoid confusion.
For all the bitwise operations, call `a & b`, `a | b`, `a ^ c`.
"""

import operator as op

import sys

from lambdax.lambda_calculus import λ as _λ

# comparison operations
eq = _λ(op.eq)
ge = _λ(op.ge)
gt = _λ(op.gt)
lt = _λ(op.lt)
le = _λ(op.le)
ne = _λ(op.ne)

# logical operations
is_ = _λ(op.is_)
is_not = _λ(op.is_not)
not_ = _λ(op.not_)
truth = _λ(op.truth)

# mathematical and bitwise operations
add = _λ(op.add)
floordiv = _λ(op.floordiv)
index = _λ(op.index)
inv = _λ(op.inv)
invert = _λ(op.invert)
lshift = _λ(op.lshift)
mod = _λ(op.mod)
mul = _λ(op.mul)
if sys.version_info >= (3, 5):
    matmul = _λ(op.matmul)
neg = _λ(op.neg)
pos = _λ(op.pos)
rshift = _λ(op.rshift)
sub = _λ(op.sub)
truediv = _λ(op.truediv)

# sequence operations
concat = _λ(op.concat)
contains = _λ(op.contains)
countOf = _λ(op.countOf)
delitem = _λ(op.delitem)
getitem = _λ(op.getitem)
indexOf = _λ(op.indexOf)
setitem = _λ(op.setitem)
if sys.version_info >= (3, 4):
    length_hint = _λ(op.length_hint)

# in-place operations
iadd = _λ(op.iadd)
iand = _λ(op.iand)
iconcat = _λ(op.iconcat)
ifloordiv = _λ(op.ifloordiv)
ilshift = _λ(op.ilshift)
imod = _λ(op.imod)
imul = _λ(op.imul)
if sys.version_info >= (3, 5):
    imatmul = _λ(op.imatmul)
ior = _λ(op.ior)
ipow = _λ(op.ipow)
irshift = _λ(op.irshift)
isub = _λ(op.isub)
itruediv = _λ(op.itruediv)
ixor = _λ(op.ixor)
