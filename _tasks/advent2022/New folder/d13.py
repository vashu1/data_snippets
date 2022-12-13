from utils import *
from collections import defaultdict, Counter, deque
import json
import functools

input_test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
input_test = input_test.split('\n')

input_full = open('d13.txt').readlines()


input = [l.strip() for l in input_full]

def _cmp_int(l, r):
    if l == r:
        return 0
    return 1 if l < r else -1


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return _cmp_int(left, right)
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    else:  # both lists
        # compare the first value of each list, then the second value, and so on.
        # If the left list runs out of items first, the inputs are in the right order.
        # If the right list runs out of items first, the inputs are not in the right order.
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        for l, r in zip(left, right):
            r = compare(l, r)
            if r != 0:
                return r
        if len(left) != len(right):
            return 1 if len(left) < len(right) else -1
        return 0

vals = []
indx = 0
while indx + 1 < len(input):
    l, r = json.loads(input[indx]), json.loads(input[indx+1])
    res = compare(l, r)
    assert res != 0
    if res > 0:
        vals.append((indx+3)//3)
    indx += 3

print(sum(vals))

# PART II

d1 = [[2]]
d2 = [[6]]
packets = [json.loads(l) for l in input if l]
assert d1 not in packets
assert d2 not in packets
packets.append(d1)
packets.append(d2)
packets = list(sorted(packets, key=functools.cmp_to_key(compare), reverse=True))
a1 = packets.index(d1) + 1
a2 = packets.index(d2) + 1
print(a1 * a2)