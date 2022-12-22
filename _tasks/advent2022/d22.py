from utils import *


def turn_cube(m):  # rotate cube
    global cube
    if m == 'D':
        turn_cube('U')
        turn_cube('U')
        turn_cube('U')
        return
    elif m == 'U':
        s0, s1, s2, s3, s4, s5 = cube
        s0 = rotate_cc(s0, 2)
        s3 = rotate_cc(s3, 2)
        s2 = rotate_cc(s2, 1)
        s4 = rotate_cc(s4, 3)
        s3, s0, s2, s5, s4, s1 = s0, s1, s2, s3, s4, s5
    elif m == 'L':
        s0, s1, s2, s3, s4, s5 = cube
        s0 = rotate_cc(s0, 1)
        s1 = rotate_cc(s1, 1)
        s2 = rotate_cc(s2, 1)
        s3 = rotate_cc(s3, 3)
        s4 = rotate_cc(s4, 1)
        s5 = rotate_cc(s5, 1)
        s2, s1, s5, s3, s0, s4 = s0, s1, s2, s3, s4, s5
    elif m == 'R':
        turn_cube('L')
        turn_cube('L')
        turn_cube('L')
        return
    else:
        assert False
    cube = [s0, s1, s2, s3, s4, s5]


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


def rotate_cc(side, cnt):  # rotate side counter-clockwise
    assert 0 < cnt < 4
    for _ in range(cnt):
        s, revolutions, start, i = side
        res = []
        for i in range(SZ):
            res.append(''.join([s[j][SZ - 1 - i] for j in range(SZ)]))
        side = res, revolutions + 1, start, i
    return side


cube = []
side_start = []
s = 0
i = 0
while input[i]:
    sides = len(input[i].strip()) // SZ
    if not sides:
        break
    #print(f'{sides=}')
    for z in range(sides):
        ss = min(input[i].index('.'), input[i].index('#'))
        side_start.append((ss + z*SZ, i))
        cube.append([])
        for j in range(i, i + SZ):
            line = input[j].strip()
            cube[s].append(line[z*SZ:(z+1)*SZ])
        s += 1
    i += SZ


# repack
cube = [(side, 0, start, i) for i, (side, start) in enumerate(zip(cube, side_start))]

# reorder
def reorder():
    global cube
    s0, s1, s2, s3, s4, s5 = cube
    if len(input) < 50:
        """
      0
    321
      54
        """
        s0, s3, s2, s1, s5, s4 = s0, s1, s2, s3, s4, s5
        s4 = rotate_cc(s4, 1)
    else:
        """
  3
 204
  1
        
   04
   1
  25
  3
        """
        s0, s4, s1, s2, s5, s3 = s0, s1, s2, s3, s4, s5
        s2 = rotate_cc(s2, 3)
        s3 = rotate_cc(s3, 3)
        s4 = rotate_cc(s4, 3)
    cube = [s0, s1, s2, s3, s4, s5]

reorder()

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



directions = [(0,-1), (1,0), (0,1), (-1,0)]
def turn(direction, i):
    global directions
    indx = directions.index(direction)
    if i == 'L':
        indx -= 1
    elif i =='R':
        indx += 1
    else:
        assert False
    return directions[indx % len(directions)]

position = (0, 0)
direction = (1, 0)

cube_reverts = {
    'U': 'D',
    'D': 'U',
    'L': 'R',
    'R': 'L',
}
def cube_step(position, direction, steps):
    def ok(coord):
        return 0 <= coord < SZ
    global cube
    x, y = position
    i, j = direction
    while steps > 0:
        cube_turn = None
        saved = (x, y), (i, j)
        steps -= 1
        x += i
        y += j
        # turn and mod
        if x < 0 and ok(y):
            i, j = -1, 0
            cube_turn = 'R'
            x = SZ - 1
        elif x >= SZ and ok(y):
            i, j = 1, 0
            cube_turn = 'L'
            x = 0
        elif y < 0 and ok(x):
            i, j = 0, -1
            cube_turn = 'D'
            y = SZ - 1
        elif y >= SZ and ok(x):
            i, j = 0, 1
            cube_turn = 'U'
            y = 0
        else:
            assert ok(x) and ok(x)
        if cube_turn:
            turn_cube(cube_turn)
        if cube[0][0][y][x] == '#':
            if cube_turn:
                turn_cube(cube_reverts[cube_turn])
            return saved
        else:
            assert cube[0][0][y][x] == '.'
    return (x, y), (i, j)


for i in path:
    if isinstance(i, int):
        position, direction = cube_step(position, direction, i)
    else:
        direction = turn(direction, i)




def rotate_cc_position(position):
    x, y = position
    x_ = y
    y_ = SZ - 1 - x
    return x_, y_





while cube[0][1] % 4 != 0:  # recover cube side positions
    print('FINAL TURN')
    cube[0] = rotate_cc(cube[0], 1)
    position = rotate_cc_position(position)
    direction = turn(direction, 'L')

side, turns, start, i = cube[0]




x, y = position
x += start[0]
y += start[1]
position = x, y


# The final password is the sum of 1000 times the row, 4 times the column, and the facing.
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
r = None
if direction == (1, 0):
    r = 0
elif direction == (0, 1):
    r = 1
elif direction == (-1, 0):
    r = 2
elif direction == (0, -1):
    r = 3
else:
    assert False
r += 1000 * (position[1] + 1) + 4 * (position[0] + 1)
print(r)
print('-')
# 2036 - bad

# Part I

"""
directions = [(0,-1), (1,0), (0,1), (-1,0)]
def turn(direction, i):
    global directions
    indx = directions.index(direction)
    if i == 'L':
        indx -= 1
    elif i =='R':
        indx += 1
    else:
        assert False
    print('turn', i, direction, directions[indx % len(directions)])
    return directions[indx % len(directions)]


def step(position, direction):
    x, y = position
    i, j = direction
    while True:
        x += i
        y += j
        x %= len(cave[0])
        y %= len(cave)
        print(x, y)
        if cave[y][x] == '.':
            return x, y
        if cave[y][x] == '#':
            return position


for line in [line for line in input]:
    line = ''.join([i for i in line if i in [' ','.','#']])
    cave.append(line)
    if not line:
        break


width = max([len(l) for l in cave])
for i in range(len(cave)):
    cave[i] = cave[i] + (' '*(width - len(cave[i])))

position = (cave[0].index('.'), 0)
direction = (1, 0)

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

print(path)

for i in path:
    print(i)
    if isinstance(i, int):
        while i > 0:
            position = step(position, direction)
            i -= 1
    else:
        direction = turn(direction, i)
    print('------', position, direction)

print(position)
print(direction)

# The final password is the sum of 1000 times the row, 4 times the column, and the facing.
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
r = None
if direction == (1,0):
    r = 0
elif direction == (0,1):
    r = 1
elif  direction == (-1,0):
    r = 2
elif direction == (0,-1):
    r = 3
else:
    assert  False
r += 1000 * (position[1] + 1) + 4 * (position[0] + 1)
print(r)

"""