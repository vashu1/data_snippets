from utils import *

input_test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
input_test = input_test.split('\n')

input_full = open('d14.txt').readlines()

parse = lambda vals: (int(vals.split(',')[0]), int(vals.split(',')[1]))

vals = [line.split(' -> ') for line in input_full]
vals = flatten(vals)
vals = lmap(parse, vals)
xs, ys = zip(*vals)
print(f'{min(xs)=} {max(xs)=} {min(ys)=} {max(ys)=}')
# min(xs)=473 max(xs)=578 min(ys)=14 max(ys)=161

floor = max(ys) + 2

input = [l.strip() for l in input_full]

# The sand is pouring into the cave from point 500,0
# If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead
# move diagonally one step down and to the left
# If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right

caves = [[0 for _ in range(1_000)] for _ in range(200)]

cc = 0
def add_sand():
    def can_fall(x, y):
        return caves[y+1][x] == 0 or caves[y+1][x-1] == 0 or caves[y+1][x+1] == 0
    global cc
    x, y = 500, 0
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
    assert x != 500 or y != 0
    #print(x, y)
    caves[y][x] = 1