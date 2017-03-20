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
Use the variable ``x`` defined in the module ``lambdax`` as parameter in your lambda, e.g.:

    .. code-block:: python

        from lambdax import x
        get_42nd = x[42]
        square = x ** 2

Note: you can also import and use ``X`` (upper-case alias) to avoid name conflicts,
if you already use the identifier ``x`` in your code.


Application
^^^^^^^^^^^
To apply your lambda (or *β-reduce* your *λ-abstraction*), call the method ``β`` on it with one argument:
the substitution for``x``.

You can also wrap the lambda in the function ``λx``, if you prefer:

    .. code-block:: python

        from lambdax import λx
        assert get_42nd.β({42: "the answer"}) == "the answer"  # one parameter to replace the only x
        assert λx(square)(3) == 9  # other (equivalent) way of reducing the lambda


Limitations
^^^^^^^^^^^
An expression must start with a "magic variable", or with one of the functions provided by ``lambdax``.


Particular cases
^^^^^^^^^^^^^^^^
The package overrides a few built-in functions *if needed*, without changing their behavior outside of the context
of a lambda expression. Take a look at the provided overridden functions, here is just an example:

.. code-block:: python

    from lambdax import len  # pylint: disable=W0622
    assert (len(x) ** 2).β("abc") == 9


Typical use case
^^^^^^^^^^^^^^^^
In practice, you will use this package to write expressions like:

.. code-block:: python

    assert list(map(λx(-x * 3), range(4))) == [0, -3, -6, -9]


Benchmark
^^^^^^^^^
Don't use this if you need performance, as it will give you lambdas that are more than ten times slower
than the classic ones (using the keyword ``lambda``). Run ``python -m lambdax.test.benchmark`` to see it
by yourself.
