from collections import defaultdict

lines = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0'''
lines = lines.split('\n')
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
			if (i != 0 or j != 0) and i * j == 0:
				x_, y_ = x + i, y + j
				if valid(x_, y_):
					yield (x_, y_)


WHMAX = 70
FALLEN = 1024
#WHMAX = 6    # comment out for example
#FALLEN = 12  # comment out for example
s = 0, 0
e = WHMAX, WHMAX

grid = [[True for _ in range(WHMAX + 1)] for _ in range(WHMAX + 1)]
for i in range(FALLEN):
	x, y = [int(i) for i in lines[i].split(',')]
	grid[y][x] = False

steps = defaultdict(set)
step = 1
steps[step].add(s)
visited = set()
visited.add(s)

while True:
	for x, y in steps[step]:
		if (x, y) == e:
			break
		for x_, y_ in neighbours(x, y):
			if (x_, y_) not in visited and grid[y_][x_]:
				visited.add((x_, y_))
				steps[step+1].add((x_, y_))
	if (x, y) == e:
		break
	step += 1

print(step-1)


# II

mn, mx = 0, len(lines) - 1
while True:
	if mn == mx - 1:
		print(lines[mn])
		exit()
	middle = mn + (mx - mn) // 2
	print(middle)

	grid = [[True for _ in range(WHMAX + 1)] for _ in range(WHMAX + 1)]
	for i in range(middle):
		bx, by = [int(i) for i in lines[i].split(',')]
		grid[by][bx] = False

	steps = defaultdict(set)
	step = 1
	steps[step].add(s)
	visited = set()
	visited.add(s)

	while True:
		if not steps[step]:
			mx = middle
			break
		for x, y in steps[step]:
			if (x, y) == e:
				break
			for x_, y_ in neighbours(x, y):
				if (x_, y_) not in visited and grid[y_][x_]:
					visited.add((x_, y_))
					steps[step+1].add((x_, y_))
		if (x, y) == e:
			mn = middle
			break
		step += 1
