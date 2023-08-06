import numpy as np
import pytest

from autodiffy.ad_expression import *
from autodiffy.parse_expression import ParseExpression
from autodiffy.parse_tree import ParseTree


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

    def test_vector_valued_function(expected_result, ad):
        for mode in ['f', 'r']:
            result = evaluate(ad, mode)
            vector_length = len(result['value'])
            vars = list(ad.eval_dict.keys())
            for i in range(vector_length):
                assert abs(expected_result['value'][i] - result['value'][i]) < threshold
                for var in vars:
                    assert abs(expected_result['partial_derivatives'][i][var] -
                               result['partial_derivatives'][i][var]) < threshold

    def test_vector_of_functions(expected_result, ad_lst):
        for mode in ['f', 'r']:
            result = evaluate(ad_lst, mode)
            for i in range(len(ad_lst)):
                assert abs(expected_result[i]['value'] - result[i]['value']) < threshold
                vars = list(result[i]['partial_derivatives'].keys())
                for var in vars:
                    assert abs(expected_result[i]['partial_derivatives'][var] -
                               result[i]['partial_derivatives'][var]) < threshold

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

    test_case('(3**((x*2)+4))', {'x': 2}, 6561, {'x': 6561 * 2 * np.log(3)})

    test_case('(((x*3)-2)**((x*2)+4))', {'x': 2}, 65536, {'x': (4 ** 8) * (2 * np.log(4) + (8 / 4) * 3)})

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

    eval_dict = {'x': 1, 'y': 2, 'z': 3}
    x, y, z = instantiate_AD(eval_dict)
    f = x * y * z + x * np.exp(np.cos(y)) - np.sin(x / z)
    test_case(str(f), eval_dict, 6 + np.exp(np.cos(2)) - np.sin(1 / 3),
              {'x': 6 + np.exp(np.cos(2)) - (np.cos(1 / 3) / 3), 'y': 3 - np.exp(np.cos(2)) * np.sin(2),
               'z': 2 + (np.cos(1 / 3) / 9)})

    x, y = instantiate_AD({'x': 2, 'y': 3})
    f = x + y + np.sin(x * y)
    f.change_val({'x': [1, 2, 3], 'y': [1, 2, 4]})
    expected_result = {'value': [2 + np.sin(1), 4 + np.sin(4), 7 + np.sin(12)],
                       'partial_derivatives': [{'x': 1 + np.cos(1), 'y': 1 + np.cos(1)},
                                               {'x': 1 + 2 * np.cos(4), 'y': 1 + 2 * np.cos(4)},
                                               {'x': 1 + 4 * np.cos(12), 'y': 1 + 3 * np.cos(12)}]}

    test_vector_valued_function(expected_result, f)

    x, y = instantiate_AD({'x': 2, 'y': 3})
    f = x + y + np.sin(x * y)
    g = x * y + np.sin(x) - 2
    ad_lst = np.array([f, g])
    expected_result = [{'value': 5 + np.sin(6),
                        'partial_derivatives': {'x': 1 + 3 * np.cos(6), 'y': 1 + 2 * np.cos(6)}},
                       {'value': 4 + np.sin(2), 'partial_derivatives': {'x': 3 + np.cos(2), 'y': 2}}]

    test_vector_of_functions(expected_result, ad_lst)

    x = instantiate_AD({'x': 3})
    f = x + x ** 5 - np.cos(x)
    g = x + x ** 5 - np.cos(x)
    h = x + x ** 5 - np.sin(x)
    assert f == g
    assert f != h

    eval_dict = {'x': 2}
    x = instantiate_AD(eval_dict)
    f = logistic(x) / np.cos(-x)
    test_case(str(f), eval_dict, (1 / (1 + np.exp(-2))) / np.cos(-2),
              {'x': (np.exp(-2) * np.cos(2) + np.sin(2) * (np.exp(-2) + 1)) / ((np.cos(2) * (np.exp(-2) + 1)) ** 2)})

    eval_dict = {'x': 0.5}
    x = instantiate_AD(eval_dict)
    f = np.arcsin(x) - np.arccos(x) + np.arctan(x)
    test_case(str(f), eval_dict, np.arcsin(0.5) - np.arccos(0.5) + np.arctan(0.5),
              {'x': (2 / np.sqrt(1 - 0.25)) + 1 / (1 + 0.25)})

    eval_dict = {'x': 0.5}
    x = instantiate_AD(eval_dict)
    f = np.sinh(x) - np.cosh(x) + np.tanh(x)
    test_case(str(f), eval_dict, np.sinh(0.5) - np.cosh(0.5) + np.tanh(0.5),
              {'x': np.cosh(0.5) - np.sinh(0.5) + 1 - np.tanh(0.5) ** 2})

    eval_dict = {'x': 2}
    x = instantiate_AD(eval_dict)
    f = log_arbitrary_base(x, 3) * log_arbitrary_base(7, 4)
    test_case(str(f), eval_dict, (np.log(2) / np.log(3)) * (np.log(7) / np.log(4)),
              {'x': (np.log(7) / np.log(4)) * (1 / (2 * np.log(3)))})
