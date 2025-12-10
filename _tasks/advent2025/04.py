
test = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.'''

data = test.split('\n')
data = [s.strip() for s in open('04.txt').readlines()]


def neighbours(data, x, y):
	for i in [-1, 0, +1]:
		for j in [-1, 0, +1]:
			if i == 0 and j == 0:
				continue
			if not (0 <= x + i < len(data[0])):
				continue
			if not (0 <= y + j < len(data)):
				continue
			yield data[y+j][x+i]



cnt = 0
for y in range(len(data)):
	for x in range(len(data[0])):
		if data[y][x] == '@' and len([v for v in neighbours(data, x, y) if v == '@']) < 4:
			cnt += 1

print(cnt)

# II

data = [list(line) for line in data]

cnt = 0
while True:
	prev = cnt
	for y in range(len(data)):
		for x in range(len(data[0])):
			if data[y][x] == '@' and len([v for v in neighbours(data, x, y) if v == '@']) < 4:
				cnt += 1
				data[y][x] = '.'
	if prev == cnt:
		break

print(cnt)