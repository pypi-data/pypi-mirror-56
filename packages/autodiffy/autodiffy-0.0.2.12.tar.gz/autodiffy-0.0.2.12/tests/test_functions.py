import numpy as np

from autodiffy.ad_expression import *


def test_add():
    x = VarsExpression({'x': 2})
    f = x + 3
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 5))
    assert (np.isclose(result['partial_derivatives']["x"], 1))


def test_radd():
    x = VarsExpression({'x': 2})
    f = 3 + x
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 5))
    assert (np.isclose(result['partial_derivatives']["x"], 1))


def test_sub():
    x = VarsExpression({'x': 2})
    f = x - 3
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], -1))
    assert (np.isclose(result['partial_derivatives']["x"], 1))


def test_rsub():
    x = VarsExpression({'x': 2})
    f = 3 - x
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 1))
    assert (np.isclose(result['partial_derivatives']["x"], -1))


def test_mul():
    x = VarsExpression({'x': 2})
    f = x*2
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 4))
    assert (np.isclose(result['partial_derivatives']["x"], 2))


def test_rmul():
    x = VarsExpression({'x': 2})
    f = 2*x
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 4))
    assert (np.isclose(result['partial_derivatives']["x"], 2))


def test_truediv():
    x = VarsExpression({'x': 2})
    f = x/2
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 1))
    assert (np.isclose(result['partial_derivatives']["x"], 0.5))


def test_rtruediv():
    x = VarsExpression({'x': 2})
    f = 1/x
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 0.5))
    assert (np.isclose(result['partial_derivatives']["x"], -0.25))


def test_pow():
    x = VarsExpression({'x': 2})
    f = x**2
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], 4))
    assert (np.isclose(result['partial_derivatives']["x"], 4))


def test_sin():    
    x = VarsExpression({'x': 2})
    f = np.sin(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.sin(2)))
    assert (np.isclose(result['partial_derivatives']["x"], np.cos(2)))


def test_cos():
    x = VarsExpression({'x': 2})
    f = np.cos(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.cos(2)))
    assert (np.isclose(result['partial_derivatives']["x"], -np.sin(2)))


def test_tan():
    x = VarsExpression({'x': 2})
    f = np.tan(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.tan(2)))
    assert (np.isclose(result['partial_derivatives']["x"], 1/(np.cos(2)**2)))


def test_exp():
    x = VarsExpression({'x': 2})
    f = np.exp(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.exp(2)))
    assert (np.isclose(result['partial_derivatives']["x"], np.exp(2)))


def test_log():
    x = VarsExpression({'x': 2})
    f = np.log(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.log(2)))
    assert (np.isclose(result['partial_derivatives']["x"], 1/2))


def test_log10():
    x = VarsExpression({'x': 2})
    f = np.log10(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.log10(2)))
    assert (np.isclose(result['partial_derivatives']["x"], 1 / (2 * np.log(10))))


def test_sqrt():
    x = VarsExpression({'x': 4})
    f = np.sqrt(x)
    result = evaluate(f, "r")

    assert (np.isclose(result["value"], np.sqrt(4)))
    assert (np.isclose(result['partial_derivatives']["x"], 0.25))


def test_change_val():	
    x = VarsExpression({'x': 4})
    h = x + 1
    h.change_val({'x': [1, 2, 3]})
    try:
        h.change_val({'z': [1, 2, 3], 'y': [1, 2, 3]})
    except:
        pass


def test_eval():
    x = VarsExpression({'x': 4})
    f = np.sqrt(x)
    try:
        evaluate(f, "x")
    except:
        pass
