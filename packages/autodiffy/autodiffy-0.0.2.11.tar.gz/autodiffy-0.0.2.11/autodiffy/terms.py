import numpy as np
import operator


class Terms:
    """Defines unary and binary operators and maps each operator from a string representation to an actual
    implementation using either the operator module or the numpy package."""

    def __init__(self):

        self.binops = {'+', '*', '/', '**'}

        self.binops2operator = {'+': operator.add,
                                '-': operator.sub,
                                '*': operator.mul,
                                '/': operator.truediv,
                                '**': operator.pow}

        self.unop2operator = {'sin': np.sin,
                              'cos': np.cos,
                              'tan': np.tan,
                              'exp': np.exp,
                              'log': np.log,
                              'log10': np.log10,
                              'sqrt': np.sqrt,
                              'arcsin': np.arcsin,
                              'arccos': np.arccos,
                              'arctan': np.arctan,
                              'neg': operator.neg}

        self.trivial_reverse_mode_ops = {'neg', '+', '-'}
