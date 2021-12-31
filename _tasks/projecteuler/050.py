# Which prime, below one-million, can be written as the sum of the most consecutive primes?
import utils

MAX_N = 100_000
primes = [p for _, p in zip(range(MAX_N), utils.primes_generator())]
max_primes = max(primes)
assert max_primes > 1_000_000
primes = [p for p in primes if p < 1_000_000]


primes_set = set(primes)

max_l = 150
max_prime = 0
for i in range(len(primes)):
    if i%100==0:
        print(i)
    if i*max_l > max_primes:
        break
    for l in range(max_l, 999):
        if i + l >= len(primes):
            break
        if sum(primes[i:i+l]) in primes_set:
            if l > max_l:
                max_l = l
                max_prime = sum(primes[i:i+l])
                print(f'{sum(primes[i:i+l])=} {i=} {l=} {primes[i:i+l]=}')


print(f'{max_l=} {max_prime=}')