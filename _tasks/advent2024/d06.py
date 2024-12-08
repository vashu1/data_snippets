

lines = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d06.txt').readlines()]


def find_guard():
	for y, line in enumerate(lines):
		if '^' in line:
			return line.find('^'), y


def turn_right(x, y):
	return -y, x


def valid(x, y):
	if not 0 <= x < len(lines[0]):
		return False
	if not 0 <= y < len(lines):
		return False
	return True


assert turn_right(1, 0) == (0, 1)
assert turn_right(0, 1) == (-1, 0)
assert turn_right(-1, 0) == (0, -1)
assert turn_right(0, -1) == (1, 0)


d = (0, -1)  # up
x, y = start = find_guard()
lines = [list(l) for l in lines]

steps = set()
while True:
	steps.add((x, y))
	nx, ny = x + d[0], y + d[1]
	if not valid(nx, ny):
		break
	if lines[ny][nx] == '#':
		d = turn_right(*d)
	else:
		x, y = nx, ny
	

print(len(steps))


# II


steps.remove(start)

cnt = 0
for step in steps:
	step_x, step_y = step
	lines[step_y][step_x] = '#'

	d = (0, -1)  # up
	x, y = start

	steps_with_dir = set()
	while True:
		step = (x, y, *d)
		if step in steps_with_dir:  # loop detected
			cnt += 1
			break
		steps_with_dir.add(step)
		nx, ny = x + d[0], y + d[1]
		if not valid(nx, ny):
			break
		if lines[ny][nx] == '#':
			d = turn_right(*d)
		else:
			x, y = nx, ny

	lines[step_y][step_x] = '.'

print(cnt)