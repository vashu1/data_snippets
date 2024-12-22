from collections import Counter

lines = '''1
10
100
2024'''
lines = lines.split('\n')
lines = [i.strip() for i in open('inputs/d22.txt').readlines()]


def mix(s, g):
	return s ^ g


def prune(s):
	return s % 16777216


def secret(s):
	g = s * 64
	s = mix(s, g)
	s = prune(s)
	g = s // 32
	s = mix(s, g)
	s = prune(s)
	g = s * 2048
	s = mix(s, g)
	s = prune(s)
	return s


def secret2000(s):
	for i in range(2000):
		s = secret(s)
	return s


assert mix(42, 15) == 37
assert prune(100000000) == 16113920
s = 123
vs = [
15887950,
16495136,
527345,
704524,
1553684,
12683156,
11100544,
12249484,
7753432,
5908254,
]

for v in vs:
	s = secret(s)
	assert s == v

assert secret2000(1) == 8685429
assert secret2000(10) == 4700978
assert secret2000(100) == 15273692
assert secret2000(2024) == 8667524


cnt = 0
for v in lines:
	cnt += secret2000(int(v))

print(cnt)


# II


wins = Counter()


def parse(s):
	prices = []
	for _ in range(2000):
		prices.append(s % 10)
		s = secret(s)

	diffs = [b - a for a, b in zip(prices, prices[1:])]
	firsts = {}
	for i in range(len(diffs) - 4):
		sequence = tuple(diffs[i:i+4])
		if sequence not in firsts:
			firsts[sequence] = prices[i + 4]

	for sequence, price in firsts.items():
		wins[sequence] += price


for v in lines:
	parse(int(v))

print(wins.most_common(1)[0])
