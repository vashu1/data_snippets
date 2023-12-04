

lines = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.split('\n')

lines = [l.strip() for l in open('d03.txt').readlines()]

lines = [list(line.strip()) for line in lines]

def neighbours(lines, row, col):
	res = []
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			if i == 0 and j == 0:
				continue
			row_ = row + i
			col_ = col + j
			if row_ < 0 or col_ < 0:
				continue
			if row_ >= len(lines) or col_ >= len(lines[0]):
				continue
			assert len(lines[0]) == len(lines[row_])
			c = lines[row_][col_]
			res.append(c)
	return res


def check(lines, row, col):
	for c in neighbours(lines, row, col):
		if not c.isdigit() and not c == '.':
			return True
	return False


s = 0
for row in range(len(lines)):
	col = 0
	while col < len(lines[0]):
		d = 0
		f = False
		while col < len(lines[0]) and lines[row][col].isdigit():
			d = 10 * d +  int(lines[row][col])
			f |= check(lines, row, col)
			col += 1
		if f:
			s += d
		#if d:
		#	print(d, f)
		col += 1

print('sum', s)

# 2

marks = [[0 for j in range(len(lines[0]))]for i in range(len(lines))]
numbers = {}

count = 1
s = 0
for row in range(len(lines)):
	col = 0
	while col < len(lines[0]):
		d = 0
		f = False
		start = col
		while col < len(lines[0]) and lines[row][col].isdigit():
			d = 10 * d +  int(lines[row][col])
			f |= check(lines, row, col)
			col += 1
		if f:
			for col_ in range(start, col):
				marks[row][col_] = count
			numbers[count] = d
			count += 1
		col += 1

s = 0
for row in range(len(lines)):
	for col in range(len(lines[0])):
		if lines[row][col] == '*':
			n = neighbours(marks, row, col)
			n = [i for i in n if i > 0]
			n = set(n)
			if len(n) == 2:
				x1, x2 = n
				x1 = numbers[x1]
				x2 = numbers[x2]
				#print(x1, x2, x1 * x2)
				s +=  x1 * x2

print('sum', s)
