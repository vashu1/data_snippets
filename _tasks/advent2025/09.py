
# visualisation https://www.reddit.com/r/adventofcode/comments/1pimlzx/2025_day_9_part_2_visualization_is_prettier_than/

test = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''

data = test.split('\n')
data = [s.strip() for s in open('09.txt').readlines()]

data = [line.split(',') for line in data]
data = [(int(i[0]), int(i[1])) for i in data]
areas = []
for i in range(len(data)):
	for j in range(i+1, len(data)):
		a = data[i]
		b = data[j]
		areas.append(abs((a[0] - b[0] + 1) * (a[1] - b[1] + 1)))

print(max(areas))

# II


'''
sign = lambda x: +1 if x > 0 else (0 if x == 0 else -1)

angles = []
for (x1, y1), (x2, y2) in zip(data, data[1:] + [data[0]]):
	assert (x1 == x2) ^ (y1 == y2)
	if x1 == x2:
		angles.append(90 if y2 > y1 else 270)
	else:
		angles.append(180 if x2 < x1 else 0)

da = [a2 - a1 for a1, a2 in zip(angles, angles[1:])]
da = [(a if abs(a) == 90 else (sign(a) * -90)) for a in da]
print(angles)
print(da)

def cnt(arr):
	res = []
	indx1, indx2 = 0, 0
	while indx2 < len(arr):
		if arr[indx1] == arr[indx2]:
			indx2 += 1
		else:
			res.append(indx2 - indx1)
			indx1 = indx2
	res.append(indx2 - indx1)
	return res

print(set(cnt(da)))
print([i for i in cnt(da) if i > 1])
print(sum(da))

print('max dx', max([abs(x2 - x1) for (x1, y1), (x2, y2) in zip(data, data[1:])]))
print('max dy', max([abs(y2 - y1) for (x1, y1), (x2, y2) in zip(data, data[1:])]))
'''