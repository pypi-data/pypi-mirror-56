"""Example from Quick Start guide in docs"""

import pyscannerbit.scan as sb

# And some other stuff for use in this example
import numpy as np
import math
import matplotlib.pyplot as plt

# Test function
def rastrigin(scan,x,y,z):
    X = [x,y,z]
    A = 10
    scan.print("x+y+z",x+y+x) # Send extra results to output file.
    return - (A + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X]))

# Prior transformation from unit hypercube
def prior(vec, map):
    map["x"] = -4 + 8*vec[0] # flat prior over [-4,4]
    map["y"] = -4 + 8*vec[1]
    map["z"] = -4 + 8*vec[2]

twalk_options = {"sqrtR": 1.05}

myscan = sb.Scan(rastrigin, prior_func=prior, scanner="twalk", scanner_options=twalk_options)
myscan.scan()

results = myscan.get_hdf5()
results.make_plot("x", "y") # Simple scatter plot of samples

fig = plt.figure()
ax = fig.add_subplot(111)
results.plot_profile_likelihood(ax,"x","y") # Profile likelihood
fig.savefig("x_y_prof_like.png")

 



