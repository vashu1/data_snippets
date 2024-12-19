import functools

lines = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d19.txt').readlines()]


@functools.lru_cache(maxsize=None)
def check(s):
	if not s:
		return True
	for i in patterns:
		if s.startswith(i):
			r = check(s[len(i):])
			if r:
				return True
	return False

patterns = set(lines[0].split(', '))
cnt = 0
for i in range(2, len(lines)):
	if check(lines[i]):
		cnt += 1

print(cnt)


# II


@functools.lru_cache(maxsize=None)
def count_combinations(s):
	if not s:
		return 1
	res = 0
	for i in patterns:
		if s.startswith(i):
			res += count_combinations(s[len(i):])
	return res


cnt = 0
for i in range(2, len(lines)):
	cnt += count_combinations(lines[i])

print(cnt)