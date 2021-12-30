# Find the sum of all the primes below two million.

N = 2_000_000

primes = __import__("007_primes_generator")
primes_sum = 0
for p in primes.primes_generator():
    if p >= N:
        break
    primes_sum += p

print(primes_sum)