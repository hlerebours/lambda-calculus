""" Check what the `lambdax` module publicly exposes. """
from inspect import isbuiltin, ismodule, isclass
import operator

import lambdax.lambda_calculus
from lambdax import x1, x2


def test_what_is_exposed():
    operators = {name for name, obj in vars(operator).items()
                 if not name.startswith('_') and not isclass(obj)}
    operators.discard('xor')

    variables = {'x'} | {'x%d' % i for i in range(1, 10)}
    variables |= {v.upper() for v in variables}

    special_functions = {'λ', 'is_λ', 'comp', 'circle', 'chaining'}

    to_expose = operators | variables | special_functions

    exposed = {name for name, obj in vars(lambdax).items()
               if not name.startswith('_') and not ismodule(obj)}

    assert to_expose == exposed


def test_builtins_are_overridden():
    for obj in vars(lambdax).values():
        assert not isbuiltin(obj)


def test_operators_implementations():
    operators = vars(operator)
    tested = set()
    untested = set()
    for name, abstraction in vars(lambdax).items():
        initial = operators.get(name)
        if initial and isbuiltin(initial):
            wrapped = getattr(abstraction, '_λ_constant', None)
            if wrapped:
                tested.add(name)
                assert wrapped == initial
                try:
                    ref = initial(42, 51)
                except TypeError as e:
                    ref = e.args
                try:
                    res = abstraction(x1, x2)(42, 51)
                except TypeError as e:
                    res = e.args
                assert res == ref
            else:
                untested.add(name)

    to_implement = {n for n, o in operators.items() if not n.startswith('_') and isbuiltin(o)}
    to_implement.discard('xor')  # not implemented, on purpose
    assert untested == {'and_', 'or_'}  # special implementations
    assert tested == to_implement - untested
