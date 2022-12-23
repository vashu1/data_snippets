from utils import *
from collections import defaultdict, Counter, deque

ROUNDS = 10
MARGIN = 100

input_test = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

input_test_small = """.....
..##.
..#..
.....
..##.
....."""

input_test = input_test.split('\n')

input_full = open('d23.txt').readlines()

input = [l.strip() for l in input_test]  # input_full input_test

class Elf:
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    direction_index = 0

    @staticmethod
    def inc_direction_index():
        Elf.direction_index += 1
        Elf.direction_index %= len(Elf.directions)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proposed = None

    def propose(self):
        self.proposed = None
        neighbours = 0
        for xx in [-1, 0, 1]:
            for yy in [-1, 0, 1]:
                if xx == 0 and yy == 0:
                    continue
                if field[self.y+yy][self.x+xx] == '#':
                    neighbours += 1
        if neighbours == 0:
            return
        for i in range(4):
            vx, vy = Elf.directions[(Elf.direction_index + i) % 4]
            if vx == 0:
                positions = [(-1, vy), (0, vy), (+1, vy)]
            else:
                positions = [(vx, -1), (vx, 0), (vx, 1)]
            if all([field[self.y+dy][self.x+dx] == '.' for dx, dy in positions]):
                self.proposed = self.x + vx, self.y + vy
                return

    def move(self):
        if self.proposed is not None:
            field[self.y][self.x] = '.'
            self.x, self.y = self.proposed
            field[self.y][self.x] = '#'


w = len(input[0])
h = len(input)
field = []
for i in range(MARGIN):
    field.append('.' * (MARGIN * 2 + w))

for line in [line.strip() for line in input]:
    field.append('.'*MARGIN + line + '.'*MARGIN)

for i in range(MARGIN):
    field.append('.' * (MARGIN * 2 + w))

#print(len(field))
#print(set([len(i) for i in field]))

field = [list(line) for line in field]

elves = []
for y in range(len(field)):
    for x, v in enumerate(field[y]):
        if field[y][x] == '#':
            elves.append(Elf(x, y))

#print('\n'.join([''.join(f) for f in field]))

for r in range(ROUNDS):
    c = Counter()
    for elf in elves:
        elf.propose()
        if elf.proposed:
            c[elf.proposed] += 1
    for elf in elves:
        if c[elf.proposed] == 1:
            elf.move()
    #print('counter', c)
    Elf.inc_direction_index()
    #print('\n\n\nROUND', r+1)
    #print('\n'.join([''.join(f) for f in field]))


xs, ys = zip(*[(elf.x, elf.y) for elf in elves])
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
print(f'{minx=} {maxx=} {miny=} {maxy=}')
print((maxx - minx), (maxy - miny))
print((maxx - minx+1)*(maxy - miny+1) - len(elves))
# 12 11

# PART II

for r in range(ROUNDS, 1_000_000):
    xs, ys = zip(*[(elf.x, elf.y) for elf in elves])
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    print(f'{r=} {minx=} {maxx=} {miny=} {maxy=}', (maxx - minx), (maxy - miny))
    #
    c = Counter()
    for elf in elves:
        elf.propose()
        if elf.proposed:
            c[elf.proposed] += 1
    moved = False
    for elf in elves:
        if c[elf.proposed] == 1:
            elf.move()
            moved = True
    if not moved:
        print(r + 1)
        break
    #print('counter', c)
    Elf.inc_direction_index()

# 1019