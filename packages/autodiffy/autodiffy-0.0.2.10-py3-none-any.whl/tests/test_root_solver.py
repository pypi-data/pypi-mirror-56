# Import autodiffy
from autodiffy.ad_expression import AD

# Test function: f(x) = (x + 1)^2 = x^2 + 2x + 1

# Option 1: Build-up (f1)
x = AD({'x': 1})
f1 = (x + 1) ** 2

# Newton's method
def newton(f, x0, tol=1e-6, max_iter=1e6):
    '''Performs Newton's method to find the zeros of a scalar function f

    TODO: EXTENSIVE DOCUMENTATION HERE
    '''