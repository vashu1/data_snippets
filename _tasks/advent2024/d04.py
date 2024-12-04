import re

lines = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''
lines = lines.split('\n')
lines = [i.strip() for i in open('d04.txt').readlines()]

dirs = [
	(0,1),  # up
	(1,1),  # ur
	(1,0),  # right
	(1,-1),  # rd
	(0,-1),  # down
	(-1,-1),  # dl
	(-1,0),  # left
	(-1,1),  # lu
]
assert len(dirs) == len(set(dirs))


def valid(x, y):
	if not (0 <= x < len(lines[0])):
		return False
	if not (0 <= y < len(lines)):
		return False
	return True


def match(x0, y0, word, direction):
	for index, c in enumerate(word):
		x = x0 + direction[0] * index
		y = y0 + direction[1] * index
		if not valid(x, y):
			return False
		if not lines[y][x] == c:
			return False
	return True


cnt = 0
for direction in dirs:
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			if match(x, y, 'XMAS', direction):
				cnt += 1

print(cnt)


# II


def match2(x0, y0):
	if not (1 <= x < len(lines[0]) - 1):
		return False
	if not (1 <= y < len(lines) - 1):
		return False
	f = True
	f &= lines[y0][x0] == 'A'
	f &= set([lines[y0+1][x0+1], lines[y0-1][x0-1]]) == set(['M', 'S'])
	f &= set([lines[y0+1][x0-1], lines[y0-1][x0+1]]) == set(['M', 'S'])
	return f


cnt = 0
for y in range(len(lines)):
	for x in range(len(lines[0])):
		if match2(x, y):
			cnt += 1

print(cnt)





