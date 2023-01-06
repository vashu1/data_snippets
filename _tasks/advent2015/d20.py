import math

SZ = int(4e6)

presents = 130
elves = presents // 10  # 1 3 9
house = 9

presents = 70
house = 4 # 10 + 20 + 40

presents = 33100000
elves = presents // 10

"""
primes = [2]
for i in range(3, SZ, 2):
    mx = int(math.sqrt(i + 1) + 1)
    add = True
    for p in primes:
        if p > mx:
            break
        if i % p == 0:
            add = False
            break
    if add:
        primes.append(i)

elves = [1] + primes
print(len(elves))
"""

houses = [0] * SZ
for p in range(1, SZ):
    c = 1
    while p*c < SZ:
        houses[p*c] += p * 10
        c += 1

print(list(enumerate(houses[:10])))

for i, h in enumerate(houses):
    if h >= 33_100_000:
        print(i, h)
        break

# part 2

houses = [0] * SZ
for p in range(1, SZ):
    c = 1
    while p*c < SZ:
        houses[p*c] += p * 11
        c += 1
        if c > 50:
            break

for i, h in enumerate(houses):
    if h >= 33_100_000:
        print(i, h)
        break

"""
house = prime   will get   prime + 1
house = p1 * p2  will get   p1 + p2 + 1
house = p1^2 * p2^2     1 p1 p2 p1^2 p2^2 p1*p2 p1^2*p2 p2^2*p1  p1^2 * p2^2
"""