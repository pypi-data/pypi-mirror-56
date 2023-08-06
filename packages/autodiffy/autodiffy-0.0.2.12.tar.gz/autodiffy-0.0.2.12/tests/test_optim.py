import numpy as np
from autodiffy.optim import *

def test_optim():
    threshold = 1e-12

    # test 2-dimensional Newton-Rhapson
    assert np.linalg.norm(newton_rhapson(lambda x,y: x ** 2 + y**2, 2, [-1., -1.])[-1] - np.asarray([0., 0.])) < threshold

    # test 2-dimensional gradient descent
    assert np.linalg.norm(gradient_descent(lambda x,y: x ** 2 + y**2, 2, [-1., -1.], 1e-2)[-1] - np.asarray([-3.41321027e-09, -3.41321027e-09])) < threshold

    # test HMC using unit root of a normal pdf
    threshold = 1e-1
    def target_energy(x):
        return -np.log(target_pdf(x))

    def target_pdf(x):
        return 1 / np.sqrt(2*np.pi) * np.exp(-0.5*(x)**2)

    #define other parameters
    params = {'u_energy': target_energy,
        'step_size':1.5, 
        'leapfrog_steps':10, 
        'total_samples':5000, 
        'burn_in':.2, 
        'thinning_factor':2,
        'position_init': np.asarray([-10])}

    #it's HMC time
    my_samples = hmc_sampler(**params)

    # check that the mean and sd are close to 0 and 1
    assert np.mean(my_samples) < threshold
    assert np.std(my_samples) - 1 < threshold
