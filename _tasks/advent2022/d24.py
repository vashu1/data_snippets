from collections import defaultdict
from heapq import heappush, heappop

MAX_ROUNDS = 1_000

input_test = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
input_test = input_test.split('\n')

input_full = open('d24.txt').readlines()

input = [l.strip() for l in input_full]  # input_full input_test

width, height = len(input[0]), len(input)

start = (1, 0)
end = (width - 2, height - 1)

TARGETS = [end]  # use for Part I - 3 seconds
TARGETS = [end, start, end]  # use for Part II - 8 seconds

# parse input
blizzards = []
for y in range(height):
    for x in range(width):
        if input[y][x] not in '#.':
            bliz_to_vec = {
                '^': (0, -1),
                'v': (0, 1),
                '<': (-1, 0),
                '>': (1, 0),
            }
            if x == 1 or x == width - 1:
                assert input[y][x] not in '^v'
            blizzards.append([(x, y), bliz_to_vec[input[y][x]]])

# blizzars coords at every turn
blizzard_coords = {}
for i in range(MAX_ROUNDS):
    coords = set()
    for bz in blizzards:
        (sx, sy), (dx, dy) = bz
        x = (sx - 1 + dx * i) % (width - 2) + 1
        y = (sy - 1 + dy * i) % (height - 2) + 1
        coords.add((x, y))
    blizzard_coords[i] = coords


def score(time, x, y, targets):  # remaining steps is no blizzards - using just time is 2x worse
    ex, ey = targets[0]
    steps_to_finish = ex - x + ey - y
    next_targets = 0
    for t1, t2 in zip(targets, targets[1:]):
        next_targets += abs(t2[0] - t1[0]) + abs(t2[1] - t1[1])
    return time + steps_to_finish + next_targets


# check all paths
reached = defaultdict(set)
paths = []

t = 0  # set start
sx, sy = start
heappush(paths, (score(t, sx, sy, TARGETS), t, sx, sy, TARGETS))

while True:
    _, time, x, y, targets = heappop(paths)
    new_t = time + 1
    for dx, dy in [(1,0),(0,1),(0,0),(0,-1),(-1,0)]:
        new_tagets = targets
        nx = x + dx
        ny = y + dy
        if (nx, ny) in blizzard_coords[new_t]:  # blizzard ahead
            continue
        if (nx, ny) == targets[0]:  # target reached, set new target or show result and quit
            new_tagets = list(targets[1:])
            if not new_tagets:
                print(time + 1)
                exit(1)
        if (new_t, nx, ny) in reached[len(new_tagets)]:  # we were here at this time already
            continue
        if (nx, ny) not in [start, end]:  # borders
            if nx <= 0 or nx >= width - 1:
                continue
            if ny <= 0 or ny >= height - 1:
                continue
        reached[len(new_tagets)].add((new_t, nx, ny))
        heappush(paths, (score(new_t, nx, ny, new_tagets), new_t, nx, ny, new_tagets))
