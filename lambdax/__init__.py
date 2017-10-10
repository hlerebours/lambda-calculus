""" Package that provides a way to easily write lambda expressions.

Many built-in functions and operators are rewritten as such themselves
to ease the writing of custom lambda expressions.

Also the magic variables (x1, x2, ...) are exposed here, as well as
the function `λ` to convert anything to a lambda expression and the
function `comp` to compose lambdas.

The keyword operators have their lambda equivalent too:
- a if x else b -> if_(x, a, b)  # lazily evaluated
- a and b       -> and_(a, b)    # lazily evaluated
- a or b        -> or_(a, b)     # lazily evaluated
- a is b        -> is_(a, b)
- a is not b    -> is_not(a, b)
- a not b       -> not_(a, b)
- a in b        -> contains(b, a) (caution: operands are inverted)
- del a[b]      -> delitem(a, b)
"""

import setup
from lambdax.lambda_calculus import *
from lambdax.operators import *
from lambdax.builtins_as_lambdas import *

__version__ = setup.VERSION
