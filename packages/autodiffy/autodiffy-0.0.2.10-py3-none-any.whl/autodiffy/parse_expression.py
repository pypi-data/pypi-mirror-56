from autodiffy.terms import Terms


class ParseExpression:

    def __init__(self):
        self.terms = Terms()

    def _get_function(self, expr, var_names):
        """Extracts words of arbitrary length (e.g. sin, exp) from the overall string representation. Note: along
        with _get_numpy_expr defined below, this class handles numpy functions that are defined with or without the
        'np.' prefix."""
        if expr[:5] == 'log10':
            return 5, 'log10'

        for idx, char in enumerate(expr):
            if not char.isalpha():
                if char.isnumeric():
                    raise ValueError('invalid expression')
                candidate_expr = expr[:idx]
                if candidate_expr in self.terms.unop2operator or candidate_expr in var_names:
                    return idx, candidate_expr
                raise ValueError('invalid expression')

        raise ValueError('invalid expression')

    @staticmethod
    def _get_number(expr):
        """Extracts numbers (integers and floats) of arbitrary length from the overall string representation."""
        for idx, digit in enumerate(expr):
            if not digit.isnumeric() and digit is not '.':
                if digit.isalpha():
                    raise ValueError('invalid expression')
                return idx, expr[:idx]

        return expr

    @staticmethod
    def _get_numpy_expr(expr):
        """Extracts numpy operations from the overall string representation."""
        if expr[:5] == 'log10':
            return 5, 'log10'

        for idx, char in enumerate(expr):
            if not char.isalpha():
                if char.isnumeric():
                    raise ValueError('invalid expression')
                return idx, expr[:idx]

    def parse_expression(self, expr, var_names):
        """ Parses a string representation of an expression into a list of string elements that make up that expression.
        These elements include parantheses, numbers, variables and elementary operations such as '**' and 'np.sin'.

        EXAMPLES
        =========
        >>> ParseExpression().parse_expression('(x + y + sin(x*y)', {'x': 2, 'y': 3})
        ['(', 'x', '+', 'y', '+', 'sin', '(', 'x', '*', 'y', ')']
        """

        tokens = []
        idx = 0
        while idx < len(expr):

            if expr[idx: idx + len('np.')] == 'np.':
                expr_len, np_expr = ParseExpression._get_numpy_expr(expr[idx + 3:])
                tokens.append(np_expr)
                idx += (len('np.') + expr_len)

            elif expr[idx].isalpha():
                expr_len, fun = self._get_function(expr[idx:], var_names)
                tokens.append(fun)
                idx += expr_len

            elif expr[idx].isnumeric() or expr[idx] is '.':
                expr_len, num = ParseExpression._get_number(expr[idx:])
                tokens.append(num)
                idx += expr_len

            elif expr[idx: idx + len('**')] == '**':
                tokens.append('**')
                idx += len('**')

            elif expr[idx] == ' ':
                idx += 1

            else:
                tokens.append(expr[idx])
                idx += 1

        return tokens
