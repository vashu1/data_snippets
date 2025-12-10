
test = '''987654321111111
811111111111119
234234234234278
818181911112111'''

data = test.split('\n')
data = [s.strip() for s in open('03.txt').readlines()]


def search(i):
	m = 0
	for i1 in range(len(i)):
		for i2 in range(i1 + 1, len(i)):
			m = max(m, i[i1]*10 + i[i2])
	return m


s = 0
for line in data:
	line = [int(i) for i in list(line)]
	s += search(line)

print(s)

# II


def search2(arr, l):
	if not arr:
		return 0
	if l == 1:
		return max(arr)
	for i in range(9, 0, -1):
		if i in arr:
			v = search2(arr[arr.index(i)+1:], l-1)
			if v:
				return 10**(l-1) * i + v
	return 0


s = 0
for line in data:
	line = [int(i) for i in list(line)]
	s += search2(line, 12)

print(s)