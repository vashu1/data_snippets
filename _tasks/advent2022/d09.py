from utils import *

input_test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split('\n')

input_full = open('d09.txt').readlines()

input = [line.strip() for line in input_full]


def move_head(cmd, h):
    if cmd == 'U':
        return (h[0], h[1]+1)
    elif cmd == 'D':
        return (h[0], h[1]-1)
    elif cmd == 'L':
        return (h[0]-1, h[1])
    elif cmd == 'R':
        return (h[0]+1, h[1])
    else:
        assert False


def pull_tail(h, t):
    dx_ = t[0] - h[0]
    dy_ = t[1] - h[1]
    dx = abs(dx_)
    dy = abs(dy_)
    if dx > 1 or dy > 1:
        if dx == 0:
            return (t[0], t[1] - dy_ // 2)
        elif dy == 0:
            return (t[0] - dx_ // 2, t[1])
        else:
            dx_ = -1 if dx_ < 0 else 1
            dy_ = -1 if dy_ < 0 else 1
            return (t[0] - dx_, t[1] - dy_)
    return t


assert pull_tail((0, 0), (0,2)) == (0, 1)
assert pull_tail((0, 0), (1,2)) == (0, 1)
assert pull_tail((0, 0), (2,2)) == (1, 1)

h = (0,0)
t = (0,0)
positions = [t]
for line in input:
    cmd, cnt = line.split(' ')
    cnt = int(cnt)
    for _ in range(cnt):
        h = move_head(cmd, h)
        t = pull_tail(h, t)
        positions.append(t)

print(len(set(positions)))

ROPE_LEN = 10
rope = [(0,0)] * ROPE_LEN
positions = [rope[-1]]
for line in input:
    cmd, cnt = line.split(' ')
    cnt = int(cnt)
    for _ in range(cnt):
        rope[0] = move_head(cmd, rope[0])
        for i in range(ROPE_LEN - 1):
            rope[i+1] = pull_tail(rope[i], rope[i+1])
        positions.append(rope[-1])

print(len(set(positions)))