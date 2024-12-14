from collections import defaultdict

lines = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d08.txt').readlines()]


def valid(x, y):
	if not 0 <= x < len(lines[0]):
		return False
	if not 0 <= y < len(lines):
		return False
	return True


antennaes = defaultdict(set)
for y, line in enumerate(lines):
	for x, c in enumerate(line):
		antennaes[c].add((x, y))

del antennaes['.']

antinodes = set()
for c in antennaes:
	for a in antennaes[c]:
		for b in antennaes[c]:
			if a >= b:
				continue
			x1, y1 = a
			x2, y2 = b
			dx, dy = x2 - x1, y2 - y1
			xa1, ya1 = x1 - dx, y1 - dy
			xa2, ya2 = x2 + dx, y2 + dy
			if valid(xa1, ya1):
				antinodes.add((xa1, ya1))
			if valid(xa2, ya2):
				antinodes.add((xa2, ya2))

print(len(antinodes))


# II


antinodes = set()
for c in antennaes:
	for a in antennaes[c]:
		for b in antennaes[c]:
			if a >= b:
				continue
			x1, y1 = a
			x2, y2 = b
			dx, dy = x2 - x1, y2 - y1
			n = 0
			while True:
				xa1, ya1 = x1 - dx * n, y1 - dy * n
				if valid(xa1, ya1):
					antinodes.add((xa1, ya1))
				else:
					break
				n += 1
			n = 0
			while True:
				xa2, ya2 = x2 + dx * n, y2 + dy * n
				if valid(xa2, ya2):
					antinodes.add((xa2, ya2))
				else:
					break
				n += 1

print(len(antinodes))