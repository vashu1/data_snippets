import portion as P

test = '''3-5
10-14
16-20
12-18

1
5
8
11
17
32'''

data = test.split('\n')
data = [s.strip() for s in open('05.txt').readlines()]

cnt = 0
intervals = P.empty()
for line in data:
	if not line:
		continue
	if '-' in line:
		a, b = line.split('-')
		a = int(a)
		b = int(b)
		intervals |= P.closed(a, b)
	else:
		a = int(line)
		if a in intervals:
			cnt += 1

print(cnt)

# II

print(sum([i.upper - i.lower + 1 for i in intervals]))	
