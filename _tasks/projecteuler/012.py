import numpy as np

oo7 = __import__("007_primes_generator")
primes = [p for _, p in zip(range(1_000), oo7.primes_generator())]

oo5 = __import__("005")


triangle = 0
n = 1
while True:
    triangle += n
    n += 1
    factors = lambda n: [oo5.power(n, p) for p in primes]
    factor_count = np.prod(np.array(factors(triangle)) + 1)
    if factor_count > 500:
        print(triangle)
        break
