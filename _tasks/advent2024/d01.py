

data = '''3   4
4   3
2   5
1   3
3   9
3   3'''

lines = data.split('\n')
lines = [i.strip() for i in open('d01.txt').readlines()]

bs, cs = [], []
for line in lines:
	vs = line.split(' ')
	b, c = vs[0], vs[-1]
	b = int(b)
	c = int(c)
	bs.append(b)
	cs.append(c)

bs.sort()
cs.sort()

s = 0
for b, c in zip(bs, cs):
	#print(abs(c-b))
	s += abs(c-b)

print(s)


# II

from collections import Counter

cs = Counter(cs)
s = 0
for b in bs:
    s += b * cs[b]

print(s)
