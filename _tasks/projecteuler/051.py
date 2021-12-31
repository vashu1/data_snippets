import utils

MAX_N = 100_000
primes = [p for _, p in zip(range(MAX_N), utils.primes_generator())]
max_primes = max(primes)
assert max_primes > 1_000_000

max_c = 7
for d in [1,2]:
    print(f'{d=}')
    for p in primes:
        if str(d) in str(p):
            mask = [c==str(d) for c in str(p)]
            c = 0
            for d2 in range(10):
                if int(str(p).replace(str(d), str(d2))) in primes:
                    c += 1
                if c >= max_c:
                    max_c = c
                    print(f'{c=} {p=}')
                #for enumerate(str(p))

p = 121313
d = 1
for d2 in range(10):
    pp =str(p).replace(str(d), str(d2))
    print(f'{pp=} {int(pp) in primes}')