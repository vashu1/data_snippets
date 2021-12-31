import numpy as np
import itertools

def power(n, p):
    res = 0
    while n % p == 0:
        n //= p
        res += 1
    return res


def primes_generator():
    primes = [2]
    yield primes[-1]
    n = 3
    while True:
        n_sqrt = int(n ** 0.5) + 1
        indx = 0
        is_prime = True
        while indx < len(primes) and primes[indx] <= n_sqrt:
            if n % primes[indx] == 0:
                is_prime = False
                break
            indx += 1
        if is_prime:
            primes.append(n)
            yield n
        n += 2


def sequence_max_prod(numbers, N):
    vals = numbers[0:0+N]
    zeroes_count = len(vals[vals == 0])
    prod = np.prod([(v if v>0 else 1) for v in vals])
    max_prod = 0 if zeroes_count else prod
    for i in range(len(numbers)-N):
        drop_v = numbers[i]
        if drop_v == 0:
            zeroes_count -= 1
            drop_v = 1
        prod //= drop_v
        add_v = numbers[i+N]
        if add_v == 0:
            zeroes_count += 1
            add_v = 1
        prod *= add_v
        if zeroes_count == 0 and prod > max_prod:
            max_prod = prod
    return max_prod


def flatten(lst):
    return list(itertools.chain(*lst))


def all_combinations(ps):
    return flatten(itertools.chain([itertools.combinations(ps,i) for i in range(1, len(ps))]))


def get_proper_divisors(primes, n):
    factors = [[p] * power(n, p) for p in primes if power(n, p) > 0]
    factors = flatten(factors)
    divisors = [np.prod(ps) for ps in all_combinations(factors)]
    #assert np.prod(divisors) == n, 'add primes'
    divisors = set(divisors)
    divisors.add(1)
    return divisors