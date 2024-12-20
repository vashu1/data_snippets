# based on https://www.reddit.com/r/adventofcode/comments/1hhiawu/2024_day_18_part_2_visualization_of_my_algorithm/
# but I used 1 color

lines = [i.strip() for i in open('inputs/d18.txt').readlines()]

def valid(x, y):
	if not (0 <= x <= WHMAX):
		return False
	if not (0 <= y <= WHMAX):
		return False
	return True


def neighbours(x, y):
	for i in [-1, 0, +1]:
		for j in [-1, 0, +1]:
			if i != 0 or j != 0:
				x_, y_ = x + i, y + j
				if valid(x_, y_):
					yield (x_, y_)


def has_colored_neighbour(x_, y_):
	for x, y in neighbours(x_, y_):
		if grid[y][x] == 'R':
			return True
	return False


def color(x_, y_):
	stack = set([(x_, y_)])
	while stack:			
		xp, yp = stack.pop()
		for x, y in neighbours(xp, yp):
			if grid[y][x] == '#':
				grid[y][x] = 'R'
				stack.add((x, y))
				if x == 0 or y == WHMAX:
					return False
	return True


WHMAX = 70
s = 0, 0
e = WHMAX, WHMAX

grid = [['_' for _ in range(WHMAX + 1)] for _ in range(WHMAX + 1)]
for i in lines:
	bx, by = [int(j) for j in i.split(',')]
	grid[by][bx] = '#'
	if has_colored_neighbour(bx, by) or by == 0 or bx == WHMAX:
		grid[by][bx] = 'R'
		if not color(bx, by):
			print(i)
			break




