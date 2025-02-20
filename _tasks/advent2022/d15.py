import portion as P
from collections import defaultdict

input_test = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
input_test = input_test.split('\n')

input_full = open('d15.txt').readlines()

input = [l.strip() for l in input_full]


def parse(l):
    _, l = l.split('x=')
    x, y = l.split(', y=')
    return int(x), int(y)

data = []
for line in input:
    s, b = line.split(': ')
    data.append((parse(s),parse(b)))

drop_sm_helper = defaultdict(set)
for (sx, sy), (bx, by) in data:
    for x, y in [(sx, sy), (bx, by)]:
        drop_sm_helper[y].add(x)

def impossible_posistions(row_y, drop_sm=True):
    positions = P.empty()
    for (sx, sy), (bx, by) in data:
        distance_to_beacon = abs(sx - bx) + abs(sy - by)
        distance_to_row = abs(sy - row_y)
        if distance_to_row <= distance_to_beacon:
            half_width = distance_to_beacon - distance_to_row
            middle = sx
            a = middle - half_width
            b = middle + half_width
            positions = positions.union(P.closed(a, b))

    if drop_sm:
        for x in drop_sm_helper[row_y]:
            positions = positions.difference(P.singleton(x))

    return positions


def interval_len(interval):
    x1, x2 = interval.lower, interval.upper
    res = x2 - x1 + 1
    if interval.left == P.OPEN:
        res -= 1
    if interval.right == P.OPEN:
        res -= 1
    return res


print(sum([interval_len(i) for i in impossible_posistions(2000000)]))  # 10  2000000

# PART II

# distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

"""
to walk outside the perimeter of the diamonds and find the single point not contained in any of them
"""
import time
import random
t = time.time()
print_flag = False
for (sx, sy), (bx, by) in data:
    print((sx, sy), (bx, by))
    distance_to_beacon = abs(sx - bx) + abs(sy - by)
    for i in range(distance_to_beacon + 2):
        dx, dy = i, distance_to_beacon + 1 - i
        for cx in [-1, 1]:
            for cy in [-1, 1]:
                x, y = sx + cx * dx, sy + cy * dy
                if x not in range(4000000 + 1) or y not in range(4000000 + 1):
                    continue
                print_flag = True
                for (sx1, sy1), (bx1, by1) in data:
                    d1 = abs(sx1 - bx1) + abs(sy1 - by1)
                    d2 = abs(sx1 - x) + abs(sy1 - y)
                    if d2 <= d1:
                        print_flag = False
                        break
                if print_flag:
                    print(x, y)
                    break
            if print_flag:
                break
        if print_flag:
            break
    if print_flag:
        break

print('time', time.time() - t)
# or reuse part 1

mx, my = 20, 20
mx, my = 4000000, 4000000

c = 0
for y in range(0, my+1):
    c += 1
    if c % 100_000 == 0:
        #print(c)
        pass
    ps = impossible_posistions(y, drop_sm=False)
    ps = P.closed(0, mx).difference(ps)
    if not ps.empty:
        print(y, ps)  # 3042458 [3012821]
        x = ps.lower
        print(x * 4000000 + y)  # by multiplying its x coordinate by 4000000 and then adding its y coordinate.
