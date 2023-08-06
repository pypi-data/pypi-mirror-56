from pythonds.basic import Stack

from autodiffy.binary_tree import BinaryTreeExtended
from autodiffy.forward_mode import ForwardMode
from autodiffy.parse_expression import ParseExpression
from autodiffy.reverse_mode import reverse_mode
from autodiffy.terms import Terms

#from binary_tree import BinaryTreeExtended
#from forward_mode import ForwardMode
#from parse_expression import ParseExpression
#from reverse_mode import reverse_mode
#from terms import Terms


class ParseTree:
    """Handles the implementation of forward mode and reverse mode using a binary tree data structure.

    INPUTS
    =======
    expr: string representation of expression on which to perform automatic differentiation
    variables: dictionary containing the variables and the values at which to evaluate them
    """
    def __init__(self, expr, variables):
        self.expr = expr
        self.variables = variables
        self.terms = Terms()
        self.parse_tree = self._build_parse_tree()
        self.result = None
        self._storage_dict = {var: 0 for var in self.variables}

    @staticmethod
    def _is_numeric(num):
        return all(x.isnumeric() or x is '.' for x in num)

    def _build_parse_tree(self):
        """ Converts the string representation of an expression into a binary tree in which each node is either a unary
        operator, in which case it only has a left child, a binary operator, in which case it has both a left and
        a right child, or a variable or number in which case it is a leaf node.
        """
        token_lst = ParseExpression().parse_expression(self.expr, self.variables)
        stack = Stack()
        tree = BinaryTreeExtended('')
        stack.push(tree)
        current_tree = tree
        idx = 0
        while idx < len(token_lst):
            token = token_lst[idx]

            if token == '(':
                current_tree.insertLeft('')
                stack.push(current_tree)
                current_tree = current_tree.getLeftChild()
                idx += 1

            elif token in set(self.terms.binops) | {'-'}:

                # node already has value so tree needs to be extended
                if current_tree.getRootVal():
                    if stack.size() == 1:
                        tree = BinaryTreeExtended('')
                        tree.insertLeftExistingTree(current_tree)
                        current_tree = tree
                    else:
                        current_child = current_tree.getLeftChild()
                        new_child = BinaryTreeExtended('')
                        new_child.insertLeftExistingTree(current_child)
                        current_tree.insertLeftExistingTree(new_child)
                        stack.push(current_tree)
                        current_tree = current_tree.getLeftChild()

                if token in self.terms.binops:
                    current_tree.setRootVal(token)
                    current_tree.insertRight('')
                    stack.push(current_tree)
                    current_tree = current_tree.getRightChild()
                    idx += 1

                elif token == '-':

                    # '-' should be treated as a minus sign
                    if current_tree.getLeftChild():
                        current_tree.setRootVal(token)
                        current_tree.insertRight('')
                        stack.push(current_tree)
                        current_tree = current_tree.getRightChild()
                        idx += 1

                    # '-' should be treated as a negation
                    elif not self._is_numeric(token_lst[idx + 1]):
                        current_tree.setRootVal('neg')
                        idx += 1

                    # '-' should be treated as a negative number
                    else:
                        current_tree.setRootVal('-' + token_lst[idx + 1])
                        parent = stack.pop()
                        current_tree = parent
                        idx += 2

                else:
                    raise ValueError

            elif token == ')':
                current_tree = stack.pop()
                idx += 1

            elif token in self.terms.unop2operator:
                current_tree.setRootVal(token)
                idx += 1

            elif self._is_numeric(token) or token in self.variables:
                current_tree.setRootVal(token)
                parent = stack.pop()
                current_tree = parent
                idx += 1

            else:
                raise ValueError

        return tree

    def _evaluate_val(self, val, mode):
        """Evaluates a leaf node that is either a number of a variable. A number simply evaluates to that number. In
        forward mode, a variable is converted into a ForwardMode object and is seeded with a value of 1 for the
        partial derivative of the corresponding variable and a value of 0 for all other partial derivatives. In
        reverse mode, the variable is simply evaluated to the user-specified value."""
        if val in self.variables:
            if mode == 'forward':
                derivative_dict = {variable: 1 if variable == val else 0 for variable in self.variables}
                return ForwardMode(self.variables[val], derivative_dict)

            return self.variables[val]

        if val.replace('.', '', 1).replace('-', '', 1).isdigit() or val.startswith('np.'):
            return eval(val)

        raise ValueError('invalid leaf value (not numeric or variable)')

    def _evaluate_tree(self, tree, mode):
        """Recursive helper function to carry out forward mode and assist with the forward pass of reverse mode."""
        left_tree = tree.getLeftChild()
        right_tree = tree.getRightChild()

        if mode == 'reverse' and tree.getVal():
            return tree.getVal()

        if not right_tree:

            # no children so must be leaf
            if not left_tree:

                evaluation = self._evaluate_val(tree.getRootVal(), mode)
                if mode == 'reverse':
                    tree.setVal(evaluation)
                return evaluation

            # no value stored in node
            if not tree.getRootVal():
                return self._evaluate_tree(left_tree, mode)

            if tree.getRootVal() not in self.terms.unop2operator:
                raise ValueError('invalid node value')

            evaluation = self.terms.unop2operator[tree.getRootVal()](self._evaluate_tree(left_tree, mode))
            if mode == 'reverse':
                tree.setVal(evaluation)
            return evaluation

        if tree.getRootVal() not in self.terms.binops2operator:
            raise ValueError('invalid node value')

        evaluation = self.terms.binops2operator[tree.getRootVal()](self._evaluate_tree(left_tree, mode),
                                                                   self._evaluate_tree(right_tree, mode))
        if mode == 'reverse':
            tree.setVal(evaluation)
        return evaluation

    def _forward_pass_helper(self, tree):
        """Recursive helper function to carry out the forward pass of reverse mode."""
        if tree and tree.getLeftChild():
            left_tree = tree.getLeftChild()
            right_tree = tree.getRightChild()

            if not right_tree:

                # no value stored in node
                if not tree.getRootVal():
                    return self._forward_pass_helper(left_tree)

                if tree.getRootVal() not in self.terms.unop2operator:
                    raise ValueError('invalid node value')

                if tree.getRootVal() in self.terms.trivial_reverse_mode_ops:
                    tree.insertDerivatives(reverse_mode(tree.getRootVal()))
                else:
                    tree.insertDerivatives(reverse_mode(tree.getRootVal(), self._evaluate_tree(left_tree, 'reverse')))

                self._forward_pass_helper(left_tree)

            else:
                if tree.getRootVal() not in self.terms.binops2operator:
                    raise ValueError('invalid node value')

                if tree.getRootVal() in self.terms.trivial_reverse_mode_ops:
                    tree.insertDerivatives(reverse_mode(tree.getRootVal()))
                else:
                    tree.insertDerivatives(reverse_mode(tree.getRootVal(), self._evaluate_tree(left_tree, 'reverse'),
                                                        self._evaluate_tree(right_tree, 'reverse')))

                self._forward_pass_helper(left_tree)
                self._forward_pass_helper(right_tree)

    def _forward_pass(self):
        """Executes the forward pass of reverse mode."""
        return self._forward_pass_helper(self.parse_tree)

    def _reverse_pass_helper(self, tree, num):
        """Recursive helper function to carry out the reverse pass of reverse mode."""
        root_val = tree.getRootVal()

        if not root_val:
            self._reverse_pass_helper(tree.getLeftChild(), num)

        elif root_val in self.variables:
            self._storage_dict[tree.getRootVal()] += num

        elif root_val in self.terms.unop2operator:
            self._reverse_pass_helper(tree.getLeftChild(), num * tree.getDerivatives()[0])

        elif root_val in self.terms.binops2operator:
            self._reverse_pass_helper(tree.getLeftChild(), num * tree.getDerivatives()[0])
            self._reverse_pass_helper(tree.getRightChild(), num * tree.getDerivatives()[1])

    def _reverse_pass(self):
        """Executes the reverse pass of reverse mode."""
        return self._reverse_pass_helper(self.parse_tree, 1)

    def _evaluate_function_value(self):
        return self._evaluate_tree(self.parse_tree, 'reverse')

    def implement_forward_mode(self):
        """Executes forward mode and stores the result in the 'result' attribute."""
        self.result = self._evaluate_tree(self.parse_tree, 'forward')

    def implement_reverse_mode(self):
        """Executes both the forward pass and reverse pass of reverse mode and stores the
        result in the 'result' attribute."""
        self._forward_pass()
        self._reverse_pass()
        self.result = ForwardMode(self._evaluate_function_value(), self._storage_dict)

    def get_results(self):
        """Returns dictionary that contains the value of the expression and a dictionary of partial derivatives."""
        return {'value': self.result.val, 'partial_derivatives': self.result.der_dict}

    def get_value(self):
        """Retrieves value of expression."""
        return self.result.val

    def get_derivative(self, variable):
        """Retrieves the partial derivative corresponding to a given variable."""
        return self.result.der_dict[variable]
