from collections import defaultdict

lines = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d10.txt').readlines()]


def valid(x, y):
	if not 0 <= x < len(lines[0]):
		return False
	if not 0 <= y < len(lines):
		return False
	return True


def next_steps(x, y):
	res = []
	for i in [-1, 0, +1]:
		for j in [-1, 0, +1]:
			if (i != 0 or j != 0) and i * j == 0:
				x_, y_ = x + i, y + j
				if valid(x_, y_):
					if lines[y][x] == lines[y_][x_] - 1:
						res.append((x_, y_))
	return res


def score(x, y):
	trails = defaultdict(set)
	trails[0] = set([(x, y)])
	for i in range(9):
		for step in trails[i]:
			trails[i + 1].update(next_steps(*step))
	return len(trails[9])


cnt = 0
lines = [[-1 if i=='.' else int(i) for i in line] for line in lines]
for y, line in enumerate(lines):
	for x, c in enumerate(line):
		if c == 0:
			cnt += score(x, y)

print(cnt)


# II


def score2(x, y):
	if lines[y][x] == 9:
		return 1
	return sum([score2(*step) for step in next_steps(x, y)])


cnt = 0
lines = [[int(i) for i in line] for line in lines]
for y, line in enumerate(lines):
	for x, c in enumerate(line):
		if c == 0:
			cnt += score2(x, y)

print(cnt)