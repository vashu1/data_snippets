from collections import defaultdict
import numpy as np
import itertools

def flatten(lst):
    return list(itertools.chain(*lst))

def all_combinations(ps):
    return flatten(itertools.chain([itertools.combinations(ps,i) for i in range(1, len(ps))]))

N = 10_000

oo5 = __import__("005")
oo7 = __import__("007_primes_generator")
primes = [p for _, p in zip(range(N//2), oo7.primes_generator())]
primes = [p for p in primes if p < N]

def get_proper_divisors_sum(n):
    factors = [[p] * oo5.power(n, p) for p in primes if oo5.power(n, p) > 0]
    factors = flatten(factors)
    divisors = [np.prod(ps) for ps in all_combinations(factors)]
    divisors = set(divisors)
    return sum(divisors) + 1

assert get_proper_divisors_sum(284) == 220
assert get_proper_divisors_sum(220) == 284

sum_divisors = defaultdict(set)
for n in range(2, N+1):
    proper_divisors_sum = get_proper_divisors_sum(n)
    sum_divisors[proper_divisors_sum].add(n)


result = 0
for s in list(sum_divisors.keys()):
    for n in sum_divisors[s]:
        if s > n:
            if s in sum_divisors[n]:
                print(s, n)
                result += s + n

print(result)
