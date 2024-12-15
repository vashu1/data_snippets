
lines = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d15.txt').readlines()]


def robot_position():
	for y, line in enumerate(boxmap):
		for x, ch in enumerate(line):
			if ch == '@':
				return x, y


def try_move(boxmap, x, y, dx, dy):
	nx, ny = x + dx, y + dy
	if boxmap[ny][nx] == '.':
		boxmap[y][x], boxmap[ny][nx] = boxmap[ny][nx], boxmap[y][x]
		return True
	elif boxmap[ny][nx] == '#':
		return False
	else:
		assert boxmap[ny][nx] == 'O'
		if try_move(boxmap, nx, ny, dx, dy):
			return try_move(boxmap, x, y, dx, dy)
		else:
			return False


def score(boxmap):
	cnt = 0
	for y, line in enumerate(boxmap):
		for x, ch in enumerate(line):
			if ch == 'O' or ch == '[':
				cnt += 100 * y + x
	return cnt


def parse_direction(ch):
	if ch == '^':
		return 0, -1
	elif ch == 'v':
		return 0, +1
	elif ch == '>':
		return +1, 0
	elif ch == '<':
		return -1, 0
	else:
		assert False


boxmap = []
n = 0
while lines[n]:
	boxmap.append(list(lines[n]))
	n += 1

robot = robot_position()

for i in range(n, len(lines)):
	for ch in lines[i]:
		direction = parse_direction(ch)
		if try_move(boxmap, *robot, *direction):
			x, y = robot
			dx, dy = direction
			robot = x + dx, y + dy

print(score(boxmap))



# II


def replace(ch):
	if ch == '#':
		return '##'
	elif ch == 'O':
		return '[]'
	elif ch == '.':
		return '..'
	elif ch == '@':
		return '@.'
	else:
		assert False


def check_move(boxmap, x, y, dx, dy):
	nx, ny = x + dx, y + dy
	if boxmap[ny][nx] in ['[', ']']:
		if dx == 0:  # vertical move
			if boxmap[ny][nx] == '[':
				return check_move(boxmap, nx, ny, dx, dy) and check_move(boxmap, nx + 1, ny, dx, dy)
			else:
				return check_move(boxmap, nx - 1, ny, dx, dy) and check_move(boxmap, nx, ny, dx, dy)
		elif dy == 0:  # horizontal move
			nx2, ny2 = nx + dx, ny + dy
			return check_move(boxmap, nx2, ny2, dx, dy)
		else:
			assert False
	elif boxmap[ny][nx] == '#':
		return False
	elif boxmap[ny][nx] == '.':
		return True
	else:
		assert False


def do_move(boxmap, x, y, dx, dy):
	nx, ny = x + dx, y + dy
	if boxmap[ny][nx] in ['[', ']']:
		if dx == 0:  # vertical move
			if boxmap[ny][nx] == '[':
				do_move(boxmap, nx, ny, dx, dy)
				do_move(boxmap, nx + 1, ny, dx, dy)
			else:
				do_move(boxmap, nx - 1, ny, dx, dy)
				do_move(boxmap, nx, ny, dx, dy)
		elif dy == 0:  # horizontal move
			nx2, ny2 = nx + dx, ny + dy
			do_move(boxmap, nx2, ny2, dx, dy)
			do_move(boxmap, nx, ny, dx, dy)
		else:
			assert False
		do_move(boxmap, x, y, dx, dy)
	elif boxmap[ny][nx] == '.':
		boxmap[y][x], boxmap[ny][nx] = boxmap[ny][nx], boxmap[y][x]
	else:
		assert False


boxmap = []
n = 0
while lines[n]:
	line = ''.join([replace(ch) for ch in lines[n]])
	boxmap.append(list(line))
	n += 1

robot = robot_position()
for i in range(n, len(lines)):
	for ch in lines[i]:
		direction = parse_direction(ch)
		if check_move(boxmap, *robot, *direction):
			do_move(boxmap, *robot, *direction)
			x, y = robot
			dx, dy = direction
			robot = x + dx, y + dy

print(score(boxmap))
