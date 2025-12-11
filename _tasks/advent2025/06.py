import math

test = '''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  '''

data = test.split('\n')
data = [s.strip() for s in open('06.txt').readlines()]

vals = []
for line in data:
	if '+' in line or '*' in line:
		s = 0
		operations = [op for op in line.split(' ') if op]
		for indx, op in enumerate(operations):
			nums = [row[indx] for row in vals]
			s += sum(nums) if op == '+' else math.prod(nums)
		print(s)
	else:
		vals.append([int(l) for l in line.split(' ') if l])

# II

d = [(indx, op) for indx, op in enumerate(data[-1]) if op in ['+', '*']]
d = d + [(len(data[0]) + 1, None)]
d = zip(d, d[1:])
rows = len(data) - 1
s = 0
for (i1, op), (i2, _) in d:
	vals = []
	for i in range(i1, i2 - 1):
		vals.append(int(''.join([data[j][i] for j in range(rows)])))
	assert op in ['+', '*']
	v = sum(vals) if op == '+' else math.prod(vals)
	s += v

print(s)
