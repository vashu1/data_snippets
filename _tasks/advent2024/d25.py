
lines = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d25.txt').readlines()]

keys = []
locks = []
n = 0
scheme = []
while n <= len(lines):
	if n % 8 == 7:
		key = scheme[0] == '.....'
		if key:
			scheme = list(reversed(scheme))
		transposed_scheme = [[row[i] for row in scheme] for i in range(len(scheme[0]))]
		vals = tuple([row.count('#') - 1 for row in transposed_scheme])
		if key:
			keys.append(vals)
		else:
			locks.append(vals)
		#print(key, vals)
		scheme = []
	else:
		scheme.append(lines[n])
	n += 1

cnt = 0
for lock in locks:
	for key in keys:
		fits = all([a + b <= 5 for a, b in zip(lock, key)])
		if fits:
			cnt += 1

print(cnt)