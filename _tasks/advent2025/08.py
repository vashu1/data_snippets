
test = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''

data = test.split('\n')
c = 10
data = [s.strip() for s in open('08.txt').readlines()]
c = 1_000

data = [i.split(',') for i in data]
data = [(int(i[0]), int(i[1]), int(i[2])) for i in data]

distances = []
for i in range(len(data)):
	for j in range(i+1, len(data)):
			x1, y1, z1 = data[i]
			x2, y2, z2 = data[j]
			d = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
			distances.append((d, i, j))

distances.sort(key=lambda x: x[0])

circuits = {i:{i} for i in range(len(data))}
indx = 0
while True:
	_, a, b = distances[indx]
	if a not in circuits[b]:   # join circuits
		s = circuits[a].union(circuits[b])
		for i in s:
			circuits[i] = s
	c -= 1
	if c == 0:
		break
	indx += 1

v = set([tuple(i) for i in circuits.values()])
v = [len(i) for i in v]
v.sort()
print(v[-1]*v[-2]*v[-3])

# II

while True:
	_, a, b = distances[indx]
	if a not in circuits[b]:   # join circuits
		s = circuits[a].union(circuits[b])
		for i in s:
			circuits[i] = s
		if len(s) == len(data):
			print(data[a][0]*data[b][0])
			break
	indx += 1
