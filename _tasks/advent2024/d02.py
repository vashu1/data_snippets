
data = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''

lines = data.split('\n')
lines = [i.strip() for i in open('inputs/d02.txt').readlines()]

cnt = 0
for line in lines:
	s = line.split(' ')
	s = list(map(int, s))
	ds = [(a - b) for a, b in zip(s, s[1:])]
	f1 = all([1 <= i <= 3 for i in ds])
	f2 = all([-3 <= i <= -1 for i in ds])
	if f1 or f2:
		cnt += 1

print(cnt)


# II


def test(line):
	ds = [(a - b) for a, b in zip(line, line[1:])]
	f1 = all([1 <= i <= 3 for i in ds])
	f2 = all([-3 <= i <= -1 for i in ds])
	return f1 or f2


cnt = 0
for line in lines:
	line = line.split(' ')
	line = list(map(int, line))
	if any([test(line)] + [test(line[:i] + line[i+1:]) for i in range(len(line))]):
		cnt += 1

print(cnt)