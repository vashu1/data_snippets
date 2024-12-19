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
	return any([check(s[len(i):]) for i in patterns if s.startswith(i)])


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
	return sum([count_combinations(s[len(i):]) for i in patterns if s.startswith(i)])


cnt = 0
for i in range(2, len(lines)):
	cnt += count_combinations(lines[i])

print(cnt)
