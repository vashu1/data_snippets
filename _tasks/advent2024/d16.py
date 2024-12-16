from heapq import heappush, heappop
from collections import defaultdict

lines = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################'''  # 11048
lines = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''  # 7036
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d16.txt').readlines()]


def turn_right(x, y):
	return -y, x


def turn_left(x, y):
	return y, -x


def try_right(position, direction):
	x, y = position
	dx, dy = turn_right(*direction)
	return lines[y + dy][x + dx]


def try_left(position, direction):
	x, y = position
	dx, dy = turn_left(*direction)
	return lines[y + dy][x + dx]


s, e = (1, len(lines) - 2), (len(lines[0]) - 2, 1)
v = (1, 0)  # East
paths = []
heappush(paths, (0, (s, v, [s])))
heappush(paths, (1000, (s, turn_left(*v), [s])))
visited = {i[1][:2]: i[0] for i in paths}
best_tiles = defaultdict(set)

res = []
while paths:
	score, (position, direction, path) = heappop(paths)
	x, y = position
	dx, dy = direction
	n = 0
	while True:
		n += 1
		x, y = x + dx, y + dy
		path.append((x, y))
		if lines[y][x] == '#':
			break
		if (x, y) == e:
			res.append(score + n)
			best_tiles[score + n].update(set(path))
		new_score = score + n + 1000
		if try_right((x, y), direction) != '#':
			p, d = (x, y), turn_right(*direction)
			if (p, d) not in visited or visited[(p, d)] >= new_score:  # change >= to > for fast 1st part
				visited[(p, d)] = new_score
				heappush(paths, (new_score, (p, d, list(path))))
		if try_left((x, y), direction) != '#':
			p, d = (x, y), turn_left(*direction)
			if (p, d) not in visited or visited[(p, d)] >= new_score:
				visited[(p, d)] = new_score
				heappush(paths, (new_score, (p, d, list(path))))

print(min(res))
print(len(best_tiles[min(res)]))
