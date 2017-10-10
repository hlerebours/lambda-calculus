""" Trivial benchmark to roughly measure the performance gap between the usual pythonic lambdas
and the ones built with this package, to be fully aware of what we lose in the process.
The goal of this package is not to provide an efficient replacement to lambdas though,
but just a more concise way of writing them.
"""

from time import time

from lambdax import x
from lambdax.builtins_overridden import abs as λabs, list as λlist

iterations = range(100000)

begin_test = time()
# here `λlist` behaves like built-in `list`, whereas `λabs` returns an abstraction
test_result = λlist(map(λabs(-x ** 3 + 7), iterations))
end_test = time()

begin_ref = time()
ref_result = list(map(lambda y: abs(-y ** 3 + 7), iterations))
end_ref = time()

assert test_result == ref_result
ref_duration = end_ref - begin_ref
test_duration = end_test - begin_test
print("Reference is %.3fs" % ref_duration)
print("Test computed in: %.3fs (x%d)" % (test_duration, test_duration / ref_duration))
