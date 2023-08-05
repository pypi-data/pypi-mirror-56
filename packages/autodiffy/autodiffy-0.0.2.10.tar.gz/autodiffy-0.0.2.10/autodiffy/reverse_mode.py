import numpy as np


def reverse_mode(op, val1, val2=None):
    """Defines derivatives of elementary function (no chain rule) that are used in the forward pass of reverse mode."""
    if op == 'neg':
        return -1, None

    if op == '+':
        return 1, 1

    if op == '-':
        return 1, -1

    if op == '*':
        return val2, val1

    if op == '/':
        return 1 / val2, -val1 / (val2 ** 2)

    if op == '**':
        return val2 * val1 ** (val2 - 1), val1 ** val2 * np.log(val1)

    if op == 'sin':
        return np.cos(val1), None

    if op == 'cos':
        return -np.sin(val1), None

    if op == 'tan':
        return 1 / (np.cos(val1) ** 2), None

    if op == 'exp':
        return np.exp(val1), None

    if op == 'log':
        return 1 / val1, None

    if op == 'log10':
        return 1 / (val1 * np.log(10)), None

    if op == 'sqrt':
        return reverse_mode('**', val1, 0.5)
