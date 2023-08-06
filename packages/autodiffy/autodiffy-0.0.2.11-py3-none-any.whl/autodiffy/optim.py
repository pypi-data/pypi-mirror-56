import numpy as np
import autodiffy
import autodiffy.ad_expression as ad

def newton_rhapson(f, x0, tol=1e-10, max_iter=1e4):
    """
    Newton-Rhapson Root-Finding Algorithm using autodiffy
    
    INPUTS
    =======
    f: Scalar-valued function of a single variable to be evaluated
    x0: Initialization point for the algorithm
    tol: (Optional) Tolerance level for stopping condition
    max_iter: (Optional) Maximum number of iterations to prevent infinite loops
    
    RETURNS
    ========
    lst: A list containing the values from each iteration of the algorithm
    
    EXAMPLES
    =========
    >>> newton_rhapson(lambda x: x ** 2 + np.cos(x + np.pi/2), -0.5)[-1]
    -3.695065694300201e-17
    """
    # init list to hold iterations
    lst = [x0]
    # init x_curr
    x_curr = x0
    
    # init a VarsExpression object
    x = ad.instantiate_AD({'x':x0})
    # pass it into the function
    f = f(x)
    
    # init the diff to be some high number
    diff = 10
    # init counter for iterations
    iter_count = 0
    
    while(diff > tol):
        # compute val / deriv at current point
        feval = f.evaluate('f')
        # retrieve value and derivative
        fval = feval['value']
        fderiv = feval['partial_derivatives']['x']
        
        # iterative step for newton-rhapson
        x_curr -= fval/fderiv
        
        # set the difference based on last step
        diff = abs(lst[-1] - x_curr)
        # append x_curr
        lst.append(x_curr)
        # change value for f
        f.change_val({'x': x_curr})
        
        # check if algorithm has exceeded max_iter
        iter_count += 1
        if iter_count > max_iter:
            print(f'Warning: Algorithm stopped after {max_iter} iterations before convergence')
            break
    
    return lst

def grad_desc(f, x0, lr, tol=1e-10, max_iter=1e4):
    """
    Newton-Rhapson Root-Finding Algorithm using autodiffy
    
    INPUTS
    =======
    f: Scalar-valued function of a single variable to be evaluated
    x0: Initialization point for the algorithm
    lr: Learning rate for the algorithm
    tol: (Optional) Tolerance level for stopping condition
    max_iter: (Optional) Maximum number of iterations
    
    RETURNS
    ========
    lst: A list containing the values from each iteration of the algorithm
    
    EXAMPLES
    =========
    >>> newton_rhapson(lambda x: x ** 2 + np.cos(x + np.pi/2), -0.5)[-1]
    -3.695065694300201e-17
    """
    # init list to hold iterations
    lst = [x0]
    # init x_curr
    x_curr = x0
    
    # init a VarsExpression object
    x = ad.instantiate_AD({'x':x0})
    # pass it into the function
    f = f(x)
    
    # init the diff to be some high number
    diff = 10
    # init counter for iterations
    iter_count = 0
    
    while(diff > tol):
        # compute val / deriv at current point
        feval = f.evaluate('f')
        # retrieve value and derivative
        fderiv = feval['partial_derivatives']['x']
        
        # iterative step for newton-rhapson
        x_curr -= lr * fderiv
        
        # set the difference based on last step
        diff = abs(lst[-1] - x_curr)
        # append x_curr
        lst.append(x_curr)
        # change value for f
        f.change_val({'x': x_curr})
        
        # check if algorithm has exceeded max_iter
        iter_count += 1
        if iter_count > max_iter:
            print(f'Warning: Algorithm stopped after {max_iter} iterations before convergence')
            break
    
    return lst