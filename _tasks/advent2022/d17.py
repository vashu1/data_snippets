from utils import *
from collections import defaultdict, Counter, deque

rock_index = 0
rocks = ["""####""",

""".#.
###
.#.""",

"""..#
..#
###""",

"""#
#
#
#""",

"""##
##"""]
for i in range(len(rocks)):
    rocks[i] = list(reversed([l.strip() for l in rocks[i].split('\n')]))

def get_rock():
    global rocks, rock_index
    res = rocks[rock_index]
    rock_index += 1
    rock_index %= len(rocks)
    return res

input_test = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
input_test = input_test.split('\n')

# chamber is exactly seven units wide
# Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three
# units above the highest rock in the room (or the floor, if there isn't one).

input_full = open('d17.txt').readlines()

floor = 0
input_indx = 0
input = [l.strip() for l in input_full]
input = input[0]

cave = [['.' for _ in range(7)] for _ in range(1_000_000)]


def get_wind():
    global input, input_indx
    res = input[input_indx]
    input_indx += 1
    input_indx %= len(input)
    if res == '<':
        res = -1
    elif res == '>':
        res = +1
    else:
        assert False
    return res


def start_position():
    global floor, cave
    for i in range(7):
        if cave[floor][i] != '.':
            floor += 1
            return start_position()
    return 2, floor + 3


def check_rock(rock, x, y):
    #print('\n'.join(reversed(rock)))
    # check walls
    if y < 0:
        return False
    if x < 0 or x + len(rock[0]) > 7:
        return False
    # check other rocks
    global cave
    for ry, row in enumerate(rock):
        for rx, ch in enumerate(row):
            if ch == '#':
                #print(f'{x=} {y=} {rx=} {ry=}')
                if cave[y + ry][x + rx] == '#':
                    return False
    return True


def put_rock(rock, x, y):
    global cave
    for ry, row in enumerate(rock):
        for rx, ch in enumerate(row):
            if ch == '#':
                cave[y + ry][x + rx] = '#'


def add_rock():
    x, y = start_position()
    rock = get_rock()
    while True:
        # wind
        dx = get_wind()
        if check_rock(rock, x + dx, y):
            x += dx
        # down
        if check_rock(rock, x, y - 1):
            y -= 1
        else:
            put_rock(rock, x, y)
            return


def show_cave():  # add_rock() ; show_cave() ; print(start_position())
    height = 20
    for y in range(height+1):
        print(''.join(cave[height-y]))


#for _ in range(2022):
#    add_rock()
#_, y = start_position()
#print(y - 3)

# PART II

steps = 1000000000000
l = []
for _ in range(1745):  # 30 1745
    add_rock()

_, y = start_position()
l.append(y)

for _ in range(10):
    for _ in range(1745):  # 35  1745
        add_rock()

    _, y = start_position()
    l.append(y)

for _ in range((steps-0)%1745):
    add_rock()

_, y = start_position()
l.append(y)

print([j - i for i, j in zip(l, l[1:])])
print(l)

b2 = l[-1] - l[-2]
print(b2)
b = l[0]+ (l[1]-l[0])*((steps-1745)//1745) + b2 - 3
print(b)#, b - 1514285714288)
exit(0)
#30 35 35
#54 53 53

# 1745 1745
#

a = (steps - 0)
print(a//1745, a%1745)
b = 0 + (a//1745) * 2767 + 1593
b -= 3
print(b, b-1514285714288)
exit(1)


#print(len(input_test[0]), len(input_full[0]))
# 40 10091




c = 0
for _ in range(30):
    c += 1
    add_rock()

counts = defaultdict(list)
states = defaultdict(list)
while True:
    _, y = start_position()
    if y+10 > len(cave):
        print('out of cave')
        print(f'{c=}')
        break
    # check no holes
    bad_state = False
    for x in range(7):
        bad = True
        for dy in range(20):
            if cave[y-dy][x] == '#':
                bad = False
        if bad:
            bad_state = True
            break
    if not bad_state:
        state = rock_index, input_indx, ''.join([''.join(cave[y-dy]) for dy in range(-4, 10)])
        states[state].append(y)
        counts[state].append(c)
        l = states[state]
        s = set([j - i for i, j in zip(l, l[1:])])
        l2 = counts[state]
        s2 = set([j - i for i, j in zip(l2, l2[1:])])
        if len(states[state]) == 10 and len(s) < 3 and len(s2) < 3:
            print(c, s, counts[state], s, s2)
            break
    c += 1
    add_rock()

exit(1)

_, y = start_position()
print(y - 3)

# [j - i for i, j in zip(l, l[1:])]

mx = 0
for i in states:
    if len(states[i]) > mx:
        l = states[i]
        print(mx, [j - i for i, j in zip(l, l[1:])])
        i = len(states[i])

c1 = 0
c2 = 0
for i in states:
    if len(states[i]) > 1:
        l = [j - i for i, j in zip(l, l[1:])]
        if len(set(l)) == 1:
            c1 += 1
        else:
            c2 += 1