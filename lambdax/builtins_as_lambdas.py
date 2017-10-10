""" Expose most of the built-in functions and classes but suffixed with '_λ'
and to be only used in λ-abstractions.
See module `lambdax.builtins_overridden` to keep built-in names and have a mixed behavior,
working as expected both inside and outside λ-abstractions.
"""

import builtins

from lambdax.lambda_calculus import λ as _λ


# pylint: disable=redefined-builtin

abs_λ = _λ(abs)
all_λ = _λ(all)
any_λ = _λ(any)
ascii_λ = _λ(ascii)
bin_λ = _λ(bin)
callable_λ = _λ(callable)
chr_λ = _λ(chr)
delattr_λ = _λ(delattr)
dir_λ = _λ(dir)
divmod_λ = _λ(divmod)
exit_λ = _λ(exit)
quit_λ = _λ(quit)
format_λ = _λ(format)
getattr_λ = _λ(getattr)
hasattr_λ = _λ(hasattr)
hash_λ = _λ(hash)
hex_λ = _λ(hex)
id_λ = _λ(id)
isinstance_λ = _λ(isinstance)
issubclass_λ = _λ(issubclass)
iter_λ = _λ(iter)
len_λ = _λ(len)
max_λ = _λ(max)
min_λ = _λ(min)
next_λ = _λ(next)
oct_λ = _λ(oct)
ord_λ = _λ(ord)
pow_λ = _λ(pow)
print_λ = _λ(print)
repr_λ = _λ(repr)
round_λ = _λ(round)
setattr_λ = _λ(setattr)
sorted_λ = _λ(sorted)
sum_λ = _λ(sum)
vars_λ = _λ(vars)

# Classes overridden as functions: calling them for instantiation and calling their
# class-methods and static methods behave as usual when parameters are not abstractions,
# however using them as second argument in `isinstance` or `issubclass` requires to use
# the overridden versions of these functions provided by this module too.

bool_λ = _λ(bool)
complex_λ = _λ(complex)
enumerate_λ = _λ(enumerate)
filter_λ = _λ(filter)
frozenset_λ = _λ(frozenset)
list_λ = _λ(list)
map_λ = _λ(map)
memoryview_λ = _λ(memoryview)
range_λ = _λ(range)
reversed_λ = _λ(reversed)
set_λ = _λ(set)
slice_λ = _λ(slice)
str_λ = _λ(str)
tuple_λ = _λ(tuple)
type_λ = _λ(type)
zip_λ = _λ(zip)

bytearray_λ = _λ(bytearray)
bytearray_fromhex_λ = _λ(builtins.bytearray.fromhex)
bytearray_maketrans_λ = _λ(builtins.bytearray.maketrans)

bytes_λ = _λ(bytes)
bytes_fromhex_λ = _λ(builtins.bytes.fromhex)
bytes_maketrans_λ = _λ(builtins.bytes.maketrans)

dict_λ = _λ(dict)
dict_fromkeys_λ = _λ(builtins.dict.fromkeys)

float_λ = _λ(float)
float_fromhex_λ = _λ(builtins.float.fromhex)

int_λ = _λ(int)
int_from_bytes_λ = _λ(builtins.int.from_bytes)
