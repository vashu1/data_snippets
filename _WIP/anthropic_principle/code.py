# pip3 install mpmath
import mpmath as mp
import matplotlib.pyplot as plt
mp.dps = 10000 # big overshot

# arbitrary-precision    standard library - decimal    also mpmath   also gmpy and PyGMP

"""

Romberg algorithm   evently spaced interation

If it is possible to evaluate the integrand at unequally spaced points, then other methods such as Gaussian
 quadrature and Clenshaw–Curtis quadrature are generally more accurate. 

# https://en.wikipedia.org/wiki/Product_distribution#Uniformly_distributed_independent_random_variables
from sympy import init_printing, integrate, Symbol, exp, cos, erf, log, oo
import numpy as np
init_printing()
z = Symbol('z')
n = 21  # 22 does not work
nf = np.prod(range(1,n)) # (n-1)!
f = (-log(z))**(n-1) / nf
integrate(f, z)
integrate(f, (z,0,1))

PROB = 1e-12
for n in range(1, 30+1):  # 21
    z = Symbol('z')
    nf = np.prod(range(1,n)) # (n-1)!
    f = (-log(z))**(n-1) / nf
    print(n, integrate(f, (z, PROB, 1)) / integrate(f, (z,0,PROB)))

>>> integrate(f, (z,0,1))
1

???
n=50
>>> integrate(f, (z,0,1))
298076041230456389198917069229231362782919921875
────────────────────────────────────────────────
                      4307    

def a(n):
    nf = np.prod(range(1,n)) # (n-1)!
    f = (-log(z))**(n-1) / nf
    return integrate(f, (z,0,1))

for n in range(1,30):
    print(n, a(n))
"""

def n_dim_sphere_volume(r, n): # change of order */ to /* does not change precision much
    return mp.power(mp.pi, n/2.0) * mp.power(r, n) / mp.gamma(n/2.0 + 1)

n_dim_sphere_volume(1,100)
n_dim_sphere_volume(1,333)
n_dim_sphere_volume(1,1000) # e-886

def prob(fc):
    probabilities = [mp.mpf(random.random()) for factor_count in range(1,fc)]
    return mp.nprod(lambda x: probabilities[int(x)], (0, len(probabilities)-1))

prob(100)
prob(333)
prob(1000)

f = lambda n, z: mp.power(-mp.log(z), n-1) / mp.factorial(n-1)

#TODO generator
points = [mp.mpf(0.5)]
count = int(2e4)
factor = 0.9
for i in range(count):
    points.append(points[-1]*factor)

# print(points[-1]) # 3.54126796586135e-916