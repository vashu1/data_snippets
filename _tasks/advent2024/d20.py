from collections import defaultdict, Counter

lines = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d20.txt').readlines()]

lines = [list(line) for line in lines]

s = e = None
for y, line in enumerate(lines):
	for x, ch in enumerate(line):
		if ch == 'S':
			s = (x, y)
		elif ch == 'E':
			e = (x, y)


def valid(x, y):
	if not (0 < x < len(lines[0]) - 1):
		return False
	if not (0 < y < len(lines) - 1):
		return False
	return True


def neighbours(x, y):
	for i in [-1, 0, +1]:
		for j in [-1, 0, +1]:
			if (i != 0 or j != 0) and i * j == 0:
				x_, y_ = x + i, y + j
				if valid(x_, y_):
					yield (x_, y_)


def shortest():
	steps = defaultdict(set)
	visited = set()
	steps[0].add(s)
	visited.add(s)
	step = 0
	while True:
		for x_, y_ in steps[step]:
			for x, y in neighbours(x_, y_):
				if lines[y][x] != '#' and (x, y) not in visited:
					steps[step + 1].add((x, y))
					visited.add((x, y))
					if (x, y) == e:
						return step + 1
		step += 1


mx = shortest()

'''
cnt = 0
c = Counter()
for x in range(1, len(lines[0]) - 1):
	print(x)
	for y in range(1, len(lines) - 1):
		if lines[y][x] == '#':
			lines[y][x] = '.'
			v = shortest()
			if mx - v >= 100:
				cnt += 1
			c[mx - v] += 1
			lines[y][x] = '#'


del c[0]
print('RESULT 1:', cnt, c)
# 1372
'''


# II


def fill_steps(position, cells):
	px, py = position
	cells[py][px] = 0
	steps = defaultdict(set)
	visited = set()
	steps[0].add(position)
	visited.add(position)
	step = 0
	while True:
		no_update = True
		for x_, y_ in steps[step]:
			for x, y in neighbours(x_, y_):
				if lines[y][x] != '#' and (x, y) not in visited:
					steps[step + 1].add((x, y))
					cells[y][x] = step + 1
					visited.add((x, y))
					no_update = False
		step += 1
		if no_update:
			return


def cheat_neighbours(position, max_steps):
	steps = defaultdict(set)
	steps[0].add(position)
	visited = set()
	visited.add(position)
	step = 0
	while True:
		if step == max_steps:
			return
		for x_, y_ in steps[step]:
			for x, y in neighbours(x_, y_):
				if (x, y) not in visited:
					visited.add((x, y))
					steps[step + 1].add((x, y))
					if lines[y][x] != '#':
						if step > 0:
							yield step + 1, x, y
		step += 1



CHEAT_SAVES_MIN = 100

reached = [[-1 for _ in lines[0]] for _ in lines]
remains = [[-1 for _ in lines[0]] for _ in lines]

fill_steps(s, reached)
fill_steps(e, remains)
mx = shortest()

cnt = 0
c = Counter()
for y, line in enumerate(lines):
	for x, ch in enumerate(line):
		if lines[y][x] == '#':
			continue
		for cheat_used, ch_x, ch_y in cheat_neighbours((x, y), max_steps=20):
			cost = reached[y][x] + cheat_used + remains[ch_y][ch_x]
			if mx - cost >= CHEAT_SAVES_MIN:
				cnt += 1
				c[mx - cost] += 1

print(cnt)
