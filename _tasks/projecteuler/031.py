# There are eight coins in general circulation:
#
# 1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
# It is possible to make £2 in the following way:
#
# 1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
# How many different ways can £2 be made using any number of coins?

from collections import Counter

VALUE = 200

coins = [1, 2, 5, 10, 20, 50, 100, 200]
sums = Counter()
for coin in coins:
    extra = Counter()
    c = 1
    while c*coin <= VALUE:
        for sum in range(1, VALUE + 1):
            if c*coin == sum:
                extra[sum] += 1
            else:
                if sum - c*coin in sums:
                    extra[sum] += sums[sum - c*coin]
        c += 1
    for v in extra:
        sums[v] += extra[v]

print(sums[VALUE])