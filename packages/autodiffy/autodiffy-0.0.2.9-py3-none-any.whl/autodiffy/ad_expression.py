import numpy as np

from autodiffy.parse_tree import ParseTree


class VarsExpression:

    def __init__(self, eval_dict, expr=None):
        self.eval_dict = eval_dict
        self.expr = list(eval_dict.keys())[0] if not expr else expr

    def __neg__(self):
        return VarsExpression(self.eval_dict, '-(' + self.expr + ')')

    def __add__(self, value):
        try:
            return VarsExpression({**self.eval_dict, **value.eval_dict}, '(' + self.expr + '+' + value.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '+' + str(value) + ')')

    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        try:
            return VarsExpression({**self.eval_dict, **value.eval_dict}, '(' + self.expr + '-' + value.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '-' + str(value) + ')')

    def __rsub__(self, value):
        return VarsExpression(self.eval_dict, '(' + str(value) + '-' + self.expr + ')')

    def __mul__(self, factor):
        try:
            return VarsExpression({**self.eval_dict, **factor.eval_dict}, '(' + self.expr + '*' + factor.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '*' + str(factor) + ')')

    def __rmul__(self, factor):
        return self * factor

    def __truediv__(self, factor):
        try:
            return VarsExpression({**self.eval_dict, **factor.eval_dict}, '(' + self.expr + '/' + factor.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '/' + str(factor) + ')')

    def __rtruediv__(self, factor):
        return VarsExpression(self.eval_dict, '(' + str(factor) + '/' + self.expr + ')')

    def __pow__(self, value):
        try:
            return VarsExpression({**self.eval_dict, **value.eval_dict}, '(' + self.expr + '**' + value.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '**' + str(value) + ')')

    def __rpow__(self, value):
        VarsExpression(self.eval_dict, '(' + str(value) + '**' + self.expr + ')')

    def sin(self):
        return VarsExpression(self.eval_dict, '(' + 'sin(' + self.expr + '))')

    def cos(self):
        return VarsExpression(self.eval_dict, '(' + 'cos(' + self.expr + '))')

    def tan(self):
        return VarsExpression(self.eval_dict, '(' + 'tan(' + self.expr + '))')

    def exp(self):
        return VarsExpression(self.eval_dict, '(' + 'exp(' + self.expr + '))')

    def log(self):
        return VarsExpression(self.eval_dict, '(' + 'log(' + self.expr + '))')

    def log10(self):
        return VarsExpression(self.eval_dict, '(' + 'log10(' + self.expr + '))')

    def sqrt(self):
        return VarsExpression(self.eval_dict, '(' + 'sqrt(' + self.expr + '))')

    def __str__(self):
        return self.expr

    def change_val(self, new_eval_dict):
        for key, val in new_eval_dict.items():
            if key not in self.eval_dict:
                raise KeyError
            self.eval_dict[key] = val

    @staticmethod
    def evaluate_one_point(expr, eval_dict, mode):
        pt = ParseTree('(' + expr + ')', eval_dict)
        if mode.startswith('f'):
            pt.implement_forward_mode()

        elif mode.startswith('r'):
            pt.implement_reverse_mode()

        else:
            raise ValueError('must enter valid mode (forward or backwards)')

        return pt.get_results()

    def evaluate(self, mode):
        try:
            store_results = []
            for i in range(len(list(self.eval_dict.values())[0])):
                eval_dict = {key: value[i] for key, value in self.eval_dict.items()}
                store_results.append(self.evaluate_one_point(self.expr, eval_dict, mode))
            values = [d['value'] for d in store_results]
            partial_derivatives = [d['partial_derivatives'] for d in store_results]
            return {'value': values, 'partial_derivatives': partial_derivatives}

        except TypeError:
            return self.evaluate_one_point(self.expr, self.eval_dict, mode)


def evaluate(exprs, mode):
    try:
        return [expr.evaluate(mode) for expr in exprs]
    except TypeError:
        return exprs.evaluate(mode)


def instantiate_AD(d):
    assert len(d) > 0, 'must pass in non-empty dictionary'
    lst = []
    for key, val in d.items():
        # TODO: check if val is a number (or vector of numbers)
        lst.append(VarsExpression({key: val}))
    return tuple(lst) if len(d) > 1 else lst[0]
