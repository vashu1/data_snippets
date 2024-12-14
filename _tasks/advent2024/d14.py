from collections import Counter

lines = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d14.txt').readlines()]


# 101 tiles wide and 103 tiles tall
W, H = 101, 103
#W, H = 11, 7  # uncomment for test

def extract(line):
	p, v = line.split(' ')
	p = p.split('=')[1].split(',')
	v = v.split('=')[1].split(',')
	p = [int(p[0]), int(p[1])]
	v = [int(v[0]), int(v[1])]
	return p, v


def sign(v):
	return -1 if v < 0 else (0 if v == 0 else +1)


def robot_step(p, v):
	p[0] += v[0]
	p[1] += v[1]
	while p[0] >= W:
		p[0] -= W
	while p[0] < 0:
		p[0] += W
	while p[1] >= H:
		p[1] -= H
	while p[1] < 0:
		p[1] += H


quadrants = Counter()
for line in lines:
	p, v = extract(line)
	for _ in range(100):
		robot_step(p, v)
	p[0] -= W // 2 
	p[1] -= H // 2
	quadrants[(sign(p[0]), sign(p[1]))] += 1

res = quadrants[(-1, -1)] * quadrants[(+1, -1)] * quadrants[(-1, +1)] * quadrants[(+1, +1)]
print(res)


# II


robots = []
for line in lines:
	p, v = extract(line)
	robots.append((p, v))

n = 0
while True:
	data = [['_'] * W for i in range(H)]
	quadrants = Counter()
	for robot in robots:
		p, v = robot
		quadrants[(sign(p[0] - W // 2), sign(p[1] - H // 2))] += 1
		data[p[1]][p[0]] = '*'
	for line in data:
		print(''.join(line))
	print(n, '\n\n\n\n')
	n += 1
	for line in data:
		if '***********************' in ''.join(line):
			_ = input()
	#if quadrants[(-1, -1)] == quadrants[(+1, -1)] and quadrants[(-1, +1)] == quadrants[(+1, +1)]:
	#	_ = input()
	for robot in robots:
		p, v = robot
		robot_step(p, v)