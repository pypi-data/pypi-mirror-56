import numpy as np
import pytest

from ad_expression import *
from parse_expression import ParseExpression
from parse_tree import ParseTree


def test_parse_tree():
    threshold = 1e-12

    def test_case(expr, vars, val, ders):
        tree = ParseTree(expr, vars)
        modes = [tree.implement_forward_mode, tree.implement_reverse_mode]
        for mode in modes:
            mode()
            assert abs(tree.get_value() - val) < threshold
            for var in vars:
                assert abs(tree.get_derivative(var) - ders[var]) < threshold

    test_case('(x-(exp((((sin((x*4)))**2)*-2))))', {'x': np.pi / 16},
              np.pi / 16 - (1 / np.exp(1)), {'x': 1 + (8 / np.exp(1))})

    test_case('(x - (exp((-2 * ((sin((4 * x))) ** 2)))))', {'x': np.pi / 16},
              np.pi / 16 - (1 / np.exp(1)), {'x': 1 + (8 / np.exp(1))})

    test_case('(x - (exp((2 * ((sin((4 * x))) ** 2)))))', {'x': np.pi / 16},
              np.pi / 16 - (1 / np.exp(-1)), {'x': 1 - (8 / np.exp(-1))})

    test_case('exp(-(sin(x)-cos(y)) ** 2)', {'x': np.pi / 2, 'y': np.pi / 3},
              np.exp(-0.25), {'x': 0, 'y': -np.sqrt(3) * np.exp(-0.25) / 2})

    test_case('(x + y + sin(x*y)', {'x': 2, 'y': 3}, 5 + np.sin(6), {'x': 1 + 3 * np.cos(6), 'y': 1 + 2 * np.cos(6)})

    test_case('(x * y + np.sin(x) - 2)', {'x': 2, 'y': 3}, 4 + np.sin(2), {'x': 3 + np.cos(2), 'y': 2})

    test_case('((log(2*x)) + log10(y) + (x ** 3) - sqrt(y) + tan(y) + ((x ** 2) / (y + 1)))',
              {'x': 2, 'y': 4}, np.log10(4) + np.log(4) + np.tan(4) + 6.8,
              {'x': 13.3, 'y': -0.41 + 1 / (4 * np.log(10)) + 1 / (np.cos(4) ** 2)})

    test_case('((3 ** (x ** 2)) / 3)', {'x': 2}, 27, {'x': 108 * np.log(3)})

    test_case('((1 / x) + 23)', {'x': 2}, 23.5, {'x': -0.25})

    with pytest.raises(ValueError):
        ParseExpression().parse_expression('(2 * cosh(x))', {'x': 2})

    with pytest.raises(ValueError):
        ParseExpression().parse_expression('(2 * np.cos1(x))', {'x': 2})

    with pytest.raises(ValueError):
        ParseExpression().parse_expression('(2 * np.cos(x) + 125a)', {'x': 2})

    eval_dict = {'x': 2, 'y': 3}
    x, y = instantiate_AD(eval_dict)
    f = x + y + np.sin(x * y)
    test_case(str(f), eval_dict, 5 + np.sin(6), {'x': 1 + 3 * np.cos(6), 'y': 1 + 2 * np.cos(6)})


test_parse_tree()
