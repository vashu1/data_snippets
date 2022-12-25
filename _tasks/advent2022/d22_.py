import numpy as np

input_test = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

input_test = input_test.split('\n')

input_full = open('d22.txt').readlines()

input = [l for l in input_full]  # input_full input_test
# 4x4  50x50
SZ = 4 if len(input) < 50 else 50


# for any point on cube return right direction vector and original input position
save = {}
def get_orientation_and_coords(p):
    return save[tuple(p)]


def on_edge(v):
    i0 = np.where(v == 0)[0]
    isz = np.where(v == SZ + 1)[0]
    return (i0.size + isz.size) > 1


def ortogonal(v):  # inside of cube, works only inside sides (returns zero on edges)
    i0 = np.where(v == 0)[0]
    isz = np.where(v == SZ + 1)[0]
    result = np.zeros((3,), dtype=int)
    if i0.size == 1:
        result[[i0[0]]] = 1
    if isz.size == 1:
        result[[isz[0]]] = -1
    return result


def turn_left(position, direction):
    return np.cross(direction, ortogonal(position))


def step(position, direction):
    new_position = position + direction
    if on_edge(new_position):  # on edge
        new_direction = ortogonal(position)
        new_position += new_direction
    else:
        new_direction = np.copy(direction)
    return new_position, new_direction


position = np.asarray((1, 1, 0))
direction = np.asarray((1, 0, 0))

cube = np.zeros((SZ + 2, SZ + 2, SZ + 2), dtype=int)

# parse cube
first_input_y = 0
first_input_x = min(input[first_input_y].index('.'), input[first_input_y].index('#'))
stack = [(first_input_x, first_input_y, np.copy(position), np.copy(direction))]
while stack:
    x, y, posv, dirv = stack.pop()
    for dx, dy, turn_back in [(1, 0, 0), (0, 1, 1), (-1, 0, 2)]:
        nx = x + dx
        ny = y + dy
        npos, ndir = step(posv, dirv)
        dirv = -turn_left(posv, dirv)  # turn right
        if cube[tuple(npos)] != 0:
            continue  # already visited
        if nx < 0 or ny < 0:
            continue
        if not input[ny]:
            continue
        if nx >= len(input[ny]):
            continue
        new_val = {
            '\n': 0,
            '\r': 0,
            ' ': 0,
            '#': -1,
            '.': 1,
        }[input[ny][nx]]
        if new_val:
            right_vec = np.copy(ndir)
            while turn_back > 0:
                right_vec = turn_left(npos, right_vec)
                turn_back -= 1
            save[tuple(npos)] = right_vec, (nx, ny)
            cube[tuple(npos)] = new_val
            stack.append((nx, ny, npos, right_vec))


# parse walking directions
path = []
acc = ''
for i in input[-1].strip():
    if i in ['L', 'R']:
        path.append(int(acc))
        acc = ''
        path.append(i)
    else:
        acc += i

if acc:
    path.append(int(acc))


# walk on cube
for i in path:
    #print('COMMAND', i)
    if isinstance(i, int):
        while i:
            new_position, new_direction = step(position, direction)
            if cube[tuple(new_position)] < 0:  # obstacle is -1
                break
            position, direction = new_position, new_direction
            #print('new pos', position, direction)
            i -= 1
    else:
        if i == 'L':
            direction = turn_left(position, direction)
        elif i == 'R':
            direction = -turn_left(position, direction)
        else:
            assert False
        #print('new dir', direction)


# The final password is the sum of 1000 times the row, 4 times the column, and the facing.
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
right_vec, (input_x, input_y) = get_orientation_and_coords(position)

r = None
if (direction == right_vec).all():
    r = 0
elif (direction == -turn_left(position, right_vec)).all():
    r = 1
elif (direction == -right_vec).all():
    r = 2
elif (direction == turn_left(position, right_vec)).all():
    r = 3
else:
    assert False
r += 1000 * (input_y + 1) + 4 * (input_x + 1)
print(r)
