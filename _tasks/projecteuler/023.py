import utils

# Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
# it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers

MAX_N = 28123

primes = [p for _, p in zip(range(MAX_N), utils.primes_generator())]
primes = [p for p in primes if p <= MAX_N]

abundants = []
for i in range(1, MAX_N+1):
    # is "i" abundant?
    pd = utils.get_proper_divisors(primes, i)
    if sum(pd) > i:
        abundants.append(i)

# all sums
abundants_set = set(abundants)
sums = set()
for n in range(1, MAX_N+1):
    if n % 1000 == 0:
        print(n)
    if n not in sums:
        for a in abundants:
            na = n - a
            if na in sums or na in abundants_set:
                sums.add(n)
            if a > n:
                break

# sums of 2
sums = set()
for a in abundants:
    for b in abundants:
        sums.add(a+b)

vals = [i for i in range(1, MAX_N+1) if i not in sums]
print(f'{vals[:5]=} {vals[-5:]=} {len(vals)=}')
print(f'{sum(vals)=}')
