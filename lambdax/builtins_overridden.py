""" Expose most of the built-in functions and classes usable as functions, but override
them such that they can be used as usual but also in λ-abstractions with no boilerplate.
Though you should avoid this kind of magic and prefer explicit behaviors instead.
See module `lambdax.builtins_as_lambdas`.
"""

import builtins
from functools import wraps as _wraps
from itertools import chain as _chain

from lambdax.lambda_calculus import is_λ as _is_λ, λ as _λ


def _convert(f):
    @_wraps(f)
    def fun(*args, **kwargs):
        """ Replace the built-in function `f` """
        as_λ = builtins.any(_is_λ(a) for a in _chain(args, kwargs.values()))
        to_call = _λ(f) if as_λ else f
        return to_call(*args, **kwargs)

    return fun


# pylint: disable=redefined-builtin

abs = _convert(abs)
all = _convert(all)
any = _convert(any)
ascii = _convert(ascii)
bin = _convert(bin)
callable = _convert(callable)
chr = _convert(chr)
delattr = _convert(delattr)
dir = _convert(dir)
divmod = _convert(divmod)
exit = _convert(exit)
quit = _convert(quit)
format = _convert(format)
getattr = _convert(getattr)
hasattr = _convert(hasattr)
hash = _convert(hash)
hex = _convert(hex)
id = _convert(id)
isinstance = _convert(isinstance)
issubclass = _convert(issubclass)
iter = _convert(iter)
len = _convert(len)
max = _convert(max)
min = _convert(min)
next = _convert(next)
oct = _convert(oct)
ord = _convert(ord)
pow = _convert(pow)
print = _convert(print)
repr = _convert(repr)
round = _convert(round)
setattr = _convert(setattr)
sorted = _convert(sorted)
sum = _convert(sum)
vars = _convert(vars)


# Classes overridden as functions: calling them for instantiation and calling their
# class-methods and static methods behave as usual when parameters are not abstractions,
# however using them as second argument in `isinstance` or `issubclass` requires to use
# the overridden versions of these functions provided by this module too.

bool = _convert(bool)
complex = _convert(complex)
enumerate = _convert(enumerate)
filter = _convert(filter)
frozenset = _convert(frozenset)
list = _convert(list)
map = _convert(map)
memoryview = _convert(memoryview)
range = _convert(range)
reversed = _convert(reversed)
set = _convert(set)
slice = _convert(slice)
str = _convert(str)
tuple = _convert(tuple)
type = _convert(type)
zip = _convert(zip)

bytearray = _convert(bytearray)
bytearray.fromhex = _convert(builtins.bytearray.fromhex)
bytearray.maketrans = _convert(builtins.bytearray.maketrans)

bytes = _convert(bytes)
bytes.fromhex = _convert(builtins.bytes.fromhex)
bytes.maketrans = _convert(builtins.bytes.maketrans)

dict = _convert(dict)
dict.fromkeys = _convert(builtins.dict.fromkeys)

float = _convert(float)
float.fromhex = _convert(builtins.float.fromhex)

int = _convert(int)
int.from_bytes = _convert(builtins.int.from_bytes)
