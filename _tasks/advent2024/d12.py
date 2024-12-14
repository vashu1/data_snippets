from collections import defaultdict

lines = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d12.txt').readlines()]


def valid(x, y):
	if not 0 <= x < len(lines[0]):
		return False
	if not 0 <= y < len(lines):
		return False
	return True


def neighbours(x, y):
	for i in [-1, 0, +1]:
		for j in [-1, 0, +1]:
			if (i != 0 or j != 0) and i * j == 0:
				x_, y_ = x + i, y + j
				if valid(x_, y_):
					yield (x_, y_)


def cnt_splits(lst):
	res = 0
	if lst:
		res +=1
		splits = [x1 for x1, x2 in zip(lst, lst[1:]) if x1 != x2 - 1]
		res += len(splits)
	return res


def xsides(xs):
	res = 0
	for y in xs:
		xs[y].sort()
		# upper
		if y == 0:
			xss = list(xs[y])
		else:
			xss = [x for x in xs[y] if lines[y][x] != lines[y-1][x]]
		res += cnt_splits(xss)
		# lower
		if y == len(lines) - 1:
			xss = list(xs[y])
		else:
			xss = [x for x in xs[y] if lines[y][x] != lines[y+1][x]]
		res += cnt_splits(xss)
	return res


def ysides(ys):
	res = 0
	for x in ys:
		ys[x].sort()
		# left
		if x == 0:
			yss = list(ys[x])
		else:
			yss = [y for y in ys[x] if lines[y][x] != lines[y][x-1]]
		res += cnt_splits(yss)
		# right
		if x == len(lines[0]) - 1:
			yss = list(ys[x])
		else:
			yss = [y for y in ys[x] if lines[y][x] != lines[y][x+1]]
		res += cnt_splits(yss)
	return res



def area_perimeter_sides(x, y, used):
	letter = lines[y][x]
	area = 0
	perimeter = 0
	stack = set([(x, y)])
	xs = defaultdict(list)
	ys = defaultdict(list)
	while stack:
		x, y = stack.pop()
		xs[y].append(x)
		ys[x].append(y)
		used[y][x] = True
		area += 1
		perimeter += 4
		for x_, y_ in neighbours(x, y):
			if lines[y_][x_] == letter:
				perimeter -= 1
			if lines[y_][x_] == letter and not used[y_][x_]:
				stack.add((x_, y_))
	sides = xsides(xs) + ysides(ys)
	return area, perimeter, sides


used = [[False for i in range(len(lines[0]))] for _ in range(len(lines))]
cnt1 = 0
cnt2 = 0
for y in range(len(lines)):
	for x in range(len(lines[0])):
		if not used[y][x]:
			area, perimeter, sides = area_perimeter_sides(x, y, used)
			cnt1 += area * perimeter
			cnt2 += area * sides

print(cnt1)
print(cnt2)