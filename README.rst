.. image:: https://travis-ci.org/hlerebours/lambda-calculus.svg?branch=master
    :target: https://travis-ci.org/hlerebours/lambda-calculus

.. image:: https://coveralls.io/repos/github/hlerebours/lambda-calculus/badge.svg?branch=master
    :target: https://coveralls.io/github/hlerebours/lambda-calculus?branch=master

*λx*
====
    *for simpler lambdas*

—
-

Declaration
^^^^^^^^^^^
Just write the pure expression (the body of your anonymous function) using the variables ``x1``, ``x2``, ..., ``x9``
(found in the module ``lambdax``) as parameters of your lambda, e.g.:

    .. code-block:: python

        from lambdax import x, x1, x2, x3
        paraboloid = (x1 / 3.) ** 2 + (x2 / 7.) ** 2
        get_42nd = x[42]
        golden_root = x ** 2 - x - 1

``x`` is just a predefined alias for ``x1`` to have prettier lambdas when taking a single parameter.

Note: you can also import and use ``X`` and ``X1``, ``X2``, etc. (upper-case aliases) to avoid name conflicts,
if you already use the identifier ``x`` or ``x1``, ``x2`` etc. in your code.

—
-

Application
^^^^^^^^^^^
To apply your lambda, just call it as a usual function, where all arguments are positional and *must not* be named.
First argument replaces all occurrences of ``x1`` (or ``x``) in the expression, second one replaces ``x2``, etc.
Multivariate lambdas can be reduced by providing either all arguments "separately" or an only "iterable" of arguments.

    .. code-block:: python

        from lambdax.test import assert_value
        # two arguments for two different placeholders:
        assert_value(paraboloid(10, 20), (10 / 3.) ** 2 + (20 / 7.) ** 2)
        # one parameter to replace the only x:
        assert_value(get_42nd({42: "the answer"}), "the answer")
        # one parameter to replace the two occurrences of the same x:
        assert_value(golden_root(1.618), 1.618 ** 2 - 1.618 - 1)
        # the first parameter goes to every x1, the second one for x2, the third one for x3:
        assert_value((x2 * x1 + x1 * x3)(.1, .2, .3), .2 * .1 + .1 * .3)
        # all arguments are provided in one tuple:
        assert_value((x1 + x2 * x3)([2, 3, 5]), 2 + 3 * 5)

—
-

Limitations
^^^^^^^^^^^
The first identifier in the expression must be one of the public members of the module ``lambdax``,
i.e. a magic variable, a provided operator-as-function or the special function ``λ`` (see below).

—
-

Particular cases
^^^^^^^^^^^^^^^^
1. If there is a call with parameter(s) inside your expression, at least one of the parameters
   must be named or be an abstraction to distinguish your declaration from a *β-reduction*.
   You can apply ``λ`` on an argument if none of them already is a *λ-abstraction*. Examples:

   .. code-block:: python

       from lambdax import λ
       assert_value(x1(2), 2)  # calling x1 with 2 as argument applies the identity function to 2
       apply_is_back = x1(x2)  # the call is clearly part of the abstraction
       on_4dot2 = x(λ(4.2))  # it's explicitly an abstraction thanks to `λ`
       imaginary_4_as = x(imag=4)  # it's an abstraction because there is a named parameter in the call
       just_call = x()  # it's an abstraction because there is no parameter provided to the call

   If you were wondering, the lambdas defined above can be used like that:

   .. code-block:: python

       assert_value(apply_is_back(len, "abc"), 3)
       assert_value(on_4dot2(int), 4)
       assert_value(imaginary_4_as(complex), complex(0, 4))
       assert_value(just_call(str), '')

2. As well as writing arguments as explicit abstractions, if your expression can't begin with a "magic thing" coming from
   ``lambdax``, you can still wrap it with the function ``λ`` to make it an explicit abstraction. Examples:

   .. code-block:: python

       def already_existing_function(a, exp=1):
           """ Standard function """
           return a ** exp - 1
       # the lambda below takes one parameter, calls a function with two parameters
       # and modifies the result:
       my_lambda = (λ(already_existing_function)(x, exp=x) - 5) * 2
       assert_value(my_lambda(3), 42)

3. The package re-implements the common "operator" functions provided by the built-in module ``operator``
   to be directly usable in a lambda expression.

   Caution: the functions ``and_`` and ``or_`` are functional equivalents for keywords
   ``and`` and ``or``, not for bitwise operators ``&`` and ``|`` despite what has been done
   in the built-in module ``operator``. The goal here is to be consistent with the provided
   functions ``not_``, ``is_`` and ``is_not``, which match the keyword operators ``not``, ``is``
   and ``is not``. Plus there is no need for bitwise operators as functions, since they are all
   supported as double-underscore-methods in ``lambdax``.

   .. code-block:: python

       from lambdax import contains, and_
       assert contains([1, 2, 3], x)(2) is True
       assert contains(x, 4)([1, 2]) is False
       assert_value(and_(x, 6)(3), 6)
       assert_value((x & 6)(3), 2)

—
-

Composition
^^^^^^^^^^^
You can compose *λ-abstractions* by explicitly calling one of the functions ``comp``, ``circle`` or ``chaining``:
"*g* ∘ *f*" in mathematics is written in this context as ``comp(g, f)``, ``circle(g, f)`` or ``chaining(f, g)``
(mind the order of parameters).
Caution:
- g(f) is never a composition of ``f`` and ``g``
- if both `f` and `g` use the same variable X, they will share the same input in ``g(f)``. Just don't do that...

—
-

Typical use case: the ``map()`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    values = list(map((-x * 3) % 8, range(5)))
    assert all(isinstance(v, int) for v in values)
    assert values == [0, 5, 2, 7, 4]

    assert list(map(x2 ** x1, enumerate([-1, 1] * 3))) == [1] * 6
    # [(-1) ** 0, 1 ** 1, (-1) ** 2, ...]

—
-

Benchmark
^^^^^^^^^
Don't use this if you need performance, as it will give you lambdas that are about 20x slower
than the classic ones (using the keyword ``lambda``)! Run ``python -m lambdax.test.benchmark``
to see it by yourself.
