import numpy as np
from autodiffy.parse_tree import ParseTree


class VarsExpression:
    """ Stores a string representation of the expression for which the user wants to calculate the partial derivatives
    using either forward mode or reverse mode.
    
    INPUTS
    ======= 
    eval_dict: A dictionary with key-value pair as { Key: variable label, Value: variable value ( must be numeric ) }
    expr: expression to evaluate

    EXAMPLES
    =========
    >>> x = VarsExpression({'x': 2})
    >>> x
    x
    >>> y = VarsExpression({'y': 3})
    >>> y.eval_dict
    {'y': 3}
    >>> z = VarsExpression({'x': 2, 'y': 3}, "x + y")
    >>> z
    x + y
    """

    def __init__(self, eval_dict, expr=None):
        self.eval_dict = eval_dict
        self.expr = list(eval_dict.keys())[0] if not expr else expr

    def __neg__(self):
        return VarsExpression(self.eval_dict, '-(' + self.expr + ')')

    def __add__(self, value):
        """        
        INPUTS
        ======= 
        value: A VarsExpression or numeric value
        
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> y = VarsExpression({'y': 3})
        >>> f = x + y
        >>> f
        (x+y)
        >>> f.eval_dict
        {'x': 2, 'y': 3}
        >>> x = VarsExpression({'x': 2})
        >>> f = x + 3
        >>> f
        (x+3)
        >>> f.eval_dict
        {'x': 2}
        """
        try:
            return VarsExpression({**self.eval_dict, **value.eval_dict}, '(' + self.expr + '+' + value.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '+' + str(value) + ')')

    def __radd__(self, value):
        return self + value

    def __sub__(self, value):
        """        
        INPUTS
        ======= 
        value: A VarsExpression or numeric value
        
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> y = VarsExpression({'y': 3})
        >>> f = x - y
        >>> f.expr
        '(x-y)'
        >>> f.eval_dict
        {'x': 2, 'y': 3}
        >>> x = VarsExpression({'x': 2})
        >>> f = x - 3
        >>> f.expr
        '(x-3)'
        """
        try:
            return VarsExpression({**self.eval_dict, **value.eval_dict}, '(' + self.expr + '-' + value.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '-' + str(value) + ')')

    def __rsub__(self, value):
        return VarsExpression(self.eval_dict, '(' + str(value) + '-' + self.expr + ')')

    def __mul__(self, factor):
        """        
        INPUTS
        ======= 
        value: A VarsExpression or numeric value
        
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> y = VarsExpression({'y': 3})
        >>> f = x * y
        >>> f.expr
        '(x*y)'
        >>> f.eval_dict
        {'x': 2, 'y': 3}
        >>> x = VarsExpression({'x': 2})
        >>> f = x * 3
        >>> f.expr
        '(x*3)'
        """
        try:
            return VarsExpression({**self.eval_dict, **factor.eval_dict}, '(' + self.expr + '*' + factor.expr + ')')

        except AttributeError:
            return VarsExpression(self.eval_dict, '(' + self.expr + '*' + str(factor) + ')')

    def __rmul__(self, factor):
        return self * factor

    def __truediv__(self, factor):
        """        
        INPUTS
        ======= 
        value: A VarsExpression or numeric value
        
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> y = VarsExpression({'y': 3})
        >>> f = x / y
        >>> f.expr
        '(x/y)'
        >>> x = VarsExpression({'x': 2})
        >>> f = x / 3
        >>> f.expr
        '(x/3)'
        """
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
        return VarsExpression(self.eval_dict, '(' + str(value) + '**' + self.expr + ')')

    def sin(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.sin(x)
        >>> f
        (sin(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'sin(' + self.expr + '))')

    def cos(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.cos(x)
        >>> f
        (cos(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'cos(' + self.expr + '))')

    def tan(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.tan(x)
        >>> f
        (tan(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'tan(' + self.expr + '))')

    def exp(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.exp(x)
        >>> f
        (exp(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'exp(' + self.expr + '))')

    def log(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.log(x)
        >>> f.expr
        '(log(x))'
        """
        return VarsExpression(self.eval_dict, '(' + 'log(' + self.expr + '))')

    def log10(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.log10(x)
        >>> f
        (log10(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'log10(' + self.expr + '))')

    def sqrt(self):
        """            
        RETURNS
        ========
        VarsExpression

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> f = np.sqrt(x)
        >>> f
        (np.sqrt(x))
        """
        return VarsExpression(self.eval_dict, '(' + 'np.sqrt(' + self.expr + '))')

    def __str__(self):
        return self.expr

    def __repr__(self):
        return self.expr

    def change_val(self, new_eval_dict):
        """ Changes the values at which to evaluate a given VarsExpression object.

        INPUTS          
        ======= 
        new_eval_dict: A dictionary (key: variable, value: list of evaluation points)

        EXAMPLES
        =========
        >>> x = VarsExpression({'x': 2})
        >>> x.change_val({'x': [1, 2, 3]})
        >>> x
        x
        """
        for key, val in new_eval_dict.items():
            if key not in self.eval_dict:
                raise KeyError
            self.eval_dict[key] = val

    @staticmethod
    def evaluate_one_point(expr, eval_dict, mode):
        """Evaluates the value and partial derivatives of a single VarsExression object that is a scalar function."""
        pt = ParseTree('(' + expr + ')', eval_dict)
        if mode.startswith('f'):
            pt.implement_forward_mode()

        elif mode.startswith('r'):
            pt.implement_reverse_mode()

        else:
            raise ValueError('must enter valid mode (forward or backwards)')

        return pt.get_results()

    def evaluate(self, mode):        
        """Evaluates the value and partial derivatives of a single VarsExression object that is either a scalar function
        or a vector-valued function.

        INPUTS
        ======= 
        mode (String): "f": Forward mode or "r": Reverse mode
        
        RETURNS
        ========
        Dictionary of value and partial derivatives of each variable

        EXAMPLES
        ========
        >>> x = VarsExpression({'x': 2})
        >>> y = VarsExpression({'y': 3})
        >>> f = x + y
        >>> f.evaluate("f")
        {'value': 5, 'partial_derivatives': {'x': 1, 'y': 1}}
        >>> f.evaluate("r")
        {'value': 5, 'partial_derivatives': {'x': 1, 'y': 1}}
        >>> f = x * y
        >>> f.evaluate("f")
        {'value': 6, 'partial_derivatives': {'x': 3, 'y': 2}}
        """

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
    """Evaluates either a vector of functions or a single function."""
    try:
        return [expr.evaluate(mode) for expr in exprs]
    except TypeError:
        return exprs.evaluate(mode)


def instantiate_AD(d):
    """Instantiates an arbitrary number of VarsExpression objects.

    INPUTS
    ======= 
    d: A dictionary with key-value pair as { Key: variable label, Value: variable value ( must be numeric ) } 
    
    RETURNS
    ========
    A tuple of VarsExpression objects

    EXAMPLES
    =========
    >>> x, y = instantiate_AD({'x': 2, 'y': 3})
    >>> x
    x
    >>> x.eval_dict
    {'x': 2}
    >>> y
    y
    >>> y.eval_dict
    {'y': 3}
    """
    assert len(d) > 0, 'must pass in non-empty dictionary'
    lst = []
    for key, val in d.items():
        lst.append(VarsExpression({key: val}))
    return tuple(lst) if len(d) > 1 else lst[0]
