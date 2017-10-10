""" Check what the `lambdax` module publicly exposes. """
import builtins
from inspect import isbuiltin, ismodule, isclass
from itertools import chain
import operator
from unittest.mock import patch

import lambdax.builtins_as_lambdas
import lambdax.builtins_overridden
from lambdax import x1, x2, x


def _get_exposed(tested_module):
    return {name for name, obj in vars(tested_module).items()
            if not name.startswith('_') and not ismodule(obj)}


def test_no_builtin_exposed():
    for obj in chain(vars(lambdax).values(), vars(lambdax.builtins_overridden).values()):
        assert not isbuiltin(obj)


def test_base_exposed():
    variables = {'x'} | {'x%d' % i for i in range(1, 10)}
    variables |= {v.upper() for v in variables}
    special_functions = {'λ', 'is_λ', 'comp', 'circle', 'chaining', 'and_', 'or_', 'if_'}

    to_expose = variables | special_functions
    exposed = _get_exposed(lambdax.lambda_calculus)

    assert to_expose == exposed


def test_operators_exposed():
    operators = {name for name, obj in vars(operator).items()
                 if not name.startswith('_') and not isclass(obj) and not hasattr(builtins, name)}
    to_expose = operators.difference(('and_', 'or_', 'xor'))

    assert to_expose == _get_exposed(lambdax.operators)


def test_overridden_builtins_exposed():
    builtin_names = {name for name, obj in vars(builtins).items()
                     if name[0].upper() != name[0]}

    irrelevant_builtins = {
        'input', 'help', 'open',
        'copyright', 'license', 'credits',
        'compile', 'eval', 'exec', 'execfile', 'runfile',
        'classmethod', 'staticmethod', 'property',
        'object', 'super',
        'globals', 'locals'
    }

    builtins_to_expose = builtin_names - irrelevant_builtins
    to_expose_as_λ = {name + '_λ' for name in builtins_to_expose}

    split_exposed_names = (name.split('_') for name in _get_exposed(lambdax.builtins_as_lambdas))
    exposed_as_λ = {'%s_%s' % (words[0], words[-1]) for words in split_exposed_names}

    assert to_expose_as_λ == exposed_as_λ
    assert builtins_to_expose == _get_exposed(lambdax.builtins_overridden)


def test_operators_implementations():
    operators = vars(operator)
    for name, abstraction in vars(lambdax.operators).items():
        initial = operators.get(name)
        if initial and isbuiltin(initial):
            wrapped = getattr(abstraction, '_λ_constant')
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


def _get_effect(implementation):
    output = []
    with patch('sys.stdout') as out:
        out.side_effect = output.append
        try:
            res = implementation("42")
        except BaseException as e:
            res = e.args
    return res, output


def _get_method_or_object(obj, meth=''):
    return getattr(obj, meth) if meth else obj


def test_overridden_builtins_implementations():
    for name in _get_exposed(lambdax.builtins_as_lambdas):
        obj, tail = name.split('_', 1)
        meth = tail[:-2]
        original = _get_method_or_object(getattr(builtins, obj), meth)
        as_λ = getattr(lambdax.builtins_as_lambdas, name)
        overridden = _get_method_or_object(getattr(lambdax.builtins_overridden, obj), meth)
        ref, ref_output = _get_effect(original)
        expl, expl_output = _get_effect(as_λ(x))
        iso, iso_output = _get_effect(overridden)
        lbda, lbda_output = _get_effect(overridden(x))
        assert lbda_output == iso_output == expl_output == ref_output
        try:
            assert list(iter(lbda)) == list(iter(iso)) == list(iter(expl)) == list(iter(ref))
        except TypeError:
            assert lbda == iso == expl == ref
