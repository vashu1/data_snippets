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

if __name__ == '__main__':
    print(vals[0])

# TRY 2

def power(n, p):
    res = 0
    while n % p == 0:
        n //= p
        res += 1
    return res

factors = lambda n: [power(n, p) for p in primes]
factors_matrix = np.array([factors(n) for n in range(1, N+1)])
factors_max = np.max(factors_matrix, axis=0)

if __name__ == '__main__':
    print(np.prod([p**n for p, n in  zip(primes, factors_max)]))