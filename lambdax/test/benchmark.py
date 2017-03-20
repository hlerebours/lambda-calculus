""" Trivial benchmark to roughly measure the performance gap between the usual pythonic lambdas
and the ones built with this package, to be fully aware of what we lose in the process.
The goal of this package is not to provide an efficient replacement to lambdas though,
but just a more concise way of writing them.
"""

from time import time

import lambdax

iterations = range(100000)

begin_test = time()
res_test = list(map(-lambdax.x ** 3 + 7, iterations))
end_test = time()

begin_ref = time()
res_ref = list(map(lambda x: -x ** 3 + 7, iterations))
end_ref = time()

assert res_test == res_ref
print("Computed in: %.3fs" % (end_test - begin_test))
print("Reference is %.3fs" % (end_ref - begin_ref))
