
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