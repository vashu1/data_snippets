'''

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

'''
import numpy as np

N = 20
primes = []
for i in range(2, N+1):
    if not [p for p in primes if i%p==0]:
        primes.append(i)

v = np.prod(primes)
vals = [v*(2**p2)*(3**p3) for p2 in range(4) for p3 in range(2)]
vals = [v for v in vals if all([v%n==0 for n in range(2, N+1)])]
vals.sort()

print(vals[0])