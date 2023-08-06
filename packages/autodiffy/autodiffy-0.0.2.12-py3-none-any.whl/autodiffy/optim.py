import numpy as np
import autodiffy
import autodiffy.ad_expression as ad

def _letter(x:int):
    """Helper function to convert a number to a unique sequence of letters
    Uses first 10 letters for a base 10 representation"""
    first_10 = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j'}
    # convert input to string
    x = str(x)
    rs = ''
    for num in x:
        rs += first_10[int(num)]
    return rs

def newton_rhapson(f, ni:int, x0, tol=1e-10, max_iter=1e4):
    """
    Newton-Rhapson Root-Finding Algorithm using autodiffy
    
    INPUTS
    =======
    f: Scalar-valued function of a single variable to be evaluated
    num_input: Number of inputs that f expects
    x0: Vector containing initialization point for the algorithm
    tol: (Optional) Tolerance level for stopping condition
    max_iter: (Optional) Maximum number of iterations to prevent infinite loops
    
    RETURNS
    ========
    lst: A list containing the values (vectors) from each iteration of the algorithm
    
    EXAMPLES
    =========
    >>> newton_rhapson(lambda x: x ** 2 + np.cos(x + np.pi/2), 1, [-0.5])[-1]
    array([-3.69506569e-17])
    """
    # check if x0 is the same length as number of inputs
    assert len(x0) == ni, 'initial values not same length as number of inputs'

    # convert x0 to numpy array
    x0 = np.asarray(x0)

    # init list to hold iterations
    lst = [x0.copy()]
    # init x_curr
    x_curr = x0
    
    # init a tuple of VE objects of length ni for inputs
    # if number of inputs is 1, then no args handling is needed
    if ni == 1:
        x = ad.instantiate_AD({'x'+_letter(0):x0[0]})
        f = f(x)
    else:
        inputs = ad.instantiate_AD({'x'+_letter(num):x0[num] for num in range(ni)})
        # pass inputs into the function
        f = f(*inputs)
    
    # init the diff to be some high number
    diff = 10
    # init counter for iterations
    iter_count = 0
    
    while(diff > tol):
        # compute val / deriv at current point
        feval = f.evaluate('f')
        # retrieve value and derivative
        fval = feval['value']
        fderiv = np.asarray(list(feval['partial_derivatives'].values()))
        # break out of loop if derivative is 0
        if np.prod(fderiv) == 0:
            print(f'Derivative of 0 has been reached. Exiting')
            break
        
        # iterative step for newton-rhapson
        x_curr -= fval/fderiv
        
        # set the difference based on last step
        diff = np.linalg.norm((lst[-1] - x_curr))
        # append x_curr
        lst.append(x_curr.copy())
        # change value for f
        f.change_val({'x'+_letter(num):x_curr[num] for num in range(ni)})
        
        # check if algorithm has exceeded max_iter
        iter_count += 1
        if iter_count > max_iter:
            print(f'Warning: Algorithm stopped after {max_iter} iterations before convergence')
            break
    
    return lst

def gradient_descent(f, ni:int, x0, lr, tol=1e-10, max_iter=1e4):
    """
    Gradient Descent using autodiffy
    
    INPUTS
    =======
    f: Scalar-valued function of a single variable to be evaluated
    num_input: Number of inputs that f expects
    x0: Initialization point for the algorithm
    lr: Learning rate for the algorithm
    tol: (Optional) Tolerance level for stopping condition
    max_iter: (Optional) Maximum number of iterations
    
    RETURNS
    ========
    lst: A list containing the values from each iteration of the algorithm
    
    EXAMPLES
    =========
    >>> gradient_descent(lambda x: x ** 2 + np.cos(x + np.pi/2), 1, [-0.5], 1e-2)[-1]
    array([0.45018361])
    """
    # check if x0 is the same length as number of inputs
    assert len(x0) == ni, 'initial values not same length as number of inputs'

    # convert x0 to numpy array
    x0 = np.asarray(x0)

    # init list to hold iterations
    lst = [x0.copy()]
    # init x_curr
    x_curr = x0
    
    # init a tuple of VE objects of length ni for inputs
    # if number of inputs is 1, then no args handling is needed
    if ni == 1:
        x = ad.instantiate_AD({'x'+_letter(0):x0[0]})
        f = f(x)
    else:
        inputs = ad.instantiate_AD({'x'+_letter(num):x0[num] for num in range(ni)})
        # pass inputs into the function
        f = f(*inputs)
    
    # init the diff to be some high number
    diff = 10
    # init counter for iterations
    iter_count = 0
    
    while(diff > tol):
        # compute val / deriv at current point
        feval = f.evaluate('f')
        # retrieve value and derivative
        fderiv = np.asarray(list(feval['partial_derivatives'].values()))
        
        # iterative step for gradient descent
        x_curr -= lr * fderiv
        
        # set the difference based on last step
        diff = np.linalg.norm((lst[-1] - x_curr))
        # append x_curr
        lst.append(x_curr.copy())
        # change value for f
        f.change_val({'x'+_letter(num):x_curr[num] for num in range(ni)})
        
        # check if algorithm has exceeded max_iter
        iter_count += 1
        if iter_count > max_iter:
            print(f'Warning: Algorithm stopped after {max_iter} iterations before convergence')
            break
    
    return lst



def hmc_sampler(**kwargs):
    """
    1-Dimensional Hamiltonian Monte Carlo Sampling using autodiffy

    HMC uses Euclidean-Gaussian Kinetic Energy and Leap-frog integrator
    
    INPUTS
    =======
    u_energy: Target energy function
    step_size: Step size for movement simulation
    leapfrog_steps: Number of steps for leapfrog integrator
    total_samples: Number of samples to draw
    burn_in: Burn-in proportion (0 to 1)
    thinning_factor: Keep every nth observation sampled
    position_init: Initial position as a vector
    
    RETURNS
    ========
    sam: A numpy array containing the samples drawn
    
    EXAMPLES
    =========
    """
    ## Setup
    #read in all arguments
    u_energy = kwargs['u_energy']
    step_size = kwargs['step_size']
    leapfrog_steps = kwargs['leapfrog_steps']
    total_samples = kwargs['total_samples']
    burn_in = kwargs['burn_in']
    thinning_factor = kwargs['thinning_factor']
    #init a vector to hold the samples
    samples = []
    #start with specified initial position
    q_curr = kwargs['position_init']

    #instantiate u_energy as autodiffy object
    u = ad.instantiate_AD({'u':q_curr[0]})
    u_fun = u_energy(u)
    
    #set current u_energy
    u_eval = u_fun.evaluate('f')
    ue_curr = np.asarray([u_eval['value']])
    
    #keep track of acceptance probability
    ap = 0
    
    # Repeat total_samples times
    for sam in range(total_samples):
        if sam % 500 == 0:
            print(f'At iteration {sam}')
        ## Step A: kick-off
        #sample random momentum
        p_curr = np.random.normal(loc=0., scale=1.)
    
        ## Step B: simulate movement
        #repeat for leapfrog_steps-1 times
        p_step = np.copy(p_curr)
        q_step = np.copy(q_curr)
        for step in range(leapfrog_steps):
            #set value for u_fun
            u_fun.change_val({'u':q_step[0]})
            u_eval = u_fun.evaluate('f')
            #half-step update for momentum
            p_step = p_step - step_size/2*np.asarray(list(u_eval['partial_derivatives'].values()))

            #full-step update for potential
            q_step = q_step + step_size*p_step

            #set value for u_fun
            u_fun.change_val({'u':q_step[0]})
            u_eval = u_fun.evaluate('f')
            #half-step update for momentum
            p_step = p_step - step_size/2*np.asarray(list(u_eval['partial_derivatives'].values()))
            
        ## Step C: Reverse momentum
        p_step = -p_step
        
        ## Step D: Correction for simulation error
        #compute total energy at current and step
        h_curr = ue_curr + 0.5 * np.linalg.norm(p_curr) ** 2
        h_step = u_energy(q_step) + 0.5 * np.linalg.norm(p_step) ** 2
        #generate alpha
        alpha = min(1, (np.exp(h_curr - h_step)))
        #sample from uniform
        u = np.random.uniform()
        #MH step
        if u <= alpha:
            #accept
            q_curr = q_step
            ue_curr = u_energy(q_curr)
            ap += 1
        #append whatever is current
        samples.append(q_curr)
    
    #convert samples to numpy array
    samples = np.asarray(samples)
    #print acceptance rate
    print(f'The acceptance rate is {ap/total_samples:0.3f}')
    # Burning and thinning
    return samples[round(burn_in*len(samples))::thinning_factor, :]