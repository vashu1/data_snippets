from collections import defaultdict, Counter
import math
import os

weights = []
remaining = []

# part 1 - set to 3
# part 2 - set to 4
N_GROUPS = 4

test = '\n'.join([str(i) for i in list(range(1, 5+1)) + list(range(7, 11+1))])

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    weights.append(int(line))

weights.sort(reverse=True)
remaining = [sum(weights[i:]) for i in range(len(weights))] + [0]
target_weight = remaining[0] // N_GROUPS
assert len(weights) == len(set(weights))

# three groups of exactly the same weight

# The first group - the one going in the passenger compartment - needs as few packages as possible
# so that Santa has some legroom left over.

# the first group has the smallest quantum entanglement to reduce the chance of any "complications".
# The quantum entanglement of a group of packages is the product of their weights


def is_better(best, new_one):
    if best is None:
        return True
    if len(best[0]) > len(new_one[0]):
        return True
    if math.prod(best[0][:-1]) > math.prod(new_one[0][:-1]):
        return True
    return False


c = c1 = 0
best = None
current = [[target_weight] for _ in range(N_GROUPS)]
visited2 = set()

def split(current, index):
    global c, c1, best, visited2
    c += 1
    if c %10000 == 0:
        print(f'{c=} {c1=} {len(visited2)=} {math.prod(best[0][:-1])=}')
    if index == len(weights):
        c1 += 1
        if is_better(best, current):
            best = [list(c) for c in current]  #TODO
            print(best)
        return
    cw = weights[index]
    for i in range(len(current)):
        old_sum = current[i][-1]
        if old_sum < cw:
            continue
        current[i][-1] = cw
        current[i].append(old_sum - cw)
        k0 = len(current[0])
        #if best and len(current[0]) > len(best[0]):
        #    continue
        k00 = math.prod(current[0][:-1])
        #if best and k0 == len(best[0]):
        #    if k00 > math.prod(best[0][:-1]):
        #        continue
        k = tuple([k0, k00, current[0][-1]] + list(sorted([c[-1] for c in current[1:]])))
        if k not in visited2:
            split(current, index + 1)
            visited2.add(k)
        current[i].pop()
        current[i][-1] = old_sum

split(current, 0)
print(best)
print(c, c1)
print(math.prod(best[0][:-1]))
