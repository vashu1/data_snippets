from utils import *
from collections import defaultdict, Counter, deque

input_test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
input_test = input_test.split('\n')

input_full = open('d14.txt').readlines()

parse = lambda vals: (int(vals.split(',')[0]) - 300, int(vals.split(',')[1]))
min_x = min_y = 1_000_000
max_x = max_y = -1_000_000
for i in input_full:
    for c in i.split(' -> '):
        x, y = parse(c)
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

print(f'{min_x=} {max_x=} {min_y=} {max_y=}')
# min_x=473 max_x=578 min_y=14 max_y=161
floor = max_y + 2

input = [l.strip() for l in input_full]

# The sand is pouring into the cave from point 500,0
# If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead
# move diagonally one step down and to the left
# If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right

caves = [[0 for _ in range(400)] for _ in range(200)]

cc = 0
def add_sand():
    def can_fall(x, y):
        return caves[y+1][x] == 0 or caves[y+1][x-1] == 0 or caves[y+1][x+1] == 0
    global cc
    x, y = 500-300, 0
    if not can_fall(x, y):
        print(cc+1)
        exit(0)
    while can_fall(x, y):
        if y > 200-3:
            print('first', c)
            exit(0)
        if caves[y+1][x] == 0:
            y += 1
        elif caves[y+1][x-1] == 0:
            y += 1
            x -= 1
        elif caves[y+1][x+1] == 0:
            y += 1
            x += 1
    cc += 1
    return x, y

for line in input:
    coords = [parse(vals) for vals in line.split(' -> ')]
    for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
        assert x1 == x2 or y1 == y2
        if x1 == x2:
            y_, y__ = (y1, y2) if y1 < y2 else (y2, y1)
            for y in range(y_, y__+1):
                caves[y][x1] = -1
        if y1 == y2:
            x_, x__ = (x1, x2) if x1 < x2 else (x2, x1)
            for x in range(x_, x__+1):
                caves[y1][x] = -1

# floor
for i in range(len(caves[0])):
    caves[floor][i] = -1

while True:
    x, y = add_sand()
    assert x != 500-300 or y != 0
    #print(x, y)
    caves[y][x] = 1