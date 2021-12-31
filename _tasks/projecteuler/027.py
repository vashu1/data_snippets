import utils

MAX_N = 300_000
primes = [p for _, p in zip(range(MAX_N), utils.primes_generator())]
primes = set(primes)
max_primes = max(primes)

def try_ab(a, b, n=0):
    while (n**2 + a*n + b) in primes:
        if (n**2 + a*n + b) > max_primes:
            print(f'BAD {n=} {a=} {b=}')
        n += 1
    return n

# b is prime
coeff_b = [-c for c in primes if c <= 1000] + [c for c in primes if c <= 1000]
# n = 1 -> 1+a+b is prime
coeff_a = set([a for a in range(-1000+1, 1000) for b in coeff_b if a + b + 1 in primes])

vals = []
for a in coeff_a:
    for b in coeff_b:
        if 4+2*a+b in primes:  # n=2   4+2a+b is prime?
            vals.append((a, b, try_ab(a, b, n=3)))

vals.sort(key=lambda v:v[2])
a,b,n = vals[-1]
print(f'{a=} {b=} {n=}')
print(f'{a*b=}')