SZ = 1_000
grid = [[0]*SZ for _ in range(SZ)]


def flatten(lst):
    return [item for sublist in lst for item in sublist]


for line in open('d06.txt').readlines():
    #print(line)
    line = line.strip()
    s, _, e = line.split(' ')[-3:]
    x1, y1 = list(map(int, s.split(',')))
    x2, y2 = list(map(int, e.split(',')))
    assert x1 <= x2
    assert y1 <= y2
    """ # part 1
    if line.startswith('toggle'):
        f = lambda x: 0 if x else 1
    elif line.startswith('turn off'):
        f = lambda _: 0
    elif line.startswith('turn on'):
        f = lambda _: 1
    """
    if line.startswith('toggle'):
        f = lambda x: x + 2
    elif line.startswith('turn off'):
        f = lambda x: max(0, x - 1)
    elif line.startswith('turn on'):
        f = lambda x: x + 1
    else:
        assert False
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            grid[y][x] = f(grid[y][x])

print(sum(flatten(grid)))